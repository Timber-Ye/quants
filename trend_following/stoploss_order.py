# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 11:06
# @Author  : 
# @File    : stoploss_order.py.py

import os
import sys

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(PROJECT_ROOT)

from common.use_api import Signal


class StopLossOrder:
    def __init__(self,
                 entry_multiplier=1.01,  # 入场倍数
                 exit_multiplier=0.99,  # 离场倍数
                 max_holding_period=20,  # 最长持仓天数
                 stop_loss_multiplier=0.98,  # 止损倍数
                 stop_loss_period=5,  # 止损触发期
                 trailing_stop_multiplier=0.98,  # 移动止损倍数
                 trailing_stop_period=5  # 移动止损触发期
                 ):
        self.entry_multiplier = entry_multiplier
        self.exit_multiplier = exit_multiplier
        self.max_holding_period = max_holding_period
        self.stop_loss_multiplier = stop_loss_multiplier
        self.stop_loss_period = stop_loss_period
        self.trailing_stop_multiplier = trailing_stop_multiplier
        self.trailing_stop_period = trailing_stop_period

        self.entry_price = 0
        self.stop_loss = 0
        self.trailing_high = 0
        self.trailing_low = 0
        self.holding_period = 0

    def __enter_position(self, price, capital, position):
        new_pos = capital // price
        self.entry_price = price
        self.stop_loss = price * self.stop_loss_multiplier
        self.holding_period = 0
        self.trailing_high = price
        self.trailing_low = price
        new_cap = capital - new_pos * price

        return new_cap, new_pos

    def __exit_position(self, price, capital, position):
        new_cap = capital + position * price
        new_pos = 0
        self.entry_price = 0
        self.stop_loss = 0
        self.holding_period = 0
        self.trailing_high = 0
        self.trailing_low = 0

        return new_cap, new_pos

    def __call__(self, signal, price, capital, position):
        new_cap = capital
        new_pos = position
        flag = Signal.Stay
        # 入场信号
        if (signal == Signal.Enter) & (position == 0) & (self.holding_period == 0):
            new_cap, new_pos = self.__enter_position(price * self.entry_multiplier, capital, position)
            flag = Signal.Enter

        # 离场信号
        elif ((signal == Signal.Exit) | (self.holding_period >= self.max_holding_period)) & (position != 0):
            new_cap, new_pos = self.__exit_position(price * self.exit_multiplier, capital, position)
            flag = Signal.Exit

        # 止损信号
        elif (price < self.stop_loss) & (position != 0):
            new_cap, new_pos = self.__exit_position(self.stop_loss, capital, position)
            flag = Signal.StopLoss

        # 移动止损信号
        elif (price > self.trailing_high) & (position != 0):
            self.trailing_high = price
            self.trailing_low = price * self.trailing_stop_multiplier
            self.stop_loss = self.trailing_low

        elif (price < self.trailing_low) & (position != 0):
            self.trailing_low = price
            self.trailing_high = price * self.trailing_stop_multiplier
            self.stop_loss = self.trailing_high

        # 更新持仓期
        if new_pos != 0:
            self.holding_period += 1

        return flag, new_cap, new_pos

