# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 18:46
# @Author  : 
# @File    : draw_figs.py
import mplfinance as mpf

# 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
my_color = mpf.make_marketcolors(up='r',
                                 down='g',
                                 edge='inherit',
                                 wick='inherit',
                                 volume='inherit')
# 设置图表的背景色
my_style = mpf.make_mpf_style(marketcolors=my_color,
                              figcolor='(0.82, 0.83, 0.85)',
                              gridcolor='(0.82, 0.83, 0.85)')


def K_candle_plot(data):
    """
    绘制K线图. 数据准备：

    df = pd.DataFrame(result['data'])

    k_data = df.iloc[:, 0:6].copy()

    k_data.rename(columns={0:'datetime', 1:'Open',2:'High',3:'Low',4:'Close', 5:'Volume'}, inplace=True)

    k_data['datetime'] = pd.DatetimeIndex(pd.to_datetime(k_data['datetime'], unit='ms')).tz_localize('UTC' ).tz_convert('Asia/Shanghai')

    k_data['datetime'] = pd.to_datetime(k_data['datetime'], format='%Y-%m-%d')

    k_data.set_index('datetime', inplace=True)

    k_data = k_data.astype({'Open': 'float',
                            'High': 'float',
                            'Low': 'float',
                            'Close': 'float',
                            'Volume': 'int'})
    """
    add_plot = [
        mpf.make_addplot(data, type='candle', panel=2)

    ]
    mpf.plot(data, type='candle',
                    mav=(2, 5),
                    addplot=add_plot,
                    volume=True,
                    figscale=1.5,
                    title='Candle', figratio=(5, 5), ylabel='price', ylabel_lower='volume',
                    )

    # plt.show()  # 显示


def K_candle_plot_MACD(data, volume=False):
    """
    绘制带有MACD指标的K线图. 数据准备：

    df = pd.DataFrame(result['data'])

    k_data = df.iloc[:, 0:6].copy()

    k_data.rename(columns={0:'datetime', 1:'Open',2:'High',3:'Low',4:'Close', 5:'Volume'}, inplace=True)

    k_data['datetime'] = pd.DatetimeIndex(pd.to_datetime(k_data['datetime'], unit='ms')).tz_localize('UTC' ).tz_convert('Asia/Shanghai')

    k_data['datetime'] = pd.to_datetime(k_data['datetime'], format='%Y-%m-%d')

    k_data.set_index('datetime', inplace=True)

    k_data = k_data.astype({'Open': 'float',
                            'High': 'float',
                            'Low': 'float',
                            'Close': 'float',
                            'Volume': 'int'})

    data['MACD'], data['Signal'], _ = talib.MACD(data['Close'].copy().values, fastperiod=12, slowperiod=26,
                                                 signalperiod=9)
    """
    histogram = data['MACD'] - data['Signal']
    histogram[histogram < 0] = None
    histogram_positive = histogram
    histogram = data['MACD'] - data['Signal']
    histogram[histogram >= 0] = None
    histogram_negative = histogram

    add_plot = [
        mpf.make_addplot(histogram_positive, type='bar', width=0.7, panel=2, color='b'),
        mpf.make_addplot(histogram_negative, type='bar', width=0.7, panel=2, color='fuchsia'),
        mpf.make_addplot(data['MACD'], panel=2, color='fuchsia', secondary_y=True),
        mpf.make_addplot(data['Signal'], panel=2, color='b', secondary_y=True),
    ]

    mpf.plot(data, type='candle',
                    addplot=add_plot,
                    volume=True,
                    figscale=1.5,
                    title='MACD', figratio=(5, 5), ylabel='price', ylabel_lower='volume',
                    main_panel=0, volume_panel=1,
                    )
    # plt.show()  # 显示



