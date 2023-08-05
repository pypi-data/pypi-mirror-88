# -*- coding:utf-8 -*-
# @Time: 2020/11/8 16:44
# @Author: jiangwenhao
# @File: riseovernum_nday.py

import pandas as pd
import numpy as np


def cal(close, up_limit, ma=5):
	"""
	计算个股ma日内涨停数

	Parameters
	----------
	close : Series
		收盘价
	up_limit : Series
		涨停价（index应与close对应）
	ma: int
		日期区间(ma日）
	Returns
	-------
	pd.Series or np.array
		个股ma日内涨停数
		Examples:
			----------------------------------
			0      NaN
			1      NaN
			2      NaN
			3      NaN
			4      0.0
			...
			120    1.0
			121    1.0
			122    1.0
			123    1.0
			124    0.0
			Name: riseovernum_nday, Length: 125, dtype: float64
			----------------------------------
	"""
	if isinstance(close, pd.Series) and isinstance(up_limit, pd.Series) and isinstance(ma, int):
		df_compare = pd.DataFrame({'close': close, 'up_limit': up_limit}).reset_index(drop=True)
		df_compare['is_uplimit'] = 0
		df_compare.loc[round(df_compare['close'], 2) == round(df_compare['up_limit'], 2), 'is_uplimit'] = 1
		riseovernum_nday = df_compare['is_uplimit'].rolling(window=ma).sum()
	else:
		raise ValueError('传入的close和up_limit需为Series格式,ma需要为int格式')
	return riseovernum_nday
