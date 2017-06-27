# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 16:58:08 2017

@author: whikwon
"""

import pandas as pd
import query_state as qs
import pyodbc

"""Database 목록"""


db1 = 'DRIVER={Oracle in OraClient11g_home1};DBQ=iepcs;UID=iepcs_view;PWD=viewdb7388;'
db2 = 'DRIVER={Oracle in OraClient11g_home1};DBQ=iegosp;UID=iegos_view;PWD=viewdb7388;'               
    

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
    gos = pyodbc.connect(db2)   
    data = pd.read_sql_query(qs.find_lot(start_date, end_date, grade), gos)
    data.columns = ['연신','코팅','코드','생산량']

    del gos
    
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
    iepcs = pyodbc.connect(db1)
    data = pd.read_sql_query(qs.hq_inspection(start_date, end_date), iepcs)
    
    del iepcs
    
    return data
    
