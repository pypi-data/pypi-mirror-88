# _*_coding:utf-8_*_
# @Time: 2020/11/8 9:16
# @Author: zhang chenyong
# @File: min_bomb_time.py
import pandas as pd


def cal(high, close, up_limit):
    """
    分钟炸板次数因子

    Parameters
    ----------
    high：Series    分钟最高价
        Examples :
            _________________________
                    0      8.39
                    1      8.35
                    2      8.32
                    3      8.46
                    4      8.51
                           ...
                    235    9.03
                    236    9.03
                    237    9.03
                    238    9.03
                    239    9.03
                    Name: high, Length: 240, dtype: float64
            ___________________________________

    close： Series     分钟收盘价
        Examples :
            _________________________
                    0      8.24
                    1      8.33
                    2      8.28
                    3      8.46
                    4      8.44
                           ...
                    235    9.03
                    236    9.03
                    237    9.03
                    238    9.03
                    239    9.03
                    Name: close, Length: 240, dtype: float64
            ___________________________________

    up_limit： Series  当天股票涨停价

    Returns
    -------
        int类型   分钟炸板次数
    """

    # 判断传入分钟最高价和分钟收盘价为Series格式
    assert isinstance(high, pd.Series)
    assert isinstance(close, pd.Series)
    # 传入涨停价 须是Series格式
    assert isinstance(up_limit, pd.Series)
    # 取出分钟最高价和收盘价
    df = pd.DataFrame()
    df['high'] = high
    df['close'] = close
    # 涨停价
    df['up_limit'] = up_limit[0]
    # 分钟是否炸板
    df['min_bomb'] = [1 if (df.loc[i, 'high'] == df.loc[i, 'up_limit']) & (df.loc[i, 'close'] != df.loc[i, 'up_limit'])
                      else 0 for i in df.index]
    # 总炸板次数
    ref1_min_bomb_time = df['min_bomb'].sum()

    return ref1_min_bomb_time


if __name__ == '__main__':
    from qytools.db_read import DBReader
    db_read = DBReader()
    data = db_read.read_tdx_1min_data(start=20201023, end=20201023, fields=['high', 'close'], code=600573)
    up_limit = db_read.read_ts_day_data(start=20201023, end=20201023, fields='up_limit', code=600573)
    high = data['high']
    close = data['close']
    up_limit = up_limit['up_limit']
    print(cal(high, close, up_limit))
