# _*_coding:utf-8_*_
# @Time: 2020/11/8 21:19
# @Author: zhang chenyong
# @File: riseover_amount.py


import pandas as pd


def cal(low, amount, up_limit):
    """
    板上成交额因子： 分钟最低价等于涨停价的分钟成交额的总量

    Parameters
    ----------
    low：pd.Series    分钟最低价
        Examples:

                0      8.23
                1      8.24
                2      8.28
                3      8.27
                4      8.44
                       ...
                235    9.03
                236    9.03
                237    9.03
                238    9.03
                239    9.03
                Name: low, Length: 240, dtype: float64
            ______________________________
    amount： pd.Series     分钟成交额

        Examples

                0      13567572.00
                1       2488528.00
                2       3892867.00
                3       4631776.00
                4       5022798.00
                          ...
                235      200466.00
                236       59598.00
                237           0.00
                238           0.00
                239      701631.06
                Name: amount, Length: 240, dtype: float64
            ______________________________
    up_limit： Series  当日股票涨停价

        Examples:

                0    9.03
                Name: up_limit, dtype: float64
            ______________________________
            Returns
    -------
        int类型   ref1_riseover_amount
    """

    # 判断传入分钟最高价和分钟收盘价为Series格式
    assert isinstance(low, pd.Series)
    assert isinstance(amount, pd.Series)
    # 传入涨停价必须是浮点数或整数格式
    assert isinstance(up_limit, pd.Series)
    # 取出分钟最高价和收盘价
    df = pd.DataFrame()
    df['low'] = low
    df['amount'] = amount
    # 涨停价
    df['up_limit'] = up_limit[0]
    # 涨停分钟成交额
    df['ref1_riseover_amount'] = [df.loc[i, 'amount'] if df.loc[i, 'low'] == df.loc[i, 'up_limit']
                                    else 0 for i in df.index]
    # 板上成交额
    ref1_riseover_amount = df['ref1_riseover_amount'].sum()

    return ref1_riseover_amount


if __name__ == '__main__':
    from qytools.db_read import DBReader
    db_read = DBReader()
    data = db_read.read_tdx_1min_data(start=20201023, end=20201023, fields=['low', 'amount'], code=600573)
    up_limit = db_read.read_ts_day_data(start=20201023, end=20201023, fields='up_limit', code=600573)
    low = data['low']
    amount = data['amount']
    up_limit = up_limit['up_limit']
    print(cal(low, amount, up_limit))