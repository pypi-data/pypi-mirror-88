# -*- coding:utf-8 -*-
# @Time: 2020/11/8 16:44
# @Author: jiangwenhao
# @File: max_vol.py

import pandas as pd
import numpy as np


def cal(vol):
	"""
	计算个股今日最大量

	Parameters
	----------
	vol : Series
		成交量
	Returns
	-------
	float
		个股今日最大量
		Examples:
			----------------------------------
			302594.62
			----------------------------------
	"""
	if isinstance(vol, pd.Series):
		df_compare = pd.DataFrame({'vol': vol}).reset_index(drop=True)
		max_vol = df_compare['vol'].max()
	else:
		raise ValueError('传入的vol需为Series格式')
	return max_vol
