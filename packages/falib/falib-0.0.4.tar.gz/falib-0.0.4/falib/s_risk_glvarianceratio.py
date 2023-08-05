# -*- coding:utf-8 -*-
# @Time: 2020/11/10 13:30
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(close, n, m=1):
    """
    计算n区间内的m区间的收益损失方差比
    Parameters
    ----------
    close: Series
           股票收盘价
    n: int
       计算收益损失方差比的区间
    m: int
       计算收益区间
    Returns
    -------
    pd.Series
        个股n个区间内的收益损失方差比
        Examples
    ----------
            0       NaN
            1       NaN
            2       NaN
            3       NaN
            4       NaN
            5    0.2793
            6    0.0218
            7    0.2518
            8    0.2928
            9    1.8181
            Name: x, dtype: float64
            -----------------------
    """
    if isinstance(close, pd.Series) and isinstance(m, int) & isinstance(n, int):
        close = close / close.shift(m) - 1
        close = close.rolling(n).apply(lambda ser: __get_s_risk_glvarianceratio20(ser_=ser))
        return close
    else:
        raise ValueError('传入的close需为Series格式,n, m需为int格式')


def __get_s_risk_glvarianceratio20(ser_):
    up_list = [x for x in ser_.tolist() if x > 0]
    down_list = [x for x in ser_.tolist() if x <= 0]
    if len(down_list) == 0 or len(up_list) == 0:
        return np.nan
    var_up = np.var(up_list)
    var_down = np.var(down_list)
    glvarianceratio20 = var_up / var_down
    return glvarianceratio20