# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 10:14
# @Author  : hanchiao
# @File    : cal_sharpe_ratio.py
import numpy as np


# 计算滚动夏普率
def rolling_sharpe_ratio(returns, window):
    return np.sqrt(window) * returns.rolling(window).mean() / returns.rolling(window).std()


def cal_sharpe_ratio(data, lookback_period=60, risk_free_rate=0.015):
    """
    Basic knowledge: https://www.investopedia.com/terms/s/sharperatio.asp
    :param data: 包含“Assets”字段
    :param lookback_period: 计算夏普率的回溯期
    :param risk_free_rate: 每个交易日的风险目标（无风险收益）
    :return: 夏普率序列
    """

    # 计算日收益率
    daily_return = data['Assets'].pct_change()


    sharpe_ratio = [0.0] * lookback_period

    # 循环计算每个交易日的信号和风险权重
    for i in range( lookback_period,len(data)):
        # 计算过去回溯期的收益率和标准差，计算夏普率
        returns = daily_return.iloc[i-lookback_period :i]
        mean_return = returns.mean()
        std_return = returns.std()

        if 1e-6 > std_return > -1e-6:
            sharpe_ratio.append(float('-inf'))
        else:
            sharpe_ratio.append((mean_return*252 - risk_free_rate) / (std_return * np.sqrt(252)))  # assuming 252 trading days per year

    return sharpe_ratio

