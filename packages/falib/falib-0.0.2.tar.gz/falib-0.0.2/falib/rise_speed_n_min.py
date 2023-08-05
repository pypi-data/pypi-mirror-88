# -*- coding:utf-8 -*-
# @Time: 2020/11/9 09:16
# @Author: jiangwenhao
# @File: rise_speed_n_min.py

import pandas as pd
import numpy as np


def cal(close, up_limit, n=1):
	"""
	计算突破涨停前n分钟的涨速

	Parameters
	----------
	close : Series
		收盘价
	up_limit : Series
		涨停价（index应与close对应）
	n: int
		突破前n分钟，默认为1
	Returns
	-------
	pd.Series or np.array
		突破涨停前n分钟的涨速
		Examples:
			----------------------------------
			0    1.445378
			Name: rise_speed_n_min, Length: 1, dtype: float64
			----------------------------------
	"""
	if isinstance(close, pd.Series) and isinstance(up_limit, pd.Series) and isinstance(n, int):
		df_compare = pd.DataFrame({'close': close, 'up_limit': up_limit}).reset_index(drop=True)
		df_compare['last_1_min_close'] = df_compare['close'].shift(1)
		df_compare['is_cross'] = df_compare.apply(
			lambda x: 1 if
			(round(x['close'], 2) >= round(x['up_limit'], 2)) & (round(x['last_1_min_close'], 2) < round(x['up_limit'], 2))
			else 0, axis=1
		)
		df_compare['last_n_min_close'] = df_compare['close'].shift(n)

		rise_speed_n_min = df_compare.apply(
			lambda x: (x['up_limit']-x['last_n_min_close'])/x['last_n_min_close'] * 100
			if x['is_cross'] == 1
			else np.nan, axis=1
		).dropna().reset_index(drop=True)
		if len(rise_speed_n_min) ==0 :
			rise_speed_n_min =pd.Series([np.nan])
	else:
		raise ValueError('传入的close和up_limit需为Series格式,n需要为int格式')
	return rise_speed_n_min
