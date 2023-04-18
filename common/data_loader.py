# python common/data_loader.py
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 14:03
# @Author  : 
# @File    : data_loader.py


import okx.Account as Account
import okx.MarketData as MarketData
import pandas as pd
import numpy as np


def data_loader(bar):
    flag = "1"  # live trading:0 , demo trading: 1
    marketDataAPI = MarketData.MarketAPI(flag=flag)
    result = marketDataAPI.get_history_candlesticks(instId='BTC-USD-SWAP', bar=bar, limit=100)
    df = pd.DataFrame(result['data'])
    k_data = df.iloc[:, 0:6].copy()
    k_data.rename(columns={0: 'Datetime', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'}, inplace=True)

    k_data['Datetime'] = pd.DatetimeIndex(pd.to_datetime(k_data['Datetime'], unit='ms')).tz_localize('UTC').tz_convert('Asia/Shanghai')
    k_data['Datetime'] = pd.to_datetime(k_data['Datetime'], format='%Y-%m-%d %H:%M')
    k_data.set_index('Datetime', inplace=True)
    k_data = k_data.astype({'Open': 'float',
                            'High': 'float',
                            'Low': 'float',
                            'Close': 'float',
                            'Volume': 'int'})

    return k_data


if __name__ == '__main__':
    import os
    import sys

    PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
    sys.path.append(PROJECT_ROOT)
    print("pwd: {}".format(PROJECT_ROOT))

    from utils.draw_figs import K_candle_plot

    bar = '1W'
    data = data_loader(bar)
    SAVE_DIR = os.path.join(PROJECT_ROOT, 'data/')
    FILE_NAME = "BTC-USD-SWAP-Bar-" + bar
    data.to_csv(SAVE_DIR + FILE_NAME + '.csv')

    K_candle_plot(data, title='Mark Price Candlesticks (time bar: ' + bar + ')',
                  # save_dir=SAVE_DIR + FILE_NAME+'.pdf'
                  )
