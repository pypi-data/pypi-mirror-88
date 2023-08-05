# -*- coding:utf-8 -*-
# @Time: 2020/11/10 19:05
# @Author: caiyucheng
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(data, n):
    """
    1 - 过去n个周期的累积收益率排名 / 股票总数
    Parameters
    ----------
    data: pd.DataFrame
          包含close的dataframe
    n: int
       计算区间
    Returns
    -------
    pd.DataFrame
    返回的data中较原data新增一列s_tech_rank表示股票n个周期累积收益率的倒数排名(取倒数是因为正向因子)
        Examples
        --------
            code        date  adj_factor  ...         vol  volume_ratio  s_tech_rank
            0            1  2020-01-02     109.169  ...  1.5302e+06          2.18          NaN
            1            1  2020-01-03     109.169  ...  1.1162e+06          1.21          NaN
            2            1  2020-01-06     109.169  ...  8.6208e+05          0.80          NaN
            3            1  2020-01-07     109.169  ...  7.2861e+05          0.70          NaN
            4            1  2020-01-08     109.169  ...  8.4782e+05          0.86          NaN
            ...         ...         ...  ...         ...           ...          ...
            127530  603999  2020-02-24       2.444  ...  1.5450e+05          1.06       0.6571
            127531  603999  2020-02-25       2.444  ...  1.7454e+05          1.16       0.4700
            127532  603999  2020-02-26       2.444  ...  1.1746e+05          0.75       0.3190
            127533  603999  2020-02-27       2.444  ...  8.0846e+04          0.52       0.1376
            127534  603999  2020-02-28       2.444  ...  1.3784e+05          0.98       0.0759
            [127535 rows x 42 columns]
            ----------------------------------------------------------------------------------
    """
    if isinstance(data, pd.DataFrame):
        if 'close' and 'code' and 'date' not in data.columns.tolist():
            raise Exception('输入的data中必须有code、close、date')
        data_test = data[['date', 'code', 'close']].copy().pivot_table(index='date', columns='code', values='close').pct_change(periods=n).T.rank(method='first')
        # data_test = data_test.pct_change(periods=n).T.rank(method='first')
        len_data, col_, index_ = len(data_test), data_test.columns.tolist(), data_test.index.tolist()
        data_test = pd.DataFrame(np.array(data_test) / len_data, index=index_, columns=col_).stack().reset_index()
        data_test.columns = ['code', 'date', 's_tech_rank']
        data = pd.merge(data, data_test, how='left', on=['code', 'date'])
        return data

    else:
        raise ValueError('请输入格式正确的参数')
