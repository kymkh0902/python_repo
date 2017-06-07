# -*- coding: utf-8 -*-
"""
Created on Thu May 25 07:32:55 2017

@author: hellojyj
"""

import pyodbc
import pandas as pd
import os

#%%

db1 = pyodbc.connect(
        r'DRIVER={Oracle in OraClient11g_home1};'
        r'DBQ=iegosp;'
        r'UID=iegos_view;'
        r'PWD=viewdb7388;'
        )

def find_lot(lot):
    return('''
    select unique_lot_no, prod_cd, prod_wc_cd, norm_qty from

             (select distinct unique_lot_no, prod_cd, prod_wc_cd, norm_qty from
                           (select unique_lot_no, prod_date, prod_wc_cd, prod_seq_no, o_global_create_no, i_global_create_no, prod_cd, normal_qty + normal_corr_qty norm_qty from tb_iem120,
                           (select o_global_create_no, i_global_create_no from tb_iem131 a, tb_iem120 b where a.i_global_create_no = b.global_create_no and a.del_flag = 'A'and b.prod_wc_cd like '%%')
                           where o_global_create_no = global_create_no)
                           start with prod_date = '{}' and prod_wc_cd = '{}' and prod_seq_no = '{}'
                           connect by prior i_global_create_no = o_global_create_no)

    where substr(prod_wc_cd, 2, 1) in ('E', 'C')
    and not substr(prod_cd, 3, 3) in ('APF')
    '''.format(lot[:8], lot[8:12], lot[12:15])
    )

data = pd.read_sql_query(find_lot('20170429DS07300'), db1)



#%% 디렉토리 설정 - 최신ver 공유받아 압축파일 해제 후 폴더 확인

path = 'D:/97. CS 일일 Data/17년LGD (파주) 투입실적_5월(송부)'        #투입실적 - 압축파일 해제 폴더

os.chdir(path)
os.getcwd()


#%% 파일 불러오기

#1 투입실적 파일 불러오기

data_1 = pd.read_excel('17년LGD (파주) 투입실적_5월(송부).xlsx', sheetname = 'lot별투입이력' )


#2 Lot 추적 rawdata

# 밑에 추적할 Lot 선정 후 진행 필요 - data_2 = ??? list_isp_trace


#%% 추적할 Lot선정

data_trace1 = data_1[data_1['MAKER'] == 'LGC']  # 조건1 : Maker - LGC만

data_trace2 = data_1[~data_1['POL Lot No.\n15자리'].isnull()]  # 조건2 : POL #N/A 제외하고

data_trace3 = data_1[~data_1['연신LOT'].isnull()] # 조건3 : 연신Lot 빈 칸만


data_trace_final = data_1[(data_1['MAKER'] == 'LGC')\
                            & (~data_1['POL Lot No.\n15자리'].isnull())\
                            & (data_1['연신LOT'].isnull())]      #조건 1 & 2 & 3
                          

list_isp_trace = data_trace_final[['POL Lot No.\n15자리']] # 추적할 검사 Lot (최종)


#%% Lot 매칭하기

lot = pd.read_sql_query(find_lot('20170520DS07011'), db1)

#%%

list_isp_trace['연신'], list_isp_trace['코팅'] = 1, 1

for i,j in zip(list_isp_trace.index, list_isp_trace['POL Lot No.\n15자리']):
    lot = pd.read_sql_query(find_lot(j), db1)
    if len(lot) == 0:
        continue
    ext = lot.iloc[0,0]
    coat = lot.iloc[1,0]
    list_isp_trace.set_value(i, '연신', ext)
    list_isp_trace.set_value(i, '코팅', coat)

    
    

    

