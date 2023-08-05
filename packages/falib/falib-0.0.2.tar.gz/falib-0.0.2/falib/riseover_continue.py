# -*- coding:utf-8 -*-
# @Time: 2020/11/7 14:45
# @Author: wangtao
# @File: riseover_continue.py

import pandas as pd


def cal(close: pd.Series, up_limit: pd.Series):
	"""
	计算连板数

	Parameters
	----------
	close : Series
		收盘价
	up_limit : Series
		涨停价（index应与close对应）
		
	Returns
	-------
	pd.Series
		连板数
		Examples:
			----------------------------------
			0      0.0
			1      0.0
			...
			176    0.0
			177    0.0
			Name: riseovernum_continue, Length: 178, dtype: float64
			----------------------------------
	"""
	
	if isinstance(close, pd.Series) and isinstance(up_limit, pd.Series):
		df_compare = pd.DataFrame({'close': close, 'up_limit': up_limit}).reset_index(drop=True)
		df_compare['is_uplimit'] = 0
		df_compare.loc[round(df_compare['close'], 2) == round(df_compare['up_limit'], 2), 'is_uplimit'] = 1
		riseovernum_continue = df_compare.rolling(window=20, min_periods=1)['is_uplimit'].apply(
			lambda x: x.index.max() - x[x == 0].index.max()).rename('riseovernum_continue', inplace=True)
	else:
		raise ValueError('传入的close需为Series格式')
	return riseovernum_continue


if __name__ == '__main__':
	import qytools
	db_read = qytools.db_read.DBReader()
	df = db_read.read_ts_day_data(start=20200612, end=20200912, fields='code,date,close,up_limit', code=[601216])
	cal(df.close, df.up_limit)
