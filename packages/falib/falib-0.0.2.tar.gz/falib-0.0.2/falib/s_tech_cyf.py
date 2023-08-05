# -*- coding:utf-8 -*-
# @Time: 2020/11/10 13:30
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np
import talib


def cal(turnover_rate, n=20):
    """
    市场能量指标 = 100 - 100/(1 + EMA(turnover_rate))  默认换手率均线参数为20个周期
    Parameters
    ----------
    turnover_rate: Series
                   股票换手率
    n: int
       换手率均线指标
    Returns
    -------
    pd.Series
        Examples
        --------
            0         NaN
            1         NaN
            2         NaN
            3         NaN
            4         NaN
            5         NaN
            6         NaN
            7         NaN
            8         NaN
            9     33.4137
            10    33.6386
            11    32.0404
            12    31.3022
            13    31.3567
            14    30.6110
            15    31.6963
            16    37.1603
            17    39.1611
            18    39.9897
            19    39.6255
            Name: x, dtype: float64
            -----------------------
    """
    if isinstance(turnover_rate, pd.Series) and isinstance(n, int):
        EMA_ = pd.Series(talib.EMA((turnover_rate), timeperiod=n), name='EMA')
        CYF = 100 - 100 / (1 + EMA_)
        return CYF
    else:
        raise ValueError('请输入正确格式的参数, vol, flo_share为')
