# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 11:28
# @Author  : 
# @File    : hybrid_order.py

from common.use_api import Signal



def hybrid_strategy(macd, trix, bolling, price, capital, position, funding,lever,config):
    """
    利用MACD、TRIX、BOLL等策略编写一个混合择时策略
    :param macd: MACD信号
    :param trix: TRIX信号
    :param bolling: BOLLING信号
    :param price: 当前价格
    :param capital: 当前资金
    :param position: 当前头寸
    :param config: 配置参数
    :param funding: 融资金额
    :param lever: 杠杆倍数
    :return: 请返回三个结果：1.flag（表示最终是买、卖还是不买不买，分别用Signal.Enter，Signal.Exit和Signal.Stay表示）。
                          2.new_cap 剩余资金
                          3.new_pos 头寸
    """
    signal = 0.43*macd.value +0.43*bolling.value +0.14*trix.value
    if signal >= 0.86 and lever==0:
        signal = Signal.Leverage
        funding = capital if capital>0 else position*price
        position += (capital+funding)/price
        capital = 0
        lever = 2
    elif signal >= 0.43 and position <= 0:
        signal = Signal.Enter
        position += capital/price
        capital=0
    elif signal >= 0:
        signal = Signal.Stay
        capital=capital
        position=position
    elif signal < 0 and signal > -0.86 :
        signal = Signal.Exit
        if position > 0:
            capital=position*price-funding
            funding=0
            position=0
            lever = 0
    elif signal <= -0.86 :
         signal = Signal.Put
         if position > 0:
            capital=position*price-funding
            funding=0
            position=0
            lever = 0
            position = -capital/price
            capital = 2*capital
         if position == 0:
            position = -capital/price
            capital = 2*capital

             
    return signal,capital, position,funding,lever
