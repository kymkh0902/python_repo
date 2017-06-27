# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 12:16:16 2017

@author: whikwon
"""
import pandas as pd
import query_state as qs
import pyodbc

"""Database 목록"""

db1 = 'DRIVER={Oracle in OraClient11g_home1};DBQ=oc_tqms1;UID=lqms_view;PWD=viewdb7388;'               
db2 = 'DRIVER={Oracle in OraClient11g_home1};DBQ=oc_tqms1;UID=dqms_view;PWD=viewdb7388;'               


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
        lqms = pyodbc.connect(db1)
        X = pd.read_sql_query(qs.lqms_data(prod_wc_cd, prod_cd, start_date, end_date, *items), lqms)        
        X.columns = ['lot','제품코드','물성','단위','n수','측정값','USL','LSL','판정']
        X['측정값'] = X['측정값'].apply(lambda x : 1 if x in ['OK','NG'] else x)
        X[['측정값','USL','LSL']] = X[['측정값','USL','LSL']].astype(float)
        
        del lqms
        
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
        usl, lsl = usl.iloc[0], lsl.iloc[0]

    sigma = (data.groupby('lot')['측정값'].max() - data.groupby('lot')['측정값'].min()).mean()/d2
    if sigma == 0: 
        raise Exception('Sigma 값이 0입니다. 측정값 내 편차가 없어서 Cpk 산출이 불가합니다.')
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

    
class dqms():
    """DQMS 사용"""
    def read_model(customer = 'LGD', grade = '', model = ''):
        """
        model 정보 불러올 때 사용한다.
        
        Parameters
        ----------
        customer : 고객사(str)
        grade : grade(str)
        model : 모델명(str)
        
        Returns
        -------
        X : 고객사, Grade 별 모델 정보(dataframe)
        
        """
        dqms =  pyodbc.connect(db2)
        X = pd.read_sql_query(qs.read_model(customer, grade, model), dqms)
        X.columns = ['고객사','grade','part no','상/하','모델명','점착제1','점착제2','모드type','application']

        del dqms
        
        return X
    