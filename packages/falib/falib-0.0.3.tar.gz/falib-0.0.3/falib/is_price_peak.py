import numpy as np
from numpy import array
import pandas as pd
from qytools.db_read import DBReader


def cal(high, timeperiod=20):
	"""
	最高价是否创前20日新高
	Parameters
	----------
	high:float 最高价series
	timeperiod:int 算前n日的新高

	Returns
	-------
	pd.Series
	is_price_peak:float
	Examples:
			----------------------------------
			0     NaN
			1     NaN
			2     NaN
			3     NaN
			4     NaN
			5     NaN
			6     NaN
			7     NaN
			8     NaN
			9     NaN
			10    NaN
			11    NaN
			12    NaN
			13    NaN
			14    NaN
			15    NaN
			16    NaN
			17    NaN
			18    NaN
			19    0.0
			20    1.0
			21    1.0
			22    1.0
			23    0.0
			24    1.0
			Name: high, dtype: float64
			----------------------------------
	"""

	if isinstance(high, pd.Series):
		to_yes_price_peak = high.rolling(timeperiod).max()
		is_price_peak = high-to_yes_price_peak
		is_price_peak[is_price_peak == 0] = 1
		is_price_peak[is_price_peak<0] = 0
	else:
		raise ValueError('传入的high需为Series格式')
	return is_price_peak


def judge_peak(yes_high, before_20high):
	"""
    判断昨日high是否是新高
	Parameters
	----------
	yes_high:series 昨日最高价
	before_20high: 前20日的最高价

	Returns
	-------
    1 or 0
	"""
	if yes_high >= before_20high:
		return 1
	else:
		return 0


if __name__ == '__main__':
	db_read = DBReader()
	data = db_read.read_ts_day_data(start=20190101, end=20200501, code=1)
	data['is_price_peak'] = cal(data.high)
	a = 1
