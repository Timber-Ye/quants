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
    use_server_time=args.use_server_time
    flag=args.flag

    return api_key, secret_key, passphrase, use_server_time, flag


def trade(instId='BTC-USDT', side='buy', sz=1):
    # 三个参数，币种，买卖，数量
    per_info = get_personal_info()
    tradeAPI = Trade.TradeAPI(*per_info)
    print(*per_info,type(per_info[3]))
    result = tradeAPI.place_order(
        instId=instId, tdMode='cash', side=side, ordType='market', sz=sz)
    if result['code'] == '1':
        print('err:', result['msg'])
    elif result['code'] == '0':
        print('success '+side+' '+str(sz)+' '+instId)


def get_k(flag='1', instId='BTC-USDT', bar='15m'):
    # 获取k线图数据，可以根据返回结果进行k线图绘制
    marketDataAPI = MarketData.MarketAPI(flag=args.flag)
    result = marketDataAPI.get_history_candlesticks(instId=instId, bar=bar)
    df = pd.DataFrame(result['data'])
    k_data = df.iloc[:, 1:5]
    k_data.rename(columns={1: 'open', 2: 'high',
                  3: 'low', 4: 'price'}, inplace=True)
    return k_data


def get_balance( ccy='USDT'):
    # 获取账户USDT余额
    per_info = get_personal_info()
    accountAPI = Account.AccountAPI(*per_info)

    result = accountAPI.get_account_balance(ccy=ccy)
    for item in result['data']:
        for detail in item['details']:
            print(detail['ccy'], detail['cashBal'],
                  detail['availBal'])  # 显示币种，币种余额，可用余额


def ma_stoploss(k_data):
    position = 0
    pass    #现在需要判断读入数据是否是同一个时间的data，如果不同，则调用小面函数进行操作


def ma_sloss_step(k_data):
    global stop_loss,trailing_high,trailing_low,holding_period,position
    # 计算布林线
    k_data['MA20'] = k_data['price'].rolling(window=20).mean()
    k_data['std'] = k_data['price'].rolling(window=20).std()
    k_data['upper'] = k_data['MA20'] + 2 * k_data['std']
    k_data['lower'] = k_data['MA20'] - 2 * k_data['std']
    # 计算动量指标
    k_data['return'] = k_data['price'].pct_change()
    k_data['momentum'] = k_data['return'].rolling(window=12).sum()

    signal = 0
    end = len(k_data)-1
    if k_data['price'][end] > k_data['upper'][end-1]:
        signal = 1
    elif k_data['price'][end] < k_data['lower'][end-1]:
        signal = -1

    # 入场信号
    if (signal == 1) & (position == 0) & (holding_period == 0):
        return 1
    # 离场信号
    elif ((signal == -1) | (holding_period >= args.max_holding_period)) & (position != 0):
        return -1
    # 止损信号
    elif (k_data['price'][end] < stop_loss) & (position != 0):
        return -1
    # 移动止损信号
    elif (k_data['price'][end]>trailing_high)&(position!=0):
        trailing_high = k_data['price'][end]
        trailing_low = k_data['price'][end] * args.trailing_stop_multiplier
        stop_loss = trailing_low
    elif (k_data['price'][end] < trailing_low) & (position != 0):
        trailing_low = k_data['price'][end]
        trailing_high = k_data['price'][end] * args.trailing_stop_multiplier
        stop_loss = trailing_high

    # 更新持仓期
    if position != 0:
        holding_period += 1

    return 0

if __name__ == '__main__':
    # trade()
    # get_k()
    get_balance()