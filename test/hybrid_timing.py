# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 11:27
# @Author  : 
# @File    : hybrid_timing.py


import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(PROJECT_ROOT)

from trend_following.indicators import MACD, TRIX, BollingerBands
from trend_following import hybrid_order as hbo

from common.use_api import Signal
from common.config import get_cfg_defaults
from utils.cal_sharpe_ratio import cal_sharpe_ratio


def test_offline(config):
    data = pd.read_csv(config.SETUP.DATA_SOURCE)

    macd = MACD(config.MACD.FAST_PERIOD, config.MACD.SLOW_PERIOD, config.MACD.SIGNAL_PERIOD)
    trix = TRIX(config.TRIX.TIME_PERIOD, config.TRIX.BUY_THRESHOLD, config.TRIX.SELL_THRESHOLD)
    boll = BollingerBands(config.BOLL.WINDOW)

    data['MACD'], _, _ = macd.cal(data)
    data['TRIX'], _, _ = trix.cal(data)
    data['Bollinger'], _, _, _, _ = boll.cal(data)

    capital = config.SETUP.INIT_CAPITAL
    position = 0
    funding = 0 
    lever = 0
    data['Capital'] = capital
    data['Shares'] = 0.0
    data['Assets'] = capital
    # 初始化资金曲线
    equity_curve = [capital]

    data['Action'] = Signal.Stay

    for i in range(0, len(data)):
        price = data['Close'][i]
        signal_macd = data['MACD'][i]
        signal_trix = data['TRIX'][i]
        signal_boll = data['Bollinger'][i]

        data.loc[i, 'Action'], capital, position,funding ,lever= hbo.hybrid_strategy(signal_macd, signal_trix, signal_boll, price,
                                                                       capital, position, funding,lever,config)

        # 更新资金曲线
        equity = capital + position * price - funding
        equity_curve.append(equity)

        data.loc[i, 'Assets'] = equity
        data.loc[i, 'Capital'] = capital
        data.loc[i, 'Shares'] = position
    data['Returns'] = data['Assets'].pct_change(1)
    data['Cumulative_Returns'] = (data['Returns']+1).cumprod()
    data['Sharpe'] = cal_sharpe_ratio(data, lookback_period=len(data)-1,risk_free_rate=0.015)
    #计算最大回撤 
    # 计算每日最高累积收益
    data['max_cum_returns'] = data['Cumulative_Returns'].cummax()
    # 计算每日回撤
    data['drawdown'] = data['Cumulative_Returns'] - data['max_cum_returns']
    # 计算最大回撤
    max_drawdown = data['drawdown'].min()
    #计算年化收益率
    annual_return = data['Returns'].mean() * 250
    print("max_drawdown:",max_drawdown)
    print("annual_return=",annual_return)
    data.to_csv(os.path.join(PROJECT_ROOT + '/data/') + 'hybrid_timing_test_offline.csv')
    print("Outputs are saved to data/hybrid_timing_test_offline.csv")

    plt.plot(equity_curve)
    plt.title('Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Equity')
    plt.show()


def main():
    config = get_cfg_defaults()
    config.merge_from_file('configs/hybrid_timing.py')
    test_offline(config)


if __name__ == '__main__':
    main()