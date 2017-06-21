# -*- coding: utf-8 -*-
"""
Created on Wed May 31 15:58:54 2017

@author: whikwon
"""

import pandas as pd
import pyodbc
import os

os.chdir('C:\\Users\\whikwon\\Documents\\Python Scripts')

#GOS DB에 연결합니다. 
db1 = pyodbc.connect(
    r'DRIVER={Oracle in OraClient11g_home1};'
    r'DBQ=iegosp;'
    r'UID=iegos_view;'
    r'PWD=viewdb7388;'               
    )

#쿼리문. 지정한 날짜의 lot, 코드를 가져옵니다. 
lot = pd.read_sql_query("SELECT unique_lot_no, prod_cd FROM tb_iem120 WHERE prod_wc_cd like '%CC%' and prod_date between '20170501' and '20170531'", db1)

#TEST 코드 삭제합니다. 
lot = lot[~lot['PROD_CD'].str.contains(r'TEST')]

#점착제 전 List          
psa_list = '(H0|M0|L0|R0|J0|Z0|JS|C0|G0|S1|S2|S3|B0|P0|D3|U1|S4|KK|S7|XX|S0|Q3|Q4|U2|JB|SB|KC|JP|SP|SA|Y2|Y4|KP|L1|Q5|R4|Q6)' 
         
#코드에서 점착제 종류만 빼냅니다 --> 점착제 결정하는 코드 규칙 확인 필요. 일단 끝에서 5번째까지 코드만 읽은 후에 거기에 점착제를 뜻하는게 있는지 확인.            
lot['psa'] = lot['PROD_CD'].apply(lambda x: x[-5:]).str.extract(psa_list, expand = True)

# 행을 1만큼 이동한 열을 psa_shift라고 한다. 
lot['psa_shift'] = lot['psa'].shift(1) 

# psa_shift, psa 열을 비교해서 동일 행의 값이 같지 않을 경우 True, 
# 같을 경우 False의 내용을 가지고 있는 change? 라는 열을 만든다
lot['change?'] = lot['psa_shift'] != lot['psa'] 
                                                
print(lot[lot['change?'] == True])
                                                
