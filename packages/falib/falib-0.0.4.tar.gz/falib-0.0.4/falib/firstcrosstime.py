# -*- coding:utf-8 -*-
# @Time: 2020/11/7 15:09
# @Author: wangtao
# @File: firstcrosstime.py

import pandas as pd
import numpy as np
import datetime


def cal(time: pd.Series, price: pd.Series, target_price):
	"""
	突破一定涨幅的时间分钟数
	例如：可用来计算涨停时间
	
	Parameters
	----------
	time : Series
		当天的分钟序列
	price : Series
		当天分钟价格序列
	target_price : float or Series
		昨日收盘价（例如用于计算涨停价格）
		Examples1:
			8.91
		Examples2:
			----------------------------------
			0      8.91
			1      8.91
			...
			238    8.91
			239    8.91
			Name: pre_close, Length: 240, dtype: float64
			----------------------------------
	time_start : str, Default '09:30:00'
		计时起始分钟
		
	Returns
	-------
	float
		首次突破时间（例如首次涨停时间）
		Examples:
			----------
			48.0
			----------
	"""
	
	if isinstance(time, pd.Series) and isinstance(price, pd.Series):
		df_merge = pd.DataFrame({'time': time, 'price': price})
		df_merge['target_price'] = target_price
		df_cross = df_merge[round(df_merge['price'], 2) >= round(df_merge['target_price'], 2)]
		mins = df_cross.index.min() + 1
	else:
		raise ValueError('传入的time和high需为Series格式')
	return mins


if __name__ == '__main__':
	import qytools
	db_read = qytools.db_read.DBReader()
	date = db_read.get_opendate(20200826)
	df_min_date = db_read.read_tdx_1min_data(start=date, end=date,fields='code,date,time,close', code=[601216])
	df_day_date = db_read.read_ts_day_data(start=20200826, end=20200826, fields='code,date,up_limit', code=[601216])
	df_min_date['up_limit'] = df_day_date.up_limit[0]
	cal(df_min_date.time, df_min_date.close, df_min_date.up_limit)
