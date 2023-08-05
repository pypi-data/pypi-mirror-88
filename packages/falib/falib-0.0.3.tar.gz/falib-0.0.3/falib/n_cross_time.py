# -*- coding:utf-8 -*-
# @Time: 2020/11/9 08:56
# @Author: jiangwenhao
# @File: firstcrossttime.py

import pandas as pd
import numpy as np


def cal(close, up_limit, n=1) -> pd.Series:
	"""
	计算个股突破涨停价格的分钟数

	Parameters
	----------
	close : Series
		收盘价
	up_limit : Series
		涨停价（index应与close对应）
	n : int
		第几次突破
	Returns
	-------
	pd.Series or np.array
		个股突破涨停价格的分钟数
		Examples:
			----------------------------------
			120
			----------------------------------
	"""
	if isinstance(close, pd.Series) and isinstance(up_limit, pd.Series):
		df_compare = pd.DataFrame({'close': close, 'up_limit': up_limit}).reset_index(drop=True)
		df_compare['last_close'] = df_compare['close'].shift(1)
		df_compare['is_cross'] = df_compare.apply(
			lambda x: 1 if
			(round(x['close'], 2) >= round(x['up_limit'], 2)) & (round(x['last_close'], 2) < round(x['up_limit'], 2))
			else 0, axis=1
		)
		cross_time = df_compare[df_compare['is_cross'] == 1].index.to_list()
		if len(cross_time) >= n:
			n_cross_time = cross_time[n-1]
		else:
			n_cross_time = 2
	else:
		raise ValueError('传入的close和up_limit需为Series格式')
	return n_cross_time
