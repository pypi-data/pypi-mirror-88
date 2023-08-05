# -*- coding:utf-8 -*-
# @Time: 2020/11/9 10:03
# @Author: jiangwenhao
# @File: cross_n_min_amount.py

import pandas as pd
import numpy as np


def cal(close, up_limit, amount, n=1) -> pd.Series:
	"""
	计算个股今日涨停前n分钟的成交额

	Parameters
	----------
	close : Series
		收盘价
	up_limit : Series
		涨停价（index应与close对应）
	amount : Series
		成交量
	n : int
		突破前n分钟，默认为1

	Returns
	-------
	pd.Series
		个股今日涨停前n分钟的成交额
		Examples:
			----------------------------------
			0            NaN
			1            NaN
			2            NaN
			3            NaN
			4            NaN
			...
			82           NaN
			83           NaN
			84           NaN
			85           NaN
			86    309095.982
			Name: cross_n_min_amount, Length: 87, dtype: float64
			----------------------------------
	"""
	if isinstance(close, pd.Series) and isinstance(up_limit, pd.Series) & isinstance(amount, pd.Series) & isinstance(n, int):
		df_compare = pd.DataFrame({'close': close, 'up_limit': up_limit, 'amount': amount}).reset_index(drop=True)
		df_compare['last_min_amount'] = df_compare['amount'].shift(1)
		df_compare['last_1_min_close'] = df_compare['close'].shift(1)
		df_compare['is_cross'] = df_compare.apply(
			lambda x: 1 if
			(round(x['close'], 2) >= round(x['up_limit'], 2)) & (round(x['last_1_min_close'], 2) < round(x['up_limit'], 2))
			else 0, axis=1
		)
		df_compare['n_min_amount'] = df_compare['last_min_amount'].rolling(window=n, min_periods=1).sum()
		cross_n_min_amount = df_compare.apply(
			lambda x: x['n_min_amount'] if x['is_cross'] == 1 else np.nan, axis=1
				)
		cross_n_min_amount = cross_n_min_amount.dropna()
		if len(cross_n_min_amount) == 0:
			cross_n_min_amount = pd.Series([np.nan])
	else:
		raise ValueError('传入的close,up_limit和amount需为Series格式,n需为int格式')
	return cross_n_min_amount
