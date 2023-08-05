# -*- coding:utf-8 -*-
# @Time: 2020/11/8 16:44
# @Author: jiangwenhao
# @File: riseoverstock_bias_ma.py

import pandas as pd
import numpy as np


def cal(close, up_limit, ma=5) -> pd.Series:
	"""
	计算涨停表现偏差度

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
		涨停表现偏差度
		Examples:
			----------------------------------
			0          NaN
			1          NaN
			2          NaN
			3          NaN
			...
			50         NaN
			51         NaN
			52    1.194458
			Name: riseoverstock_bias_ma, Length: 53, dtype: float64
			----------------------------------
	"""
	if isinstance(close, pd.Series) and isinstance(up_limit, pd.Series) and isinstance(ma, int):
		df_compare = pd.DataFrame({'close': close, 'up_limit': up_limit}).reset_index(drop=True)
		df_compare['is_up_limit'] = 0
		df_compare.loc[round(df_compare['close'], 2) == round(df_compare['up_limit'], 2), 'is_up_limit'] = 1
		df_compare['rise_ratio_cum_prod'] = ((df_compare['close'] - df_compare['close'].shift(1))/df_compare['close'].shift(1)+1).cumprod()
		df_compare['rise_ratio_ma'] = df_compare['rise_ratio_cum_prod'].rolling(window=ma).mean().shift(1)
		riseoverstock_bias_ma = df_compare.apply(
			lambda x: x['rise_ratio_cum_prod']/x['rise_ratio_ma'] if x['is_up_limit'] == 1 else np.nan, axis=1
		)
	else:
		raise ValueError('传入的close和up_limit需为Series格式,ma需要为int格式')
	return riseoverstock_bias_ma
