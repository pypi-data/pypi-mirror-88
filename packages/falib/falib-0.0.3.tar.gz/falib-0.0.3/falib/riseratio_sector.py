# -*- coding:utf-8 -*-
# @Time: 2020/11/6 23:22
# @Author: wangtao
# @File: riseratio_sector.py


import pandas as pd
import numpy as np


def cal(close, timeperiod=5):
	"""
	计算区间涨幅

	Parameters
	----------
	close : Series or np.array
		收盘价
	timeperiod : int, default 5
		区间长度

	Returns
	-------
	pd.Serise
		区间涨幅
		Examples:
			----------------------------------
			0          NaN
			1          NaN
			2          NaN
			3          NaN
			4          NaN
			5    -0.004526
			...
			59    0.030500
			60    0.017884
			61    0.111111
			62    0.164908
			63    0.106291
			Name: sectorriseratio, Length: 64, dtype: float64
			----------------------------------
	"""
	
	if isinstance(close, pd.Series):
		sectorriseratio = ((close - close.shift(timeperiod)) / close.shift(timeperiod)).rename('sectorriseratio', inplace=True)
	elif isinstance(close, np.ndarray):
		sectorriseratio = (pd.Series(close) - pd.Series(close).shift(timeperiod)) / pd.Series(close).shift(timeperiod)
	else:
		raise ValueError('传入的close需为Series或np.array格式')
	return sectorriseratio


def cal_data(data, by='close', timeperiod=5):
	"""
	符合原始数据计算的区间涨幅
	为了简便运算，部分文件含有cal_data函数，可以针对日线数据库中的格式对多个股票同时操作
	
	Parameters
	----------
	data : pd.DataFrame
		原始日线数据表格式的df
		Examples:
			----------------------------------
			       code        date  close
			0    300001  2020-06-12  21.99
			1    300001  2020-06-15  21.91
			..      ...         ...    ...
			126  601216  2020-09-10   7.39
			127  601216  2020-09-11   7.32
			----------------------------------
	by ： str, default 'close'
		按照by 计算区间涨幅
	timeperiod : int, default 5
		区间长度
		
	Returns
	-------
	pd.DataFrame
		原始日线数据表格式的df，并新增了该因子列
		Examples:
			----------------------------------
					code       date  close  riseratio_sectors
			0    300001  2020-06-12  21.99                NaN
			1    300001  2020-06-15  21.91                NaN
			2    300001  2020-06-16  22.82                NaN
			3    300001  2020-06-17  22.03                NaN
			4    300001  2020-06-18  21.91                NaN
			..      ...         ...    ...                ...
			123  601216  2020-09-07   8.37          -0.105769
			124  601216  2020-09-08   8.07          -0.113187
			125  601216  2020-09-09   7.32          -0.194719
			126  601216  2020-09-10   7.39          -0.204521
			127  601216  2020-09-11   7.32          -0.188470
			----------------------------------
	"""

	if isinstance(data, pd.DataFrame) and ('code' in data.columns):
		data['riseratio_sectors'] = data.groupby('code').apply(lambda x: x[by] / x[by].shift(timeperiod) - 1).values
	else:
		raise ValueError('传入的data不是DataFrame格式或data中不含有code列')
	return data


if __name__ == '__main__':
	import qytools
	db_read = qytools.db_read.DBReader()
	df = db_read.read_ts_day_data(start=db_read.get_opendate(20200612), end=db_read.get_opendate(20200912), fields='code,date,close',code=[601216, 300001])
	df1 = df.groupby('code').get_group(300001)
	sectorriseratio_ser = cal(df1.close)
	new_data = cal_data(df)
