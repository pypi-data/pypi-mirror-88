# -*- coding:utf-8 -*-
# @Time: 2020/11/10 13:30
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(stock_close, index_close, n, m=1):
    """
    计算n期内股票与指数m期收益率皮尔逊相关系数, m默认为1
    Parameters
    ----------
    stock_close：Series
                 股票收盘价
    index_close: Series
                 指数收盘价
    n: int
       计算皮尔逊系数区间
    m: 计算收益率区间 默认为1
    Returns
    -------
    pd.Series
        n周期内股票与指数的m日收益率的皮尔逊相关系数
        Examples
        ----------
            0       NaN
            1       NaN
            2       NaN
            3       NaN
            4       NaN
            5       NaN
            6    0.0467
            7    0.4038
            8    0.4725
            9    0.4891
            Name: x, dtype: float64
            -----------------------
    """
    if isinstance(stock_close, pd.Series) and isinstance(index_close, pd.Series) and isinstance(m, int) & isinstance(n, int):
        if len(stock_close) != len(index_close):
            raise Exception('请对齐股票与指数日期, 最好检查股票期间是否有停牌日, 如果有停牌最好按指数日期左对齐merge之后再进该函数')
        list_test = list(range(len(stock_close)))
        stock_close = stock_close / stock_close.shift(m) - 1
        index_close = index_close / index_close.shift(m) - 1
        pearson_cor = [__correlation(index_ret=index_close, stock_ret=stock_close, index_=index, period=n) for index in list_test]
        pearson_cor = pd.Series(pearson_cor)
    else:
        raise ValueError('传入的stock_close, index_close需为Series格式,n, m需为int格式')
    return pearson_cor


def __correlation(index_ret,  stock_ret, index_, period):
    if index_ - period <= 0:
        return np.nan
    a = index_
    b = index_ - period
    x = stock_ret[b: a]
    y = index_ret[b: a]
    meanX = x.mean()
    deviationX = x.std(ddof=0)
    stardardizedX = (x - meanX) / deviationX
    meanY = y.mean()
    deviationY = y.std(ddof=0)
    stardardizedY = (y - meanY) / deviationY
    return (stardardizedX * stardardizedY).mean()