# _*_coding:utf-8_*_
# @Time: 2020/11/8 11:17
# @Author: zhang chenyong
# @File: first_time_section.py

import pandas as pd
import numpy as np


def cal(first_time):
    """
    首次涨停时间
    Parameters
    ----------
    first_time: Series  首次涨停时间

    Returns
    -------
        int   ref1_first_time_section
    """
    # first_time 须为Series 格式
    assert isinstance(first_time, pd.Series)
    if len(first_time) != 0:
        first_time = first_time[0]
        if '09:25:00' <= first_time < '09:30:00':
            ref1_first_time_section = 0
        elif '09:30:00' <= first_time < '10:00:00':
            ref1_first_time_section = 1
        elif '10:00:00' <= first_time < '10:30:00':
            ref1_first_time_section = 2
        elif '10:30:00' <= first_time < '11:00:00':
            ref1_first_time_section = 3
        elif '11:00:00' <= first_time < '11:30:00':
            ref1_first_time_section = 4
        elif '13:00:00' <= first_time < '13:30:00':
            ref1_first_time_section = 5
        elif '13:30:00' <= first_time < '14:00:00':
            ref1_first_time_section = 6
        elif '14:00:00' <= first_time < '14:30:00':
            ref1_first_time_section = 7
        elif '14:30:00' <= first_time < '15:00:00':
            ref1_first_time_section = 8
        else:
            ref1_first_time_section = np.nan
    else:
        ref1_first_time_section = np.nan

    return ref1_first_time_section


if __name__ == '__main__':
    from qytools.db_read import DBReader
    db_read = DBReader()
    first_time = db_read.read_ts_limit_list(start=20201023, end=20201023, code=600573, fields='first_time')
    first_time = first_time['first_time']
    print(cal(first_time))
