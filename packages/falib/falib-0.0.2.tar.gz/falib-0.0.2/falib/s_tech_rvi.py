# -*- coding:utf-8 -*-
# @Time: 2020/11/10 13:30
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(open, high, low, close, n):
    """
    相对离散指数(n期)
    Co=close-open;
    HL = high-low;
    V1=(co+2*ref(co,1)+2*ref(co,2)+ref(co,3))/6;
    V2=(HL+2*ref(HL,1)+2*ref(HL,2)+ref(HL,3))/6;
    S1=sum(V1,n/2)
    S2=sum(v2,n/2)
    RVI=S1/S2
    RVIS=( RVI+2*ref(RVI,1)+2*ref(RVI,2)+ref(RVI,3))/6;
    其中，ref表示引用以前的数据，sum表示累计和，n表示周期（基本设置n/2为１０），RVIS是RVI的信号线
    在计算时，先计算收盘价与开盘价的差值，最高价与最低价的差值，然后把它们分别求４天的加权平均，
    然后分别求它们一半周期的累计和，再把累计和相除。RVI的信号线就是RVI的４天的加权平均值。
    VALUE1 = ((CLOSE - OPEN) + 2 * (CLOSE (1)) – OPEN (1)) + 2*(CLOSE (2) – OPEN (2)) + (CLOSE (3) – OPEN (3))) / 6
    VALUE2 = ((HIGH - LOW) + 2 * (HIGH (1) – LOW (1)) + 2*(HIGH (2)- LOW (2)) + (HIGH (3) – LOW (3))) / 6
    NUM = SUM (VALUE1, N)
    DENUM = SUM (VALUE2, N)
    RVI = NUM / DENUM
    RVISig = (RVI + 2 * RVI (1) + 2 * RVI (2) + RVI (3)) / 6  这个暂时没求
    Parameters
    ----------
    open: Series
          开盘价

    high: Series
          最高价
    low: Series
          最低价
    close: Series
          收盘价
    n: int
       计算区间
    Returns
    --------
    pd.Series
          Examples
          -------
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
            12   -0.1670
            13   -0.2304
            14   -0.2575
            15   -0.2599
            16   -0.2489
            17   -0.2229
            18   -0.1821
            19   -0.1203
            Name: x, dtype: float64
            -----------------------
    """
    if isinstance(open, pd.Series) and isinstance(close, pd.Series) and isinstance(high, pd.Series) and isinstance(low, pd.Series) and isinstance(n, int):
        co = close - open
        hl = high - low
        v1 = (co + 2 * co.shift(1) + 2 * co.shift(2) + co.shift(3)) / 6
        v2 = (hl + 2 * hl.shift(1) + 2 * hl.shift(2) + hl.shift(3)) / 6
        s1 = v1.rolling(window=n).sum()
        s2 = v2.rolling(window=n).sum()
        rvi = s1 / s2
        return rvi
    else:
        raise ValueError('请输入正确的参数格式, close, high,low, open均为Series, n为int')









