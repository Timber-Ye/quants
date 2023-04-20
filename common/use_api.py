# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 11:53
# @Author  : 
# @File    : use_api.py


from enum import Enum


class Signal(Enum):
    Stay = 0
    Hold = 0

    # 入场
    Enter = 1
    ToBuy = 1

    # 离场
    Exit = -1
    ToSell = -1

    # 其他
    StopLoss = 2


def data_replay(data):
    """
    模拟实时
    :param data:
    :return:
    """
    for _i in range(len(data)):
        yield data.iloc[_i].to_dict()


class StreamingData:
    """
    {'Date', 'High', 'Low', 'Open', 'Close', 'Volume'}
    """
    def __init__(self, init_data):
        self.data = init_data.copy()
        self.num = len(self.data)

    def append(self, item):
        self.data.loc[self.num] = item
        self.num = self.num + 1

    def get_data(self):
        return self.data

    def get_close_price(self, num=1):
        if num is None or num > self.num:
            return self.data['Close'].copy().values
        else:
            return self.data['Close'].tail(num).copy().values


    def to_csv(self, dir):
        self.data.to_csv(dir)