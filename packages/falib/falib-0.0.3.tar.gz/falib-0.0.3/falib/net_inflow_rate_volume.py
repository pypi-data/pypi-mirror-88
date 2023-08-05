# -*- coding:utf-8 -*-
# @Time: 2020/11/10 19:05
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(net_mf_vol, vol):
    """
    流入率 net_mf_vol / vol
    Parameters
    ----------
    net_mf_vol: pd.Series
                净流入量
    vol: pd.Series
        成交量
    Returns
    -------
    pd.Series
        Examples
        --------
            0    0.3113
            1    0.2635
            2    0.2766
            3    0.2398
            4    0.2290
            5    0.2919
            6    0.2817
            7    0.2575
            8    0.2411
            9    0.2305
            Name: x, dtype: float64
            -----------------------
    """
    if isinstance(net_mf_vol, pd.Series) and isinstance(vol, pd.Series):
        return net_mf_vol / vol
    else:
        raise ValueError('请输入格式正确的参数, net_mf_vol, vol均为Series')
