# -*- coding:utf-8 -*-
# @Time: 2020/11/10 19:05
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(buy_lg_amount, buy_elg_amount, amount):
    """
    大单买入成交金额 / 总成交金额
    Parameters
    ----------
    buy_lg_amount: pd.Series
                   大单买入额
    buy_elg_amount: pd.Series
                特大单买入额
    amount: pd.Series
            成交金额
    Returns
    -------
    pd.Series
        Examples
        --------
        0    0.0704
        1    0.0703
        2    0.0568
        3    0.0428
        4    0.0487
        5    0.0611
        6    0.0479
        7    0.0662
        8    0.0605
        9    0.0477
        Name: x, dtype: float64
        -----------------------
    """
    if isinstance(buy_lg_amount, pd.Series) and isinstance(buy_elg_amount, pd.Series) and isinstance(amount, pd.Series):
        return (buy_elg_amount + buy_lg_amount) / amount

    else:
        raise ValueError('请输入格式正确的参数, buy_lg_amount, buy_elg_amount, amount均为Series')