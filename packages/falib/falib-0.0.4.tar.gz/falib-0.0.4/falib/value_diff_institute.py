# -*- coding:utf-8 -*-
# @Time: 2020/11/10 19:05
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(buy_elg_amount, sell_elg_amount):
    """
    机构金额差 buy_elg_amount - sell_elg_amount
    Parameters
    ----------
    buy_elg_amount: pd.Series
                    特大单买入金额
    sell_elg_amount: pd.Series
                    特大单卖出金额
    Returns
    -------
        pd.Series
        Examples
        --------
            0   -21122.18
            1   -33742.42
            2    -2165.09
            3     6412.60
            4    -3999.69
            5    -4694.99
            6     8225.93
            7   -21593.76
            8   -27117.57
            9    -2200.52
            Name: x, dtype: float64
            -----------------------
    """
    if isinstance(buy_elg_amount, pd.Series) and isinstance(sell_elg_amount, pd.Series):
        return buy_elg_amount - sell_elg_amount
    else:
        raise ValueError('请输入格式正确的参数, buy_elg_amount, sell_elg_amount均为Series')
