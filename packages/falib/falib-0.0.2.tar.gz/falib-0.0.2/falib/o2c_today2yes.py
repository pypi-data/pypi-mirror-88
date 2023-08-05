# -*- coding:utf-8 -*-
# @Time: 2020/11/8 16:44
# @Author: jiangwenhao
# @File: o2c_today2yes.py

import pandas as pd
import numpy as np


def cal(open, close) -> pd.Series:
	"""
	计算今日开盘涨幅

	Parameters
	----------
	open : Series
		开盘价
	close : Series
		收盘价

	Returns
	-------
	pd.Series or np.array
		今日开盘涨幅
		Examples:
			----------------------------------
			0           NaN
			1      0.671592
			2     -1.623816
			3     -3.349616
			4      0.652647
			...
			120   -1.320293
			121   -1.414353
			122    3.736264
			123   -0.649351
			124    1.185345
			Name: o2c_today2yes, Length: 125, dtype: float64
			----------------------------------
	"""
	if isinstance(open, pd.Series) and isinstance(close, pd.Series):
		df_compare = pd.DataFrame({'open': open, 'close': close}).reset_index(drop=True)
		df_compare['last_close'] = df_compare['close'].shift(1)
		o2c_today2yes = df_compare.apply(lambda x: ((x['open']-x['last_close'])/x['last_close'])*100, axis=1)
	else:
		raise ValueError('传入的open和close需为Series格式')
	return o2c_today2yes
