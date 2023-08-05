# _*_coding:utf-8_*_
# @Time: 2020/11/8 10:42
# @Author: zhang chenyong
# @File: volume_ratio.py


import time
import pandas as pd


def cal(min_volume, auc_vol_cum_volume):
    """
    今日量比因子： 今日竞价平均分钟成交量与前五日分钟平均成交量的比值
    Parameters
    ----------
    min_volume : pd.Series   分钟数据成交量  传入的是单只股票前五天（不包含今天）的分钟数据
    auc_vol_cum_volume: pd.Series or int/float  日竞价总成交量

    Returns
    -------
    Series 类型  ref0_volume_ratio

            Examples
    ______________________________________________
    0    0.060476
    Name: ref0_volume_ratio, dtype: float64
    ______________________________________________
    """

    assert isinstance(min_volume, pd.Series)
    assert isinstance(auc_vol_cum_volume, (pd.Series, int, float))
    if len(min_volume) != 1200:
        raise ValueError('传入的分钟数据不准确')

    df = pd.DataFrame()
    #  前五日分钟平均成交量
    df['five_day_mean_min_volume'] = pd.Series(min_volume.mean())
    #  今日竞价总成交量
    if isinstance(auc_vol_cum_volume, pd.Series):
        df['auc_vol_cum_volume'] = auc_vol_cum_volume.values/10
    else:
        df['auc_vol_cum_volume'] = auc_vol_cum_volume/10

    #  今日量比
    df['ref0_volume_ratio'] = df['auc_vol_cum_volume']/df['five_day_mean_min_volume']
    ref0_volume_ratio = df['ref0_volume_ratio']
    return ref0_volume_ratio


if __name__ == '__main__':
    from qytools.db_read import DBReader
    import time
    db_read = DBReader()
    start = time.time()
    df_min_volume = db_read.read_tdx_1min_data(start=20201023, end=20201023, shift=4, fields='volume,code,datetime', code=603306)
    ref0_aucvol_data = db_read.read_aucvol_data(start=20201023, end=20201023, code=603306, fields='cum_volume,code')
    auc_vol_cum_volume = ref0_aucvol_data['cum_volume']
    min_volume = df_min_volume['volume']
    print(cal(min_volume, auc_vol_cum_volume))

    end = time.time()
    print(end-start)
