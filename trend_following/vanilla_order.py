# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 14:44
# @Author  : 
# @File    : vanilla_order.py

import os
import sys

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(PROJECT_ROOT)

from common.use_api import Signal


def vanilla_order(signal, price, capital, position):
    new_cap = capital
    new_pos = position

    if signal == Signal.ToBuy:
        new_pos = capital / price
        new_cap = 0
    elif signal == Signal.ToSell:
        new_cap = position * price
        new_pos = 0

    return new_cap, new_pos

