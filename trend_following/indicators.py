# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 14:58
# @Author  : 
# @File    : indicators.py

import numpy as np
import talib
from talib import stream

import os
import sys

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(PROJECT_ROOT)

from common.use_api import Signal


class MACD:
    """
    Basic knowledge: https://www.investopedia.com/terms/m/macd.asp
    """
    def __init__(self, fast_period=12, slow_period=26, signal_period=9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.data_num = slow_period + signal_period - 1

        self.latest_macd = np.nan
        self.latest_signal = np.nan

    def cal_inc(self, data):
        new_macd, new_signal, _ = stream.MACD(data['Close'].copy().values,
                                              fastperiod=self.fast_period,
                                              slowperiod=self.slow_period,
                                              signalperiod=self.signal_period)
        # new_macd, new_signal = new_macd[-1], new_signal[-1]

        if new_macd > new_signal and self.latest_macd < self.latest_signal:
            # the MACD line crosses up through the average line
            signal_cross = Signal.Enter
        elif new_macd < new_signal and self.latest_macd > self.latest_signal:
            signal_cross = Signal.Exit
        else:
            signal_cross = Signal.Stay

        self.latest_macd = new_macd
        self.latest_signal = new_signal
        return signal_cross, new_macd, new_signal

    def cal(self, data):
        macd, signal, _ = talib.MACD(data['Close'].copy().values,
                                     fastperiod=self.fast_period,
                                     slowperiod=self.slow_period,
                                     signalperiod=self.signal_period)

        signal_cross = np.full(macd.shape, Signal.Hold)
        for i in range(1, len(data)):
            if macd[i] > signal[i] and macd[i - 1] < signal[i - 1]:  # the MACD line crosses up
                # through the average line
                signal_cross[i] = Signal.Enter
            elif macd[i] < signal[i] and macd[i - 1] > signal[i - 1]:  # crosses down
                signal_cross[i] = Signal.Exit

        return signal_cross, macd, signal


class BollingerBands:
    """
    Basic knowledge: https://www.investopedia.com/terms/b/bollingerbands.asp
    """
    def __init__(self, init_data, w=20):
        init_data['MA'] = init_data['Close'].rolling(window=w).mean()
        init_data['std'] = init_data['Close'].rolling(window=w).std()
        init_data['upper'] = init_data['MA20'] + 2 * init_data['std']
        init_data['lower'] = init_data['MA20'] - 2 * init_data['std']
        init_data['signal'] = Signal.Hold

        self.data = init_data.copy()
        self.container = None
        self.num = self.num + 1
        self.window = w

        self.latest_upper = self.data['upper'][-1]
        self.latest_lower = self.data['lower'][-1]

    def __add_item(self, new_item):
        self.data.append(new_item, ignore_index=True)
        self.num = self.num + 1

    def __call__(self, new_item):
        self.__add_item(new_item)
        self.container = self.data['Close'].tail(self.window)

        mean = self.container.mean()
        std = self.container.std()

        if self.data['Close'][-1] > self.latest_upper:
            signal = Signal.Enter
        elif self.data['Close'][-1] < self.latest_lower:
            signal = Signal.Exit
        else:
            signal = Signal.Stay

        self.data['MA'][-1] = mean
        self.data['std'][-1] = std
        self.data['signal'][-1] = signal

        return signal
