import okx.MarketData as MarketData

flag = "1" # live trading:0 , demo trading: 1
marketDataAPI = MarketData.MarketAPI (flag=flag)
result = marketDataAPI.get_tickers(instType="SPOT")
print(result)