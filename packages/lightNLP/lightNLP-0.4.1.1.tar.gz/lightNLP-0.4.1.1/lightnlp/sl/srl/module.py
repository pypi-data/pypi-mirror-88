import torch
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter

import flask
from flask import Flask, request

from ...utils.deploy import get_free_tcp_port
from ...utils.learning import adjust_learning_rate
from ...utils.log import logger
from ...base.module import Module

from .config import DEVICE, DEFAULT_CONFIG
from .model import Config, BiLstmCrf
from .tool import srl_tool
from .utils.convert import iobes_ranges

seed = 2019
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)


class SRL(Module):
    """
    """
    def __init__(self):
        self._model = None
        self._word_vocab = None
        self._tag_vocab = None
        self._pos_vocab = None
    
    def train(self, train_path, save_path=DEFAULT_CONFIG['save_path'], dev_path=None, vectors_path=None, log_dir=None,
              **kwargs):
        writer = SummaryWriter(log_dir=log_dir)
        train_dataset = srl_tool.get_dataset(train_path)
        if dev_path:
            dev_dataset = srl_tool.get_dataset(dev_path)
            word_vocab, pos_vocab, tag_vocab = srl_tool.get_vocab(train_dataset, dev_dataset)
        else:
            word_vocab, pos_vocab, tag_vocab = srl_tool.get_vocab(train_dataset)
        self._word_vocab = word_vocab
        self._pos_vocab = pos_vocab
        self._tag_vocab = tag_vocab
        config = Config(word_vocab, pos_vocab, tag_vocab, save_path=save_path, vector_path=vectors_path, **kwargs)
        train_iter = srl_tool.get_iterator(train_dataset, batch_size=config.batch_size)
        bilstmcrf = BiLstmCrf(config)
        self._model = bilstmcrf
        optim = torch.optim.Adam(bilstmcrf.parameters(), lr=config.lr)
        for epoch in range(config.epoch):
            bilstmcrf.train()
            acc_loss = 0
            for item in tqdm(train_iter):
                bilstmcrf.zero_grad()
                item_text_sentences = item.text[0]
                item_text_lengths = item.text[1]
                item_loss = (-bilstmcrf.loss(item_text_sentences, item_text_lengths, item.pos, item.rel, item.tag)) / item.tag.size(1)
                acc_loss += item_loss.view(-1).cpu().data.tolist()[0]
                item_loss.backward()
                optim.step()
            logger.info('epoch: {}, acc_loss: {}'.format(epoch, acc_loss))
            writer.add_scalar('srl_train/acc_loss', acc_loss, epoch)
            if dev_path:
                dev_score = self._validate(dev_dataset)
                logger.info('dev score:{}'.format(dev_score))
                writer.add_scalar('srl_train/dev_score', dev_score, epoch)
            writer.flush()
            adjust_learning_rate(optim, config.lr / (1 + (epoch + 1) * config.lr_decay))
        writer.close()
        config.save()
        bilstmcrf.save()

    def predict(self, word_list, pos_list, rel_list):
        self._model.eval()
        assert len(word_list) == len(pos_list) == len(rel_list)
        vec_text = torch.tensor([self._word_vocab.stoi[x] for x in word_list]).view(-1, 1).to(DEVICE)
        len_text = torch.tensor([len(vec_text)]).to(DEVICE)
        vec_pos = torch.tensor([self._pos_vocab.stoi[x] for x in pos_list]).view(-1, 1).to(DEVICE)
        vec_rel = torch.tensor([int(x) for x in rel_list]).view(-1, 1).to(DEVICE)
        vec_predict = self._model(vec_text, vec_pos, vec_rel, len_text)[0]
        tag_predict = [self._tag_vocab.itos[i] for i in vec_predict]
        return iobes_ranges([x for x in word_list], tag_predict)

    def load(self, save_path=DEFAULT_CONFIG['save_path']):
        config = Config.load(save_path)
        bilstmcrf = BiLstmCrf(config)
        bilstmcrf.load()
        self._model = bilstmcrf
        self._word_vocab = config.word_vocab
        self._tag_vocab = config.tag_vocab
        self._pos_vocab = config.pos_vocab
    
    def test(self, test_path):
        test_dataset = srl_tool.get_dataset(test_path)
        test_score = self._validate(test_dataset)
        logger.info('test score:{}'.format(test_score))
    
    def _validate(self, dev_dataset):
        self._model.eval()
        dev_score_list = []
        for dev_item in tqdm(dev_dataset):
            item_score = srl_tool.get_score(self._model, dev_item.text, dev_item.tag, dev_item.pos, dev_item.rel,
                                            self._word_vocab, self._tag_vocab, self._pos_vocab)
            dev_score_list.append(item_score)
        return sum(dev_score_list) / len(dev_score_list)

    def deploy(self, route_path="/srl", host="localhost", port=None, debug=False):
        app = Flask(__name__)

        @app.route(route_path + '/predict', methods=['POST', 'GET'])
        def predict():
            word_list = request.args.get('word_list', [])
            pos_list = request.args.get('pos_list', [])
            rel_list = request.args.get('rel_list', [])
            result = self.predict(word_list, pos_list, rel_list)
            return flask.jsonify({
                    'state': 'OK',
                    'result': {
                        'result': result
                        }
                })
        if not port:
            port = get_free_tcp_port()
        app.run(host=host, port=port, debug=debug)
