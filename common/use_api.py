# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 11:53
# @Author  : 
# @File    : use_api.py

import okx.Account as Account
import okx.MarketData as MarketData
import okx.Funding as Funding
import okx.Trade as Trade
import pandas as pd
import numpy as np
from config import args


def get_personal_info():
    api_key = args.api_key
    secret_key = args.secret_key
    passphrase = args.passphrase
    Permissions = args.Permissions
    use_server_time = args.use_server_time
    flag = args.flag

    return api_key, secret_key, passphrase, use_server_time, flag


def trade(side='buy', sz=1000):
    # 三个参数，币种，买卖，数量
    per_info = get_personal_info()
    tradeAPI = Trade.TradeAPI(*per_info)
    print(*per_info, type(per_info[3]))
    result = tradeAPI.place_order(
        instId=args.instId, tdMode='cash', side=side, ordType='market', sz=sz)
    if result['code'] == '1':
        print(result)
        print('err:', result['msg'])
    elif result['code'] == '0':
        print('success '+side+' '+str(sz)+' '+args.instId)


def get_k():
    # 获取k线图数据，可以根据返回结果进行k线图绘制
    marketDataAPI = MarketData.MarketAPI(flag=args.flag)
    result = marketDataAPI.get_history_candlesticks(
        instId=args.instId, bar=args.bar)
    df = pd.DataFrame(result['data'])
    k_data = df.iloc[:, 1:5]
    k_data.rename(columns={1: 'open', 2: 'high',
                  3: 'low', 4: 'price'}, inplace=True)

    k_data = k_data.astype({"open": 'float32', "high": 'float32',
                           'low': 'float32', 'price': 'float32'})  # 转换数据类型
    return k_data


def get_balance(ccy):
    # 获取账户USDT余额
    per_info = get_personal_info()
    accountAPI = Account.AccountAPI(*per_info)

    result = accountAPI.get_account_balance(ccy=ccy)
    for item in result['data']:
        for detail in item['details']:
            # 显示币种，币种余额，可用余额
            yield (detail['ccy'], float(detail['cashBal']), float(detail['availBal']))

# 这个买币和卖币的代码还要改，这个是两个币种之间的交易，逻辑是乱的，后面可能要再改一下


def buy_coin():
    for coin_name, coin_rest, avl_rest in get_balance(ccy=args.ccy_buy):
        trade(side='buy', sz=avl_rest/2)


def sell_coin():
    for coin_name, coin_rest, avl_rest in get_balance(ccy=args.ccy_sell):
        print(coin_name, avl_rest/2)
        trade(side='sell', sz=avl_rest)


def ma_stoploss():
    mean_now = pd.Series([0, 0, 0, 0], dtype='float32',index=['open','high','low','price'])
    while True:
        k_data = get_k()
        mean_tmp = k_data.mean(axis=0)
        if (mean_now-mean_tmp).pow(2).sum() > 1e-3:
            mean_now = mean_tmp
            sell_flag=ma_sloss_step(k_data=k_data)
            print("买入信号为: ",sell_flag)
            if sell_flag==1:
                buy_coin()
            elif sell_flag==-1:
                sell_coin()
            else:
                print('不进行操作')


def ma_sloss_step(k_data):
    stop_loss = 0
    trailing_high = 0
    trailing_low = 0
    holding_period = 0
    position = 0
    # 计算布林线
    k_data['MA20'] = k_data['price'].rolling(window=20).mean()
    k_data['std'] = k_data['price'].rolling(window=20).std()
    k_data['upper'] = k_data['MA20'] + 2 * k_data['std']
    k_data['lower'] = k_data['MA20'] - 2 * k_data['std']

    # 计算动量指标
    k_data['return'] = k_data['price'].pct_change()
    k_data['momentum'] = k_data['return'].rolling(window=12).sum()

    # 初始化信号
    k_data['signal'] = 0

    sell_flag=0

    # 计算信号
    for i in range(1, len(k_data)):
        sell_flag=0
        # 布林线信号
        if k_data['price'][i] > k_data['upper'][i - 1]:
            k_data['signal'][i] = 1
        elif k_data['price'][i] < k_data['lower'][i - 1]:
            k_data['signal'][i] = -1

        # 入场信号
        if (k_data['signal'][i] == 1) & (position == 0) & (holding_period == 0):
            sell_flag=1

        # 离场信号
        elif ((k_data['signal'][i] == -1) | (holding_period >= args.max_holding_period)) & (position != 0):
            sell_flag=-1

        # 止损信号
        elif (k_data['price'][i] < stop_loss) & (position != 0):
            sell_flag=-1

        # 移动止损信号
        elif (k_data['price'][i] > trailing_high) & (position != 0):
            trailing_high = k_data['price'][i]
            trailing_low = k_data['price'][i] * args.trailing_stop_multiplier
            stop_loss = trailing_low

        elif (k_data['price'][i] < trailing_low) & (position != 0):
            trailing_low = k_data['price'][i]
            trailing_high = k_data['price'][i] * args.trailing_stop_multiplier
            stop_loss = trailing_high

        # 更新持仓期
        if position != 0:
            holding_period += 1

    return sell_flag

if __name__ == '__main__':
    # trade(side='buy',sz=1000)
    # trade(side='sell',sz=1.034)
    # get_k()
    # for i in get_balance():
    #     print(i)
    ma_stoploss()

    # buy_coin()
    # sell_coin()
