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
    Leverage = 2
    # 离场
    Exit = -1
    ToSell = -1

    # 其他
    StopLoss = 2
    Put=-2

def data_replay(data):
    """
    模拟实时
    :param data:
    :return:
    """
    for _i in range(len(data)):
        yield data.iloc[_i].to_dict()

if __name__=="__main__":
    print(Signal.Enter.value)