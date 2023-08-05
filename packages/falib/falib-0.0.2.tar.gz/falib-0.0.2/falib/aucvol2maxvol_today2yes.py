# _*_coding:utf-8_*_
# @Time: 2020/11/9 9:56
# @Author: zhang chenyong
# @File: aucvol2maxvol_today2yes.py


import pandas as pd


def cal(auc_vol_cum_volume, minute_vol):
    """
    今日竞价平均分钟量与昨日最大分钟量的比值
    Parameters
    ----------
    auc_vol_cum_volume : Series  今日竞价量  or  int/float
    minute_vol : Series  昨日分钟数据

    Returns
    -------
    Series  ref0_aucvol2maxvol_today2yes
        Examples
            ______________________________________________
            0    0.01403
            Name: ref0_aucvol2maxvol_today2yes, dtype: float64
            ______________________________________________
    """

    assert isinstance(auc_vol_cum_volume, (pd.Series, int, float))
    assert isinstance(minute_vol, pd.Series)
    df = pd.DataFrame()
    #  今日竞价总成交量
    if isinstance(auc_vol_cum_volume, pd.Series):
        df['auc_vol_cum_volume'] = auc_vol_cum_volume.values / 10
    else:
        df['auc_vol_cum_volume'] = pd.Series(auc_vol_cum_volume / 10)
    #  昨日分钟最大成交量
    df['max_min_volume'] = pd.Series(minute_vol.max())
    #  今日竞价平均分钟量对昨日最大分钟量
    df['ref0_aucvol2maxvol_today2yes'] = df['auc_vol_cum_volume']/df['max_min_volume']
    ref0_aucvol2maxvol_today2yes = df['ref0_aucvol2maxvol_today2yes']
    return ref0_aucvol2maxvol_today2yes


if __name__ == '__main__':
    from qytools.db_read import DBReader

    db_read = DBReader()
    df_min_volume = db_read.read_tdx_1min_data(start=20201023, end=20201023, fields='volume,code,datetime', code=603306)
    ref0_aucvol_data = db_read.read_aucvol_data(start=20201023, end=20201023, code=603306, fields='cum_volume,code')
    auc_vol_cum_volume = ref0_aucvol_data['cum_volume']
    minute_vol = df_min_volume['volume']
    print(cal(auc_vol_cum_volume, minute_vol))
