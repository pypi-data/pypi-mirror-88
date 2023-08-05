# _*_coding:utf-8_*_
# @Time: 2020/11/8 9:16
# @Author: chen shigang
# @File: macd.py


import numpy as np
from numpy import array
import pandas as pd
import talib as ta
from sklearn.linear_model import LinearRegression
from qytools.db_read import DBReader


def cal(data_series, fast_period=12, slow_period=26, signal_period=9):
	"""
	series的macd三根柱子的回归斜率和信号
	Parameters
	----------

	data_series:series 计算macd的目标series
	fast_period:int 快周期线
	slow_period:int 慢周期线
	signal_period:int 快慢线的n周期平均数

	Returns
	-------

    macd_hist_reg: float macd回归斜率
    macd_signal_value: float macd信号值
	"""
	if isinstance(data_series, pd.Series):
		macd, macd_signal, macd_hist = ta.MACD(
			np.array(data_series), fast_period, slow_period, signal_period)
	elif isinstance(data_series, np.ndarray):
		macd, macd_signal, macd_hist = ta.MACD(
			data_series, fast_period, slow_period, signal_period)
	else:
		raise ValueError('传入的data_series需为Series或np.array格式')
	macd_hist_reg = pd.Series(macd_hist).rolling(3).apply(lambda x: cal_regression(x))
	# MACD信号
	condition = [(macd_hist < 0) & (macd_hist_reg > 0.001),
	             (macd_hist > 0) & (macd_hist_reg > 0.001),
	             (macd_hist > 0) & (abs(macd_hist_reg) <= 0.001),
	             (macd_hist > 0) & (macd_hist_reg < -0.001),
	             (macd_hist < 0) & (macd_hist_reg < -0.001),
	             (macd_hist < 0) & (abs(macd_hist_reg) <= 0.001)]
	macd_signal_symbol = [1, 2, 3, -1, -2, -3]
	macd_signal_value = np.select(condition, macd_signal_symbol)
	return macd_hist_reg, macd_signal_value


def cal_regression(macdhist):
	"""
    计算回归斜率
    Parameters
    ----------
    MACDhist ：float macd柱子的数值
    Returns
    -------

    reg_linear.coef_[0]   ：float MACDhist的回归斜率
    """
	reg_linear = LinearRegression().fit(
		array([1, 2, 3]).reshape(-1, 1), macdhist)
	return reg_linear.coef_[0]


if __name__ == '__main__':
	db_read = DBReader()
	data = db_read.read_ts_day_data(start=20190101, end=20200501, code=1)
	data['MACDhist_reg'], data['MACD_signal'] = cal(data.close)
	a = 1