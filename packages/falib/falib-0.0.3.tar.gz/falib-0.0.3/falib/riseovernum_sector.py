# -*- coding:utf-8 -*-
# @Time: 2020/11/6 23:22
# @Author: wangtao
# @File: riseratio_sector.py


import pandas as pd


def cal(close, up_limit, timeperiod=5):
	"""
	计算区间涨停股数(talib形式)
	注：默认传入的Series日期是升序排列（index越大，日期越新）
	
	Parameters
	----------
	close : Series
		收盘价
	up_limit : Series
		涨停价
	timeperiod : int, default 5
		区间长度
		
	Returns
	-------
	pd.Series
		区间涨停股数
		Examples:
			----------------------------------
			0      NaN
			1      NaN
			2      NaN
			3      NaN
			4      1.0
			...
			351    0.0
			352    0.0
			353    0.0
			354    0.0
			355    0.0
			Name: riseovernum_sector, Length: 356, dtype: float64
			----------------------------------
		
	"""
	
	if isinstance(close, pd.Series) and isinstance(up_limit, pd.Series):
		df_compare = pd.DataFrame({'close': close, 'up_limit': up_limit})
		df_compare['is_uplimit'] = 0
		df_compare.loc[round(df_compare['close'], 2) == round(df_compare['up_limit'], 2), 'is_uplimit'] = 1
		riseovernum_sector = df_compare['is_uplimit'].rolling(timeperiod).sum().rename('riseovernum_sector', inplace=True)
	else:
		raise ValueError('传入的close和up_limit需为Series或np.array格式')
	return riseovernum_sector


def cal_data(data, timeperiod=5):
	"""
	计算区间涨停股数(可对含多个code的原始日线表进行处理)
	注：默认传入的Series日期是升序排列（index越大，日期越新）
	
	Parameters
	----------
	data : pd.DataFrame
		日线数据表
		Examples:
			----------------------------------
			       code        date  close  up_limit
			0    300001  2020-06-12  21.99     23.82
			1    300001  2020-06-15  21.91     24.19
			2    300001  2020-06-16  22.82     24.10
			3    300001  2020-06-17  22.03     25.10
			4    300001  2020-06-18  21.91     24.23
			..      ...         ...    ...       ...
			107  601216  2020-08-26   9.80      9.80
			108  601216  2020-08-27   9.31     10.78
			109  601216  2020-08-28   9.05     10.24
			110  601216  2020-08-31   9.36      9.96
			111  601216  2020-09-01   9.10     10.30
			----------------------------------
	timeperiod : int, default 5
		区间长度
		
	Returns
	-------
	pd.DataFrame
		传入的data新增一列区间涨停股数
		Examples:
			--------------------------------------------------------------------
			       code        date  close  up_limit  riseovernum_sector
			0    300001  2020-06-12  21.99     23.82                 NaN
			1    300001  2020-06-15  21.91     24.19                 NaN
			2    300001  2020-06-16  22.82     24.10                 NaN
			3    300001  2020-06-17  22.03     25.10                 NaN
			4    300001  2020-06-18  21.91     24.23                 0.0
			..      ...         ...    ...       ...                 ...
			107  601216  2020-08-26   9.80      9.80                 1.0
			108  601216  2020-08-27   9.31     10.78                 1.0
			109  601216  2020-08-28   9.05     10.24                 1.0
			110  601216  2020-08-31   9.36      9.96                 1.0
			111  601216  2020-09-01   9.10     10.30                 1.0
			--------------------------------------------------------------------
	"""
	
	if isinstance(data, pd.DataFrame) and ('code' in data.columns):
		new_data = data.copy()
		new_data['is_uplimit'] = 0
		new_data.loc[round(new_data['close'], 2) == round(new_data['up_limit'], 2), 'is_uplimit'] = 1
		data['riseovernum_sector'] = new_data.groupby('code')['is_uplimit'].rolling(timeperiod).sum().values
	else:
		raise ValueError('传入的data不是DataFrame格式或data中不含有code列')
	return data


if __name__ == '__main__':
	import qytools
	db_read = qytools.db_read.DBReader()
	df = db_read.read_ts_day_data(start=db_read.get_opendate(20200612), end=db_read.get_opendate(20200901), fields='code,date,close,up_limit', code=[601216,300001])
	df1 = df.groupby('code').get_group(601216)
	riseovernum_sector_series = cal(df1.close, df1.up_limit)
	new_data = cal_data(df)
