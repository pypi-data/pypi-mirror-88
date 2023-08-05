# _*_coding:utf-8_*_
# @Time: 2020/11/8 10:42
# @Author: zhang chenyong
# @File: last_time_section.py


import pandas as pd
import numpy as np


def cal(last_time):
    """
    最后涨停时间
    Parameters
    ----------
    last_time: Series  最后涨停时间

    Returns
    -------
        int    ref1_last_time_section
    """
    # last_time 须为Series 格式
    assert isinstance(last_time, pd.Series)
    if len(last_time) != 0:
        last_time = last_time[0]
        if '09:25:00' <= last_time < '09:30:00':
            ref1_last_time_section = 0
        elif '09:30:00' <= last_time < '10:00:00':
            ref1_last_time_section = 1
        elif '10:00:00' <= last_time < '10:30:00':
            ref1_last_time_section = 2
        elif '10:30:00' <= last_time < '11:00:00':
            ref1_last_time_section = 3
        elif '11:00:00' <= last_time < '11:30:00':
            ref1_last_time_section = 4
        elif '13:00:00' <= last_time < '13:30:00':
            ref1_last_time_section = 5
        elif '13:30:00' <= last_time < '14:00:00':
            ref1_last_time_section = 6
        elif '14:00:00' <= last_time < '14:30:00':
            ref1_last_time_section = 7
        elif '14:30:00' <= last_time < '15:00:00':
            ref1_last_time_section = 8
        else:
            ref1_last_time_section = np.nan
    else:
        ref1_last_time_section = np.nan

    return ref1_last_time_section


if __name__ == '__main__':
    from qytools.db_read import DBReader
    db_read = DBReader()
    last_time = db_read.read_ts_limit_list(start=20201023, end=20201023, code=600573, fields='last_time')
    last_time = last_time['last_time']
    print(cal(last_time))
