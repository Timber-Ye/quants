# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 11:51
# @Author  : 
# @File    : config.py


from yacs.config import CfgNode as CN

_CN = CN()


_CN.SETUP = CN()  # 基本参数
_CN.SETUP.DATA_SOURCE = None  # 数据
_CN.SETUP.INIT_CAPITAL = 1000000.0  # 起始资金
_CN.SETUP.RISK_FREE = 0.015  # 无风险收益（用于计算夏普率）


_CN.MACD = CN()  # MACD指标参数
_CN.MACD.FAST_PERIOD = 12
_CN.MACD.SLOW_PERIOD = 26
_CN.MACD.SIGNAL_PERIOD = 9


_CN.BOLL = CN()  # Bollinger指标参数
_CN.BOLL.WINDOW = 20


_CN.TRIX = CN()  # TRIX指标参数
_CN.TRIX.TIME_PERIOD = 30
_CN.TRIX.BUY_THRESHOLD = 2e-3
_CN.TRIX.SELL_THRESHOLD = -2e-3


_CN.SHARPE = CN()  # 夏普比参数
_CN.SHARPE.LOOKBACK_PERIOD = 60


def get_cfg_defaults():
    """Get a yacs CfgNode object with default values for my_project."""
    # Return a clone so that the defaults will not be altered
    # This is for the "local variable" use pattern
    return _CN.clone()