# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 14:51
# @Author  : 
# @File    : trix_vanilla.py


import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(PROJECT_ROOT)

from trend_following.indicators import TRIX
import trend_following.vanilla_order as vnl
from common.use_api import data_replay


def test_offline(data, init_capital=1e6):
    trix = TRIX(timeperiod=30)

    data['Signal_Cross'], data['TRIX'], data['Signal'] = trix.cal(data)

    order = vnl.Vanilla()
    capital = init_capital
    position = 0

    data['Capital'] = 0.0
    data['Shares'] = 0.0

    equity_curve = [capital]
    price = 0

    for i in range(0, len(data)):
        price = data['Close'][i]
        signal = data['Signal_Cross'][i]

        capital, position = order(signal, price, capital, position)

        data.loc[i, 'Capital'] = capital
        data.loc[i, 'Shares'] = position

        # 更新资金曲线
        equity_curve.append(capital + position * price)

    # 计算动量指标
    data['Return'] = data['Close'].pct_change()
    data['Momentum'] = data['Return'].rolling(window=12).sum()

    data.to_csv(os.path.join(PROJECT_ROOT + '/data/') + 'trix_vanilla_test_offline.csv')

    # plt.plot(equity_curve)
    # plt.title('Equity Curve')
    # plt.xlabel('Date')
    # plt.ylabel('Equity')
    # plt.show()

    return capital + position * price


def test_online(data, init_capital=1e6):
    record = pd.DataFrame(columns=['Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'TRIX',
                                   'Signal', 'Signal_Cross', 'Capital', 'Shares'])
    trix = TRIX(timeperiod=30)
    order = vnl.Vanilla()

    # 初始化资金曲线
    capital = init_capital
    position = 0
    price = 0
    equity_curve = [capital]

    for i, new in enumerate(data_replay(full_data)):
        record.loc[i] = new
        price = new['Close']
        new['Signal_Cross'], new['TRIX'], new['Signal'] = trix.cal_inc(record)

        capital, position = order(new['Signal_Cross'], price, capital, position)
        new['Capital'], new['Shares'] = capital, position
        # 更新资金曲线
        equity_curve.append(capital + position * price)
        record.loc[i] = new

    # 计算动量指标
    record['Return'] = record['Close'].pct_change()
    record['Momentum'] = record['Return'].rolling(window=12).sum()

    record.to_csv(os.path.join(PROJECT_ROOT + '/data/') + 'trix_vanilla_test_online.csv')
    return capital + position * price


if __name__ == '__main__':
    import os

    PROJECT_DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/')

    full_data = pd.read_csv(PROJECT_DATA_DIR + 'SH000300.csv')

    # final_equity = test_offline(full_data, init_capital=1e6)
    final_equity = test_online(full_data, init_capital=1e6)

    print('收益回报率：{}'.format((final_equity-1e6)/1e6))  # offline: 0.36772555140306495 online: 0.25921414485556027

