# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 13:38
# @Author  : 
# @File    : macd_vanilla.py.py


from common.config import _CN as cfg

cfg.SETUP.DATA_SOURCE = '../data/SH000300.csv'

cfg.MACD.FAST_PERIOD = 12
cfg.MACD.SLOW_PERIOD = 30
cfg.MACD.SIGNAL_PERIOD = 9

cfg.SHARPE.LOOKBACK_PERIOD = 100

