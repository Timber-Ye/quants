# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 15:06
# @Author  : 
# @File    : hybrid_timing.py

from common.config import _CN as cfg

cfg.SETUP.DATA_SOURCE = '../data/SH000300.csv'

cfg.MACD.FAST_PERIOD = 12
cfg.MACD.SLOW_PERIOD = 26
cfg.MACD.SIGNAL_PERIOD = 9

cfg.BOLL.WINDOW = 20

cfg.TRIX.TIME_PERIOD = 30
cfg.TRIX.BUY_THRESHOLD = 2e-3
cfg.TRIX.SELL_THRESHOLD = -2e-3