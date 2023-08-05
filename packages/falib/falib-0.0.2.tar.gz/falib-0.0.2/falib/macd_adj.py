# -*- coding:utf-8 -*-
# @Time: 2020/11/10 13:30
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np
import talib


def cal(target, fastperiod_num=12, slowperiod_num=26, signalperiod_num=9):
    """
    计算目标值的macd 周期为默认参数(通常软件也是这么计算macd)
    Parameters
    ----------
    target: pd.Series
            目标值随意, 一般为close 或者 vol
    fastperiod_num: int
    slowperiod_num: int
    signalperiod_num: int
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
        20       NaN
        21       NaN
        22       NaN
        23       NaN
        24       NaN
        25       NaN
        26       NaN
        27       NaN
        28       NaN
        29       NaN
        30       NaN
        31       NaN
        32       NaN
        33    0.4401
        34    0.4021
        35    0.2905
        36    0.2528
        37    0.2170
        38    0.1888
        39    0.2596
        40    0.2528
        41    0.1691
        42    0.1549
        43    0.1360
        44    0.1225
        45    0.0938
        46   -0.0211
        47   -0.1290
        48   -0.2726
        49   -0.4023
        Name: x, dtype: float64
        -----------------------
    """
    if isinstance(target, pd.Series) and isinstance(fastperiod_num, int) and isinstance(slowperiod_num, int) and isinstance(signalperiod_num, int):
        macd = talib.MACD(target, fastperiod=fastperiod_num, slowperiod=slowperiod_num, signalperiod=signalperiod_num)[2] * 2
        return macd

    else:
        raise ValueError('请输入正确格式的参数, target为Series, 另外三个参数为int')
