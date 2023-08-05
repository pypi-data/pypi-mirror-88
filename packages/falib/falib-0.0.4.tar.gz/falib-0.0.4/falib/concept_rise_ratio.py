# _*_coding:utf-8_*_
# @Time: 2020/12/3 19:17
# @Author: zhang chenyong
# @File: concept_rise_ratio.py
from qytools.db_read import DBReader
import pandas as pd
import numpy as np


def cal(cod, date, code_in_con, con_in_code, db_read: DBReader):
    """
    计算股票所属主板块、副板块 以及 所属主板块涨幅、所属副板块涨幅
    Parameters
    ----------
    cod   list
    date   int
    code_in_con
    con_in_code
    db_read

    Returns  pd.DataFrame()

Examples:
________________________________________________________
       code        date ref1_first_con  ref1_first_con_riseratio
    0     6  2020-10-29           con3                 -0.060928
    -------

    """
    yesterday = date
    ts_day_data_today = db_read.read_ts_day_data(start=yesterday, end=yesterday,
                                                      fields=['code', 'date', 'pct_chg'],
                                                      stdrop=False)
    # 股票所属板块合并进日线数据
    ts_day_data_today = pd.merge(ts_day_data_today, con_in_code, on='code', how='left')
    ts_day_data_today.rename(columns={'pct_chg': 'pre_pct_chg'}, inplace=True)
    df_ref1_pct = ts_day_data_today[['code', 'pre_pct_chg']]
    #  计算板块当日的平均涨幅
    for i, icode_list in enumerate(code_in_con.code):
        ref1_pct_list = [df_ref1_pct.loc[icode, 'pre_pct_chg'] if icode in df_ref1_pct.code else 0 for icode in icode_list]
        code_in_con.loc[i, 'yes_con_pct_chg'] = np.mean(ref1_pct_list)
    code_in_con.sort_values(ascending=False, by=['yes_con_pct_chg'], ignore_index=True, inplace=True)
    #  读取所求股票数据
    ts_day_data_today_code = ts_day_data_today[ts_day_data_today['code'].isin(cod)].reset_index(drop=True)
    #  计算所求股票的因子 'ref1_second_con' 'ref1_second_con_riseratio' 'ref1_second_con'  'ref1_second_con_riseratio'
    for i, con_list in enumerate(ts_day_data_today_code.concept):
        # 寻找主板块和副板块
        if isinstance(con_list, list):
            # 主板块:昨日涨幅最大的板块
            if len(con_list) > 0:
                try:
                    ts_day_data_today_code.loc[i, 'ref1_first_con'] = \
                        code_in_con[code_in_con.concept.isin(con_list)].concept.iloc[0]
                except:
                    pass
                try:
                    ts_day_data_today_code.loc[i, 'ref1_first_con_riseratio'] = \
                        code_in_con[code_in_con.concept.isin(con_list)].yes_con_pct_chg.iloc[0]
                except:
                    pass
            # 股票涉及两个以上板块时，寻找副板块
            if len(con_list) > 1:
                try:
                    ts_day_data_today_code.loc[i, 'ref1_second_con'] = \
                        code_in_con[code_in_con.concept.isin(con_list)].concept.iloc[1]
                except:
                    pass
                try:
                    ts_day_data_today_code.loc[i, 'ref1_second_con_riseratio'] = \
                        code_in_con[code_in_con.concept.isin(con_list)].yes_con_pct_chg.iloc[1]
                except:
                    pass
    df_concept = ts_day_data_today_code.drop(['concept', 'pre_pct_chg'], axis=1)
    return df_concept


if __name__ == '__main__':
    cod = [78]
    yesterday = 20201029
    db_read = DBReader()
    _, code_in_con = db_read.read_concept_data(dfconcept=True, dropstandard=200)  # 板块包股票信息
    _, con_in_code = db_read.read_concept_data(dfcode=True, dropstandard=200)  # 股票包板块信息
    cal(code_in_con=code_in_con, con_in_code=con_in_code, cod=cod, date=yesterday, db_read=db_read)