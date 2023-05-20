# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 11:05
# @Author  : 
# @File    : ma_stoploss.py

import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(PROJECT_ROOT)

from trend_following.indicators import BollingerBands
import trend_following.stoploss_order as stpl
from common.use_api import data_replay
from utils.cal_sharpe_ratio import cal_sharpe_ratio


def test_offline(data, init_capital=1e6):
    boll = BollingerBands(w=20)  # 布林线

    data['Signal_Cross'], data['MA'], _, data['Upper'], data['Lower'] = boll.cal(data)

    order = stpl.StopLossOrder()
    capital = init_capital
    position = 0

    data['Capital'] = 0.0
    data['Shares'] = 0.0
    data['Assets'] = 0.0
    # 初始化资金曲线
    equity_curve = [capital]

    for i in range(0, len(data)):
        price = data['Close'][i]
        signal = data['Signal_Cross'][i]
        data.loc[i, 'Signal_Cross'], capital, position = order(signal, price, capital, position)
        data.loc[i, 'Capital'] = capital
        data.loc[i, 'Shares'] = position

        # 更新资金曲线
        equity = capital + position * price
        equity_curve.append(equity)

        data.loc[i, 'Assets'] = equity

    # 计算动量指标
    data['Return'] = data['Assets'].pct_change()
    data['Momentum'] = data['Return'].rolling(window=12).sum()
    data['Sharpe'] = cal_sharpe_ratio(data, risk_free_rate=0.0)

    data.to_csv(os.path.join(PROJECT_ROOT + '/data/') + 'ma_stop_loss_test_offline.csv')

    plt.plot(equity_curve)
    plt.title('Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Equity')
    plt.show()


def test_online(data, init_capital=1e6):
    record = pd.DataFrame(columns=['Date', 'Open', 'Close', 'High', 'Low',
                                   'Volume', 'Signal_Cross', 'MA', 'Upper',
                                   'Lower', 'Capital', 'Shares', 'Return', 'Momentum'])
    boll = BollingerBands(w=20)  # 布林线
    order = stpl.StopLossOrder()

    capital = init_capital
    position = 0

    # 初始化资金曲线
    equity_curve = [capital]

    for i, new in enumerate(data_replay(data)):
        record.loc[i] = new
        signal, new['MA'], _, new['Upper'], new['Lower'] = boll.cal_inc(record)  # 布林线信号

        new['Signal_Cross'], capital, position = order(signal, new['Close'], capital, position)  # stop-loss order

        new['Capital'], new['Shares'] = capital, position
        # 更新资金曲线
        equity_curve.append(capital + position * new['Close'])
        record.loc[i] = new

        # if i == 0:
        #     print(record.dtypes)
        #     record.to_csv(os.path.join(PROJECT_ROOT + '/data/') + 'ma_stop_loss_test_online.csv')
        #     exit()

    # 计算动量指标
    record['Return'] = record['Close'].pct_change()
    record['Momentum'] = record['Return'].rolling(window=12).sum()

    record.to_csv(os.path.join(PROJECT_ROOT + '/data/') + 'ma_stop_loss_test_online.csv')

    # plt.plot(equity_curve)
    # plt.title('Equity Curve')
    # plt.xlabel('Date')
    # plt.ylabel('Equity')
    # plt.show()


if __name__ == '__main__':
    import os

    PROJECT_DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/')

    full_data = pd.read_csv(PROJECT_DATA_DIR + 'SH000300.csv')

    test_offline(full_data)
    # test_online(full_data)