import torch
import torch.nn.functional as F
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter

import flask
from flask import Flask, request

from ...utils.deploy import get_free_tcp_port
from ...utils.learning import adjust_learning_rate
from ...utils.log import logger
from ...base.module import Module

from .model import Config, TextCNN
from .config import DEVICE, DEFAULT_CONFIG
from .tool import re_tool, TEXT, LABEL
from .utils.preprocess import handle_line

seed = 2019
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)


class RE(Module):
    """
    """

    def __init__(self):
        self._model = None
        self._word_vocab = None
        self._label_vocab = None

    def train(self, train_path, save_path=DEFAULT_CONFIG['save_path'], dev_path=None, vectors_path=None, log_dir=None, **kwargs):
        writer = SummaryWriter(log_dir=log_dir)
        train_dataset = re_tool.get_dataset(train_path)
        if dev_path:
            dev_dataset = re_tool.get_dataset(dev_path)
            word_vocab, label_vocab = re_tool.get_vocab(train_dataset, dev_dataset)
        else:
            word_vocab, label_vocab = re_tool.get_vocab(train_dataset)
        self._word_vocab = word_vocab
        self._label_vocab = label_vocab
        config = Config(word_vocab, label_vocab, save_path=save_path, vector_path=vectors_path, **kwargs)
        train_iter = re_tool.get_iterator(train_dataset, batch_size=config.batch_size)
        textcnn = TextCNN(config)
        # print(textcnn)
        writer.add_graph(textcnn, (next(iter(train_iter))).text)
        writer.flush()
        self._model = textcnn
        optim = torch.optim.Adam(textcnn.parameters(), lr=config.lr)
        for epoch in range(config.epoch):
            textcnn.train()
            acc_loss = 0
            for item in tqdm(train_iter):
                optim.zero_grad()
                logits = self._model(item.text)
                item_loss = F.cross_entropy(logits, item.label)
                acc_loss += item_loss.item()
                item_loss.backward()
                optim.step()
            logger.info('epoch: {}, acc_loss: {}'.format(epoch, acc_loss))
            writer.add_scalar('re_train/acc_loss', acc_loss, epoch)
            if dev_path:
                dev_score = self._validate(dev_dataset)
                logger.info('dev score:{}'.format(dev_score))
                writer.add_scalar('re_train/dev_score', dev_score, epoch)
            writer.flush()
            adjust_learning_rate(optim, config.lr / (1 + (epoch + 1) * config.lr_decay))
        writer.flush()
        config.save()
        textcnn.save()

    def predict(self, entity1: str, entity2: str, sentence: str):
        self._model.eval()
        text = handle_line(entity1, entity2, sentence)
        vec_text = torch.tensor([self._word_vocab.stoi[x] for x in text])
        vec_text = vec_text.reshape(1, -1).to(DEVICE)
        vec_predict = self._model(vec_text)[0]
        soft_predict = torch.softmax(vec_predict, dim=0)
        predict_prob, predict_index = torch.max(soft_predict.cpu().data, dim=0)
        predict_class = self._label_vocab.itos[predict_index]
        predict_prob = predict_prob.item()
        return predict_prob, predict_class

    def load(self, save_path=DEFAULT_CONFIG['save_path']):
        config = Config.load(save_path)
        textcnn = TextCNN(config)
        textcnn.load()
        self._model = textcnn
        self._word_vocab = config.word_vocab
        self._label_vocab = config.label_vocab
        self._check_vocab()

    def test(self, test_path):
        self._model.eval()
        test_dataset = re_tool.get_dataset(test_path)
        test_score = self._validate(test_dataset)
        logger.info('test score:{}'.format(test_score))

    def _validate(self, dev_dataset, batch_size=DEFAULT_CONFIG['batch_size']):
        self._model.eval()
        dev_score_list = []
        dev_iter = re_tool.get_iterator(dev_dataset, batch_size=batch_size)
        for dev_item in tqdm(dev_iter):
            item_score = re_tool.get_score(self._model, dev_item.text, dev_item.label)
            dev_score_list.append(item_score)
        return sum(dev_score_list) / len(dev_score_list)

    def _check_vocab(self):
        if not hasattr(TEXT, 'vocab'):
            TEXT.vocab = self._word_vocab
        if not hasattr(LABEL, 'vocab'):
            LABEL.vocab = self._label_vocab

    def deploy(self, route_path="/re", host="localhost", port=None, debug=False):
        app = Flask(__name__)

        @app.route(route_path + '/predict', methods=['POST', 'GET'])
        def predict():
            entity1 = request.args.get('entity1', '')
            entity2 = request.args.get('entity2', '')
            sentence = request.args.get('sentence', '')
            result = self.predict(entity1, entity2, sentence)
            return flask.jsonify({
                    'state': 'OK',
                    'result': {
                        'prob': result[0],
                        'class': result[1]
                        }
                })
        if not port:
            port = get_free_tcp_port()
        app.run(host=host, port=port, debug=debug)
