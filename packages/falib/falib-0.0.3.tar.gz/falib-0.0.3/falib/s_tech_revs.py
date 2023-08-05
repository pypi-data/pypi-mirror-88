# -*- coding:utf-8 -*-
# @Time: 2020/11/10 13:30
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(close, n, m):
    """
    计算股票n期累积收益率与m期累积收益率的差(价格动量差), 一般来说用 短期收益率-长期收益率 所以最好 n > m
    Parameters
    ----------
    close: Series
           股票收盘价
    n: int
       n期累计收益率
    m: int
       m期累计收益率
    Returns
    -------
    pd.Series
    股票n期累积收益率与m期累积收益率的差
    Examples
    -----------
        0       NaN
        1       NaN
        2       NaN
        3       NaN
        4       NaN
        5   -0.0162
        6    0.0303
        7    0.0166
        8    0.0269
        9   -0.0193
        Name: x, dtype: float64
        -----------------------
    """
    if isinstance(close, pd.Series) and isinstance(n, int) and isinstance(m, int):
        close_n = close / close.shift(n) - 1
        close_m = close / close.shift(m) - 1
        return close_n - close_m
    else:
        raise ValueError('请输入参数的正确格式, close为Series, n, m为int')