# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 21:25
# @Author  : 
# @File    : macd_vanilla.py

import os
import sys

import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(PROJECT_ROOT)

from trend_following.indicators import MACD
from trend_following.vanilla_order import Vanilla
from common.use_api import Signal, data_replay


def test_online(full_data):
    init_capital = 1000000.0  # 起始资金

    data = pd.DataFrame(columns=['Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'MACD',
                                 'Signal', 'Signal_Cross', 'Capital', 'Shares'])
    macd = MACD()
    order = Vanilla()
    for i, new in enumerate(data_replay(full_data)):
        data.loc[i] = new
        new['Signal_Cross'], new['MACD'], new['Signal'] = macd.cal_inc(data)

        if i == 0:  # The first day all in
            new['Signal_Cross'] = Signal.Enter
            new['Capital'] = 0.0
            new['Shares'] = init_capital / new['Close']

        else:
            new['Capital'], new['Shares'] = order(new['Signal_Cross'],
                                                  new['Close'],
                                                  data['Capital'][i-1],
                                                  data['Shares'][i-1])

        data.loc[i] = new

    data['Returns'] = np.log(data['Close'] / data['Close'].shift(1))
    data['Cumulative_Returns'] = data['Returns'].cumsum()

    data.to_csv(os.path.join(PROJECT_ROOT + '/data/') + 'macd_test_online-2.csv')


def test_offline(data):
    macd = MACD()
    data['Signal_Cross'], data['MACD'], data['Signal'] = macd.cal(full_data)

    data.loc[0, 'Signal_Cross'] = Signal.Enter  # the first day all in
    # 计算收益率和资金曲线
    capital = 1000000.0  # 起始资金
    data['Shares'] = 0.0
    data['Capital'] = 0.0
    for i in range(0, len(data)):
        if data['Signal_Cross'][i] == Signal.Enter:  # to buy
            data.loc[i, 'Shares'] = capital / data['Close'][i]
            capital = 0  # all in

        elif data['Signal_Cross'][i] == Signal.Exit:  # to sell
            capital = data['Close'][i] * data['Shares'][i - 1]
            data.loc[i, 'Shares'] = 0  # sell out

        else:
            data.loc[i, 'Shares'] = data['Shares'][i - 1]

        data.loc[i, 'Capital'] = capital  # remains

    data['Returns'] = np.log(data['Close'] / data['Close'].shift(1))
    data['Cumulative_Returns'] = data['Returns'].cumsum()

    data.to_csv(os.path.join(PROJECT_ROOT + '/data/') + 'macd_test_offline.csv')


if __name__ == '__main__':
    import os

    PROJECT_DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/')

    full_data = pd.read_csv(PROJECT_DATA_DIR + 'SH000300.csv')

    test_online(full_data)
    # test_offline(full_data)