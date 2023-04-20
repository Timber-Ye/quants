# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 14:44
# @Author  : 
# @File    : vanilla_order.py

import os
import sys

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(PROJECT_ROOT)

from common.use_api import Signal


class Vanilla:
    def __init__(self):
        self.entry_price = 0

    def __enter_position(self, price, capital, position):
        new_pos = capital / price  # 全仓买入
        new_cap = 0
        self.entry_price = price
        return new_cap, new_pos

    def __exit_position(self, price, capital, position):
        new_cap = position * price
        new_pos = 0
        self.entry_price = 0
        return new_cap, new_pos

    def __call__(self, signal, price, capital, position):
        new_cap = capital
        new_pos = position

        # 入场信号
        if signal == Signal.ToBuy:
            new_cap, new_pos = self.__enter_position(price, capital, position)

        # 离场信号
        if signal == Signal.ToSell:
            new_cap, new_pos = self.__exit_position(price, capital, position)

        return new_cap, new_pos

