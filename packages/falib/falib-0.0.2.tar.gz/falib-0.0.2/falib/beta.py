# -*- coding:utf-8 -*-
# @Time: 2020/11/10 13:30
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(stock_close, index_close, n=20):
    """
    计算周期为n区间内的股票beta值
    Parameters
    ----------
    stock_close: Series
                 股票收盘价
    index_close: Series
                 指数收盘价
    n: int
       计算区间

    Returns
    ----------
    pd.Series
        个股n日beta
        Examples
    ----------
            0        NaN
            1        NaN
            2        NaN
            3        NaN
            4        NaN
            5        NaN
            6     0.0476
            7     0.5830
            8     0.5028
            9     0.5081
            10    1.3604
            11    0.8478
            12    0.8245
            13    0.2463
            14    0.4849
            Name: x, dtype: float64
            -----------------------
    """
    if isinstance(stock_close, pd.Series) and isinstance(index_close, pd.Series) & isinstance(n, int):
        df = pd.concat([stock_close, index_close], axis=1).reset_index(drop=True).copy()
        df.columns = ['x', 'y']
        df[df.columns[0]], df[df.columns[1]] = df[df.columns[0]].pct_change(1), df[df.columns[1]].pct_change(1)
        list_index = df.index.tolist()
        df['beta'] = [__get_beta(index_=index, df_=df.copy(), n_=n) for index in list_index]
    else:
        raise ValueError('传入的stock_close, index_close需为Series格式,n需为int格式')
    return df['beta']


def __get_beta(index_, df_, n_):
    if index_ - n_ < 0:
        return np.nan
    else:
        a = index_ - n_    # 不写ab的话后面全是nan 不知道为什么
        b = index_
        stk_ret = df_['x'][a: b]
        index_ret = df_['y'][a: b]
        beta = np.cov(stk_ret, index_ret)[0][1] / np.var(index_ret)
        return beta
