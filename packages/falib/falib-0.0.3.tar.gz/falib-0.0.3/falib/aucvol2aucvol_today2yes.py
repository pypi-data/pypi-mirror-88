# _*_coding:utf-8_*_
# @Time: 2020/11/9 8:47
# @Author: zhang chenyong
# @File: aucvol2aucvol_today2yes.py

import pandas as pd


def cal(auc_vol):
    """
    今日竞价量对昨日竞价量的比值
    Parameters
    ----------
    auc_vol : Series  竞价成交量

    Returns
    -------
    Series   ref0_aucvol2aucvol_today2yes

            Examples
    ______________________________________________
    0          NaN
    1     0.258222
    2     0.132075
    3    15.857143
    4     0.076577
    5     1.764706
    Name: cum_volume, dtype: float64
    ______________________________________________

    """

    assert isinstance(auc_vol, pd.Series)
    ref0_aucvol2aucvol_today2yes = auc_vol / auc_vol.shift(1)
    return ref0_aucvol2aucvol_today2yes


if __name__ == '__main__':
    from qytools.db_read import DBReader

    db_read = DBReader()
    data = db_read.read_aucvol_data(start=20201022, end=20201029, code=603306, fields='code,date,cum_volume')
    auv_vol = data['cum_volume']
    print(cal(auv_vol))