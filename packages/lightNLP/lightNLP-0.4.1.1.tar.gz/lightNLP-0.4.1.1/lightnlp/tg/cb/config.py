from ...base.config import DEVICE
DEFAULT_CONFIG = {
    'lr': 0.02,
    'epoch': 500,
    'lr_decay': 0.05,
    'batch_size': 128,
    'dropout': 0.5,
    'static': False,
    'non_static': False,
    'embedding_dim': 100,
    'clip': 10,
    'num_layers': 2,
    'vector_path': '',
    'vocabulary_size': 0,
    'word_vocab': None,
    'save_path': './cb_saves',
    'method': 'dot',
    'teacher_forcing_ratio': 0.5
}
