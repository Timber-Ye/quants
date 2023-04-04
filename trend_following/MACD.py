# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 19:19
# @Author  : 
# @File    : MACD.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib

# 读取数据
data = pd.read_csv('data/SH000300.csv')
data.rename(columns={'Close': 'close', 'trade_dt': 'date'}, inplace=True)

# 计算 MACD
data['MACD'], data['Signal'], _ = talib.MACD(data['close'].copy().values, fastperiod=12, slowperiod=26, signalperiod=9)
# print(data['MACD'])

# plt.figure(1)
# data['MACD'].plot()
# data['Signal'].plot()

# 计算择时信号
data['Signal_Cross'] = 0  # Signal-line crossover
for i in range(1, len(data)):
    if data['MACD'][i] > data['Signal'][i] and data['MACD'][i-1] < data['Signal'][i-1]:  # the MACD line crosses up
        # through the average line
        data['Signal_Cross'][i] = 1  # to buy
        # print(i,'signal 1')
    elif data['MACD'][i] < data['Signal'][i] and data['MACD'][i-1] > data['Signal'][i-1]:  # crosses down
        data['Signal_Cross'][i] = -1  # to sell
        # print(i,'signal -1')

data['Signal_Cross'][1] = 1  # the first day all in
# 计算收益率和资金曲线
capital = 1000000.0  # 起始资金
data['Shares'] = 0.0
data['Capital'] = 0.0
for i in range(1, len(data)):
    if data['Signal_Cross'][i] == 1:  # to buy
        # data['Shares'][i] = capital / data['close'][i-1]
        data['Shares'][i] = capital / data['close'][i]
        capital = 0  # all in
    elif data['Signal_Cross'][i] == -1:  # to sell
        capital = data['close'][i] * data['Shares'][i-1]
        data['Shares'][i] = 0  # sell out
    else:
        data['Shares'][i] = data['Shares'][i-1]
    data['Capital'][i] = capital  # remains

data['Returns'] = np.log(data['close'] / data['close'].shift(1))
data['Cumulative_Returns'] = data['Returns'].cumsum()

plt.figure(2)
data['Cumulative_Returns'].plot()
plt.show()

print(capital/1000000.0)
# print(data['Cumulative_Returns'])