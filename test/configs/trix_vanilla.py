# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 15:13
# @Author  : 
# @File    : trix_vanilla.py.py


from common.config import _CN as cfg


cfg.SETUP.DATA_SOURCE = '../data/SH000300.csv'

cfg.TRIX.TIME_PERIOD = 30
cfg.TRIX.BUY_THRESHOLD = 2e-3
cfg.TRIX.SELL_THRESHOLD = -2e-3

