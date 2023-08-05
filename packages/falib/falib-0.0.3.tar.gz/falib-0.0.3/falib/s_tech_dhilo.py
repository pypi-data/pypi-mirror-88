# -*- coding:utf-8 -*-
# @Time: 2020/11/10 20:49
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np

def cal(high, low, n):
    """
    波幅中位数 n周期内 最高价 - 最低价的中位数
    Parameters
    ----------
    high: Series
          股票最高价
    low: Series
         股票最低价
    n: int
       计算区间
    Returns
    pd.Series
    Examples
    -------


    """
    if isinstance(high, pd.Series) and isinstance(low, pd.Series) and isinstance(n, int):
        s_tech_dhilo = (high - low).rolling(window=n).median()
        return s_tech_dhilo

    else:
        raise ValueError('请输入正确格式的参数, high, low为Series, n为int')