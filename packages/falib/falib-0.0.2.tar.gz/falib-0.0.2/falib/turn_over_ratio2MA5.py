# _*_coding:utf-8_*_
# @Time: 2020/11/8 21:35
# @Author: zhang chenyong
# @File: turn_over_ratio2MA5.py


import pandas as pd


def cal(turn_over_rate, MA=5):
    """
     计算换手率五日偏差： 换手率与五日换手率均值的比值
    Parameters
    ----------
    turn_over_rate : Series  换手率 (传入有时间顺序的换手率序列)
        Examples

            0     1.3995
            1     1.6192
            2     1.0316
            3     0.6638
            4     0.8834
            5     1.0744
            6     1.3549
            7     1.2594
            8     2.3724
            9     2.3801
            10    1.6741
            Name: turnover_rate, dtype: float64
        ______________________________

    MA : int  几日偏差

    Returns
    -------
    Series  ref1_turn_over_ratio2MA5
        Examples
            0          NaN
            1          NaN
            2          NaN
            3          NaN
            4     0.789102
            5     1.018891
            6     1.352709
            7     1.202659
            8     1.708114
            9     1.409811
            10    0.925848
            Name: ref1_turn_over_ratio2MA5, dtype: float64
        ______________________________

    """

    assert isinstance(turn_over_rate, pd.Series)
    assert isinstance(MA, int)

    if len(turn_over_rate) < MA + 1:
        raise ValueError('传入的换手率数据不够')
    df = pd.DataFrame()
    df['turn_over_rate'] = turn_over_rate
    df['turn_over_rate_MA'] = turn_over_rate.rolling(MA).mean()
    df['ref1_turn_over_ratio2MA5'] = df['turn_over_rate'] / df['turn_over_rate_MA']
    ref1_turn_over_ratio2MA5 = df['ref1_turn_over_ratio2MA5']
    return ref1_turn_over_ratio2MA5


if __name__ == '__main__':
    from qytools.db_read import DBReader

    db_read = DBReader()
    data = db_read.read_ts_day_data(
                                    start=20201022,
                                    end=20201106,
                                    code=603306,
                                    fields='code,date,turnover_rate'
                                    )
    turn_over_rate = data['turnover_rate']
    cal(turn_over_rate)


