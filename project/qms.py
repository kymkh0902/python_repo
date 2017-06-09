# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 12:16:16 2017

@author: whikwon
"""
import pandas as pd
import query_state as qs
import pyodbc

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


class lqms():
    """LQMS 사용"""
    def read_data(prod_wc_cd, prod_cd, start_date, end_date, *items):
        """
        물성 데이터 불러올 때 사용한다.
        
        Parameters
        ----------
        code : 제품 코드(str)
        start_date : 시작 날짜(int|str)
        end_date : 마지막 날짜(int|str)
        *items : 물성 값(str) 미 입력 시 전체 값 출력
        
        Returns
        -------
        X : 데이터(dataframe)
        
        """
        
        X = pd.read_sql_query(qs.lqms_data(prod_wc_cd, prod_cd, start_date, end_date, *items), db4)        
        X.columns = ['lot','제품코드','물성','단위','n수','측정값','USL','LSL','판정']
        X[['측정값','USL','LSL']] = X[['측정값','USL','LSL']].astype(float)
        return X
        
        
def Cpk(data,d2=1.693):
    """
    Cpk 구할 때 사용한다.
    
    Parameters
    ----------
    data : 물성 데이터(dataframe)
    d2 : 1.693 (n = 3) / 1.128 (n = 2)
    
    Returns
    -------
    Cpk : Cpk값(float)
    
    """
    
    usl = data['USL'].dropna().drop_duplicates()
    lsl = data['LSL'].dropna().drop_duplicates()
    if len(usl) + len(lsl) != 2:            
        raise Exception('USL, LSL이 2개 이상 있거나 없습니다. 단일 grade, code인지 확인해보세요.')
        
    else:
        usl, lsl = usl[0], lsl[0]

    sigma = (data.groupby('lot')['측정값'].max() - data.groupby('lot')['측정값'].min()).mean()/d2
    m = data['측정값'].mean()
    Cpu = float(usl - m) / (3*sigma)
    Cpl = float(m - lsl) / (3*sigma)
    Cpk = min([Cpu, Cpl])
    return Cpk
    
    
def Ppk(data):
    """
    Ppk 구할 때 사용한다.
    
    Paramters
    ---------
    data : 물성 데이터(dataframe)
    
    Returns
    -------
    Ppk : Ppk값(float)
    
    """
    
    usl = data['USL'].dropna().drop_duplicates()
    lsl = data['LSL'].dropna().drop_duplicates()
    if len(usl) + len(lsl) != 2:            
        raise Exception('USL, LSL이 2개 이상 있거나 없습니다. 단일 grade, code인지 확인해보세요.')
        
    else:
        usl, lsl = usl[0], lsl[0]
    sigma = data['측정값'].std()
    m = data['측정값'].mean()
    Ppu = float(usl - m) / (3*sigma)
    Ppl = float(m - lsl) / (3*sigma)
    Ppk = min([Ppu, Ppl])
    return Ppk
    
        
        



        