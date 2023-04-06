# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 19:10
# @Author  : 
# @File    : trix2.py.py

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 11:04:17 2023

@author: weixh
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from trix import trix
from macd import macd

# 读取数据
df = pd.read_csv("C:/weixh/HFData/SH000300.csv")
data.rename(columns={"Close": "close"}, inplace=True) # 将"Close"列改为"close"

# 计算Trix和Signal
df["trix"] = trix(df["close"], n=18)
df["signal"] = trix(df["close"], n=18).ewm(span=9).mean()

# 计算Trix和Signal的差值
df["diff"] = df["trix"] - df["signal"]

# 计算Macd和Signal
df["macd"], df["signal_macd"], _ = macd(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)

# 计算交易信号
df["trix_buy_signal"] = np.where(df["diff"] > 0, 1, 0)
df["trix_sell_signal"] = np.where(df["diff"] < 0, 1, 0)
df["macd_buy_signal"] = np.where(df["macd"] > df["signal_macd"], 1, 0)
df["macd_sell_signal"] = np.where(df["macd"] < df["signal_macd"], 1, 0)

# 计算每天的收益率
df["return"] = df["close"].pct_change()

# 设置初始资金
capital = 1000000

# 初始化持仓标记
position = 0

# 记录每天的资金曲线
capital_curve = [capital]

# 记录买入/卖出的日期和价格
buy_dates = []
buy_prices = []
sell_dates = []
sell_prices = []

# 遍历每一天的数据
for i in range(len(df)):
    # 计算当天的交易信号
    trix_buy_signal_today = df["trix_buy_signal"].iloc[i]
    trix_sell_signal_today = df["trix_sell_signal"].iloc[i]
    macd_buy_signal_today = df["macd_buy_signal"].iloc[i]
    macd_sell_signal_today = df["macd_sell_signal"].iloc[i]

    # 如果有买入信号
    if trix_buy_signal_today == 1 and macd_buy_signal_today == 1 and position == 0:
        # 计算可用资金和购买数量
        available_capital = capital
        buy_price = df["close"].iloc[i]
        buy_quantity = available_capital // buy_price

        # 计算剩余资金和持仓
        remaining_capital = available_capital - buy_quantity * buy_price
        position = buy_quantity

        # 记录买入的日期和价格
        buy_dates.append(df.index[i])
        buy_prices.append(buy_price)

    # 如果有卖出信号
    elif trix_sell_signal_today == 1 and macd_sell_signal_today == 1 and position > 0:
        # 计算可获得的资金和卖出数量
        sell_price = df["close"].iloc[i]
        sell_quantity = position

        # 计算剩余资金和持仓
        remaining_capital = capital + sell_quantity * sell_price
        position = 0

        #