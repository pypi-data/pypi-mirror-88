# -*- coding:utf-8 -*-
# @Time: 2020/11/10 13:30
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(vol, close, n):
    """
    当前交易量相比过去一段时期平均交易量 * 过去一段时期的累积收益率乘积
    Parameters
    ----------
    vol: pd.Series
         成交量
    close: pd.Series
           收盘价
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
        19       NaN
        20   -0.1182
        21   -0.1981
        22   -0.1737
        23   -0.1352
        24   -0.1104
        25   -0.1401
        26   -0.1035
        27   -0.0866
        28   -0.0682
        29   -0.0589
        Name: x, dtype: float64
        -----------------------
    """
    if isinstance(vol, pd.Series) and isinstance(close, pd.Series) and isinstance(n, int):
        cum_ret = close / close.shift(n) - 1
        s_tech_vol = (vol / vol.rolling(n).mean()) * cum_ret
        return s_tech_vol
    else:
        raise ValueError('请输入正确格式的参数, close, vol为Series, n为int')