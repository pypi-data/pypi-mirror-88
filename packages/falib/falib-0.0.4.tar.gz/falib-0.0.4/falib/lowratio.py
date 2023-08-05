# -*- coding:utf-8 -*-
# @Time: 2020/11/8 16:44
# @Author: jiangwenhao
# @File: low_ratio.py

import pandas as pd
import numpy as np


def cal(close, low):
	"""
	计算个股今日最低价涨跌幅

	Parameters
	----------
	close : Series
		收盘价
	low : Series
		最低价

	Returns
	-------
	pd.Series or np.array
		个股今日最低价涨跌幅
		Examples:
			----------------------------------
			0           NaN
			1     -4.378981
			2      0.082372
			3      0.803213
			4     -1.489028
			...
			139   -2.331190
			140   -1.554404
			141   -9.993271
			142   -3.439252
			143   -3.024781
			Name: low_ratio, Length: 144, dtype: float64
			----------------------------------
	"""
	if isinstance(close, pd.Series) and isinstance(low, pd.Series):
		df_compare = pd.DataFrame({'close': close, 'low': low}).reset_index(drop=True)
		df_compare['last_day_close'] = df_compare['close'].shift(1)
		low_ratio = df_compare.apply(
			lambda x: ((x['low'] - x['last_day_close'])/x['last_day_close']) * 100, axis=1
		)
	else:
		raise ValueError('传入的close和low需为Series格式')
	return low_ratio
