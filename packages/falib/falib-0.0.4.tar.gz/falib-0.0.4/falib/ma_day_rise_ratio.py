# -*- coding:utf-8 -*-
# @Time: 2020/11/9 09:28
# @Author: jiangwenhao
# @File: ma_day_rise_ratio.py

import pandas as pd
import numpy as np


def cal(close, ma=5) -> pd.Series:
	"""
	计算个股ma日内的涨跌幅

	Parameters
	----------
	close : Series
		收盘价
	ma: int
		日期区间(ma日）默认值为5
	Returns
	-------
	# pd.Series
		个股ma日内的涨跌幅
		Examples:
			----------------------------------
			0            NaN
			1            NaN
			2            NaN
			3            NaN
			4            NaN
			...
			139    30.342499
			140    42.337165
			141    23.442547
			142    15.100671
			143    21.302251
			Name: ma_day_rise_ratio, Length: 144, dtype: float64
			----------------------------------
	"""
	if isinstance(close, pd.Series) and isinstance(ma, int):
		df_compare = pd.DataFrame({'close': close}).reset_index(drop=True)
		df_compare['last_ma_close'] = df_compare['close'].shift(ma)
		ma_day_rise_ratio = df_compare.apply(
			lambda x: (x['close']-x['last_ma_close'])/x['last_ma_close'] * 100, axis=1
		)
	else:
		raise ValueError('传入的close需为Series格式,ma需要为int格式')
	return ma_day_rise_ratio
