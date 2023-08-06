import argparse
import os
import random
import numpy as np
import sys
import torch
import logging
from .utils import *
from collections import namedtuple

# set random seeds
os.environ['PYTHONHASHSEED'] = str(1234)
random.seed(1234)
np.random.seed(1234)
torch.manual_seed(1234)
torch.cuda.manual_seed(1234)
torch.cuda.manual_seed_all(1234)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


class Config:
    def __init__(self):
        self.xlmr_model_name = 'xlm-roberta-base'
        self.xlmr_dropout = 0.3
        self.hidden_num = 300
        self.linear_dropout = 0.1
        self.linear_bias = 1
        self.linear_activation = 'relu'
        self.batch_size = 16
        self.eval_batch_size = 16
        self.max_input_length = 512
        self.working_dir = os.path.dirname(os.path.realpath(__file__))


# configuration
config = Config()
