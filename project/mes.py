# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 16:58:08 2017

@author: whikwon
"""

import pandas as pd
import query_state as qs
import pyodbc

"""Database 목록"""

db1 = pyodbc.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=165.244.114.87;'
    r'DATABASE=LGCOPTMP;'
    r'UID=sa;'
    r'PWD=@admin123'
    )

db2 = pyodbc.connect(
    r'DRIVER={Oracle in OraClient11g_home1};'
    r'DBQ=iepcs;'
    r'UID=iepcs_view;'
    r'PWD=viewdb7388;'   
    )

db3 = pyodbc.connect(
    r'DRIVER={Oracle in OraClient11g_home1};'
    r'DBQ=iegosp;'
    r'UID=iegos_view;'
    r'PWD=viewdb7388;'               
    )

db4 = pyodbc.connect(
    r'DRIVER={Oracle in OraClient11g_home1};'
    r'DBQ=oc_tqms1;'
    r'UID=lqms_view;'
    r'PWD=viewdb7388;'               
    )



def read_lot(start_date, end_date, grade):
    """
    Grade 기간 별 생산 정보 불러오기
    
    Parameters
    ----------
    start_date : 시작 날짜(int or str)
    end_date : 마지막 날짜(int or str)
    
    Returns
    -------
    data : 생산 정보(dataframe)
        
    """
        
    data = pd.read_sql_query(qs.find_lot(start_date, end_date, grade), db3)
    data.columns = ['연신','코팅','코드','생산량']
    return data
    
    
    
def hq_inspection(start_date, end_date):
    """
    기간 별 본사 검사 실적 불러오기 
    
    Parameters
    ----------
    start_date : 시작 날짜(int or str)
    end_Date : 마지막 날짜(int or str)
    
    Returns
    -------
    data : 생산 정보(dataframe) 
    
    """
    data = pd.read_sql_query(qs.hq_inspection(start_date, end_date), db3)
    return data
    
