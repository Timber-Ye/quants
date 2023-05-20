# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 11:28
# @Author  : 
# @File    : hybrid_order.py

from common.use_api import Signal


def hybrid_strategy(macd, trix, bolling, price, capital, position, config):
    """
    利用MACD、TRIX、BOLL等策略编写一个混合择时策略
    :param macd: MACD信号
    :param trix: TRIX信号
    :param bolling: BOLLING信号
    :param price: 当前价格
    :param capital: 当前资金
    :param position: 当前头寸
    :param config: 配置参数
    :return: 请返回三个结果：1.flag（表示最终是买、卖还是不买不买，分别用Signal.Enter，Signal.Exit和Signal.Stay表示）。
                          2.new_cap 剩余资金
                          3.new_pos 头寸
    """
    return Signal.Stay, capital, position

