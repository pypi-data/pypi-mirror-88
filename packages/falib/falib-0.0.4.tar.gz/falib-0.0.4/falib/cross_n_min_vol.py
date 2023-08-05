# -*- coding:utf-8 -*-
# @Time: 2020/11/8 16:44
# @Author: jiangwenhao
# @File: cross_n_min_vol.py

import pandas as pd
import numpy as np


def cal(close, up_limit, vol, n=1):
	"""
	计算个股今日涨停前n分钟的成交量

	Parameters
	----------
	close : Series
		收盘价
	up_limit : Series
		涨停价（index应与close对应）
	vol : Series
		成交量
	n : int
		突破前n分钟，默认为1

	Returns
	-------
	pd.Series
		个股今日涨停前n分钟的成交量
		Examples:
			----------------------------------
			0          NaN
			1          NaN
			2          NaN
			3          NaN
			...
			50         NaN
			51         NaN
			52    223487.7
			Name: cross_n_min_vol, Length: 53, dtype: float64
			----------------------------------
	"""
	if isinstance(close, pd.Series) and isinstance(up_limit, pd.Series) & isinstance(vol, pd.Series) & isinstance(n, int):
		df_compare = pd.DataFrame({'close': close, 'up_limit': up_limit, 'vol': vol}).reset_index(drop=True)
		df_compare['last_1_min_close'] = df_compare['close'].shift(1)
		df_compare['last_min_vol'] = df_compare['vol'].shift(1)
		df_compare['is_cross'] = df_compare.apply(
			lambda x: 1 if
			(round(x['close'], 2) >= round(x['up_limit'], 2)) & (round(x['last_1_min_close'], 2) < round(x['up_limit'], 2))
			else 0, axis=1
		)
		df_compare['n_min_vol'] = df_compare['last_min_vol'].rolling(window=n, min_periods=1).sum()
		cross_n_min_vol = df_compare.apply(
			lambda x: x['last_min_vol'] if x['is_cross'] == 1 else np.nan, axis=1
				)
		cross_n_min_vol = cross_n_min_vol.dropna()
		if len(cross_n_min_vol) == 0:
			cross_n_min_vol = pd.Series([np.nan])
	else:
		raise ValueError('传入的close,up_limit和vol需为Series格式,n需为int格式')
	return cross_n_min_vol
