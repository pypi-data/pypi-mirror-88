# -*- coding:utf-8 -*-
# @Time: 2020/11/7 10:12
# @Author: wangtao
# @File: turnover_sector.py

import pandas as pd
import numpy as np


def cal(volume: pd.Series, flo_share: pd.Series, timeperiod=5) -> pd.Series:
	"""
	计算区间换手率
	注：默认传入的Series日期是升序排列（index越大，日期越新）

	Parameters
	----------
	volume : Series
		换手率
	flo_share : Series
		流通股本（数）
	timeperiod : int, default 5
		区间长度

	Returns
	-------
	pd.Serise
		区间换手率
		Examples:
			----------------------------------
			0           NaN
			1           NaN
			2           NaN
			3           NaN
			4      1.648735
			...
			59    24.722192
			60    24.622175
			61    24.275008
			62    22.061999
			63    21.538738
			Length: 64, dtype: float64
			----------------------------------
	"""

	if isinstance(volume, pd.Series) and isinstance(flo_share, pd.Series):
		sectorturnover = volume.rolling(timeperiod).sum() / flo_share
	else:
		raise ValueError('传入的volume和flo_share需为Series')
	return sectorturnover


if __name__ == '__main__':
	import qytools

	db_read = qytools.db_read.DBReader()
	df = db_read.read_ts_day_data(
		start=db_read.get_opendate(20200612),
		end=db_read.get_opendate(20200912),
		fields='code,date,vol,flo_share,close,turnover_rate',
		code=[601216]
	)
	sectorturnover_ser = cal(df.vol, df.flo_share)
