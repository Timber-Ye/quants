# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 15:23
# @Author  : 
# @File    : boll_vanilla.py


# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 14:51
# @Author  :
# @File    : trix_vanilla.py


import os
import sys

import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(PROJECT_ROOT)

from trend_following.indicators import BollingerBands
import trend_following.vanilla_order as vnl
from common.use_api import data_replay
from common.config import get_cfg_defaults
from utils.cal_sharpe_ratio import cal_sharpe_ratio


def test_offline(config):
    data = pd.read_csv(config.SETUP.DATA_SOURCE)
    boll = BollingerBands(config.BOLL.WINDOW)  # 布林线

    data['Signal_Cross'], data['MA'], _, data['Upper'], data['Lower'] = boll.cal(data)

    order = vnl.Vanilla()
    capital = config.SETUP.INIT_CAPITAL
    position = 0

    data['Capital'] = 0.0
    data['Shares'] = 0.0
    data['Assets'] = 0.0

    equity_curve = [capital]
    price = 0

    for i in range(0, len(data)):
        price = data['Close'][i]
        signal = data['Signal_Cross'][i]

        capital, position = order(signal, price, capital, position)

        data.loc[i, 'Capital'] = capital
        data.loc[i, 'Shares'] = position

        # 更新资金曲线
        assets = capital + position * price
        equity_curve.append(capital)
        data.loc[i, 'Assets'] = assets

    # 计算动量指标
    data['Returns'] = data['Assets'].pct_change(1)
    data['Cumulative_Returns'] = (data['Returns']+1).cumprod()
    data['Sharpe'] = cal_sharpe_ratio(data, lookback_period=config.SHARPE.LOOKBACK_PERIOD)

    data.to_csv(os.path.join(PROJECT_ROOT + '/data/') + 'boll_vanilla_test_offline.csv')
    print("Outputs are saved to data/boll_vanilla_test_offline.csv")


def main():
    config = get_cfg_defaults()
    config.merge_from_file('configs/boll_vanilla.py')
    test_offline(config)


if __name__ == '__main__':

    main()
    # import os

    # PROJECT_DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/')

    # full_data = pd.read_csv(PROJECT_DATA_DIR + 'SH000300.csv')

    # final_equity = test_offline(full_data, init_capital=1e6)
    # final_equity = test_online(full_data, init_capital=1e6)

    # print('收益回报率：{}'.format((final_equity-1e6)/1e6))  # offline: 0.36772555140306495 online: 0.25921414485556027

