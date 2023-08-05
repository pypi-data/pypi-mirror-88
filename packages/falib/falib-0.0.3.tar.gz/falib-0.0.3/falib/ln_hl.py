# -*- coding:utf-8 -*-
# @Time: 2020/11/10 13:30
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(high, low, n=20):
    """
    二十日最高价 / 二十日最低价 取对数
    Parameters
    ----------
    high: pd.Series
          股票最高价
    low: pd.Series
         股票最低价
    n: int
       计算区间

    Returns
    -------
    pd.Series
        Examples
        --------
        0        NaN
        1        NaN
        2        NaN
        3        NaN
        4        NaN
        5        NaN
        6        NaN
        7        NaN
        8        NaN
        9        NaN
        10       NaN
        11       NaN
        12       NaN
        13       NaN
        14       NaN
        15       NaN
        16       NaN
        17       NaN
        18       NaN
        19    0.0227
        20    0.0227
        21    0.0227
        22    0.0193
        23    0.0300
        24    0.0300
        25    0.0300
        26    0.0300
        27    0.0300
        28    0.0246
        29    0.0158
        Name: x, dtype: float64
        -----------------------
    """
    if isinstance(high, pd.Series) and isinstance(low, pd.Series) and isinstance(n, int):
        high = high.rolling(window=n).max()
        low = low.rolling(window=n).max()
        ln_lh = (high / low).apply(np.log)
        ln_lh[np.isinf(ln_lh)] = np.nan
        return ln_lh
    else:
        raise ValueError('请输入格式正确的参数, high, low为Series, n为int')