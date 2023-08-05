# -*- coding:utf-8 -*-
# @Time: 2020/11/10 19:05
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(buy_lg_vol,  buy_elg_vol, sell_lg_vol, sell_elg_vol, vol):
    """
    大单流入率 (buy_lg_vol + buy_elg_vol - sell_lg_vol - sell_elg_vol) / vol
    Parameters
    ----------
    buy_lg_vol: pd.Series
                大单买入量
    buy_elg_vol: pd.Series
                特大单买入量
    sell_lg_vol: pd.Series
                大单卖出量
    sell_elg_vol: pd.Series
                 特大单卖出量
    vol: pd.Series
         成交量
    Returns
    -------
    pd.Series
        Examples
        --------
        0    0.0544
        1    0.1782
        2   -0.0486
        3   -0.1316
        4   -0.1852
        5   -0.0694
        6   -0.0621
        7    0.0774
        8   -0.0936
        9   -0.1230
        Name: x, dtype: float64
        -----------------------
    """
    if isinstance(buy_lg_vol, pd.Series) and isinstance(buy_elg_vol, pd.Series) and isinstance(sell_lg_vol, pd.Series) and isinstance(sell_elg_vol, pd.Series) and isinstance(vol, pd.Series):
        return (buy_lg_vol + buy_elg_vol - sell_lg_vol - sell_elg_vol) / vol
    else:
        raise ValueError('请输入正确格式的参数buy_lg_vol,  buy_elg_vol, sell_lg_vol, sell_elg_vol, vol均为Series')