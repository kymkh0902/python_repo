# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 11:54:34 2017

@author: whikwon
"""

import pandas as pd
import pyodbc
import query_state as qs


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
    r'UID=qms_view;'
    r'PWD=viewdb7388;'               
    )

"""기타 정보"""
columns = ['불량명','lot','카메라 번호', 'size(max)','size(min)','value','불량번호','x','y']
width_list = {'W1' : 1280, 'W3' : 1400, 'W4' : 1930, 'W5' : 2200}

   
    
class output():
    """
    데이터를 처리해서 특정 원하는 결과 값을 가져올 때 사용한다. 
    """
   
    def ratio(data, width, length, inch_x, inch_y, axis, pitch = None, drop = True, augment = True, x_mark = 12, y_mark = 0.012): 
        """
        입력 데이터에 대한 수율 계산
        
        Paramters
        ---------
        data : 입력 데이터(dataframe)
        width : 폭(int)
        length : 길이(int)
        inch_x : 장변(float)
        inch_y : 단변(float)
        axis : 흡수축(0, 90)
        pitch : 피치(int), 미 입력 시 inch_y와 같게 입력
        augment : True(중복된 데이터 생성)
        x_mark : 마킹 x 길이(int) 
        y_mark : 마킹 y 길이(float)
        
        Returns
        -------
        defect_ratio : 불량율(float)
                
        """
        X = data.copy()
        if drop:
            X = data.drop(['불량명','lot','카메라 번호','value','불량번호','size'], axis = 1)
        X1, X2, X3, X4 = X.copy(), X.copy(), X.copy(), X.copy()
        X1['x'], X1['y'] = X1['x'] + x_mark, X1['y'] + y_mark 
        X2['x'], X2['y'] = X2['x'] + x_mark, X2['y'] - y_mark
        X3['x'], X3['y'] = X3['x'] - x_mark, X3['y'] - y_mark
        X4['x'], X4['y'] = X4['x'] - x_mark, X4['y'] + y_mark

        X = pd.concat([X, X1, X2, X3, X4], axis = 0)                            
        X, chip_qty = division(X, width, length, inch_x, inch_y, axis, pitch)
        defect_qty = len(X[['cut_x','cut_y']].drop_duplicates().dropna())
        defect_ratio = defect_qty/chip_qty*100
        return defect_ratio
     
    def counting(data, size1, size2, value1, value2, include_lowest = True):
        """
        입력 데이터 불량의 size, value 지정 값 사이 마킹 개수 계산
        
        Parameters
        ----------
        data : 입력 데이터(dataframe)
        size1 : 최소 size(float)
        size2 : 최대 size(float)
        value1 : 최소 value(float)
        value2 : 최대 value(float)
        include_lowest : True(최소값 포함), False(최소값 미포함)
                
        Returns
        -------
        defect_count : 마킹 개수(int)
        
        """
        if include_lowest:
            defect_count = len(data[(data['size']>=size1)&(data['size']<size2)&(data['value']>=value1)&(data['value']<value2)])
        else:
            defect_count = len(data[(data['size']>size1)&(data['size']<size2)&(data['value']>value1)&(data['value']<value2)])
        return defect_count
            
        
    def markinginfo(data, width, length, inch_x, inch_y, axis, pitch = None):
        """
        Chip 별 마킹 정보 확인
        
        Parameters
        ----------
        data :  입력 데이터(dataframe)
        width : 폭(int)
        length : 길이(int)
        inch_x : 장변(float)
        inch_y : 단변(float)
        axis : 흡수축(0,90)
        pitch : 피치(int), 미 입력 시 inch_y와 같게 입력

        Returns
        -------
        marking_info : Chip별 마킹 정보(dataframe)
        
        """
        X = data.copy()
        X = division(X, width, length, inch_x, inch_y, axis, pitch)[0]
        marking_info = X.groupby(['cut_x','cut_y','불량번호','size','value'])['x'].count().unstack(2)
        return marking_info
        
        
class preprocessing():
    """
    데이터를 가공할 때 사용한다. 
    """

    def base(data, *args):
        """
        기본적인 데이터 가공
        
        Parameters
        ----------
        data : 입력 데이터(dataframe)        
        *args : 데이터 불량 번호(int), 순차적으로 입력
        
        Returns
        -------
        data : 수정된 데이터 (dataframe)

        """
        X = data.copy()
        if len(args) != 0:        
            X = X[X['불량번호'].isin([i for i in args])]
            
        return X
    
        
    def slitting(data, width, reverse = False):
        """
        slitting 했을 시 데이터 분할
        
        Paramters 
        ---------
        data : 입력 데이터(dataframe)
        width : 폭(int)
        reverse : False(현 데이터 방향 그대로), True(반대)
        
        Returns
        -------
        slit1, slit2 : 분할된 데이터 2개 값 출력 (tuple)
        
        """
        if reverse:
            slit1 = data[data['x'] >= width]
            slit2 = data[data['x'] < width]
            slit1['x'] = slit1['x'] - width

        else:            
            slit1 = data[data['x'] < width]
            slit2 = data[data['x'] >= width]
            slit2['x'] = slit2['x'] - width

        return slit1, slit2
        
    
              
def read_data(lot):   
    """
    데이터 불러오기 
    
    Parameters
    ----------
    lot : 입력 lot(str)
    
    Returns
    -------
    data : 해당 lot의 코팅 raw-data 
    
    """
    data = pd.read_sql_query(qs.find_das(lot), db1)
    data.columns = columns 
    data['size'] = (data['size(max)'] + data['size(min)'])/2
    data['y'] /= 1000
    data.drop(['size(max)','size(min)'], axis = 1, inplace = True)
    
    return data      
    
    
    
def read_lot_info(lot):
    """
    lot 정보 불러오기(width, length)
    
    Parameters
    ----------
    lot : 입력 lot(str)
    
    Returns
    -------
    width, length : 폭, 길이(tuple)
    
    """
    width = width_list[pd.read_sql_query(qs.find_width(lot), db2).iloc[0][0][:2]]
    length = pd.read_sql_query(qs.find_length(lot), db2).iloc[0][0]

    return width, length

def chip_qty(width, length, inch_x, inch_y, axis, pitch = None):
    """
    원단을 chip으로 잘랐을 때 chip 개수
    
    Parameters
    ----------
    width : 폭(int)
    length : 길이(int)
    inch_x : 장변(float)
    inch_y : 단변(float)
    axis : 흡수축(0,90)
    pitch : 피치(int), 미 입력 시 inch_y와 같게 입력
    
    Returns
    -------
    chip_qty : 전체 chip 개수(int)
    
    """
    if axis == 0:
        inch_x, inch_y = inch_y, inch_x     
    if pitch == None:
        pitch = inch_y
    inch_y += (pitch%inch_y)/int(pitch/inch_y) 
    inch_y /= 1000
    bins_x = [(width%inch_x)/2 + i*inch_x for i in range(0, int(width/inch_x)+1)]
    bins_y = [i*inch_y for i in range(1, int(length/inch_y)+1)]
    chip_qty = (len(bins_x)-1) * (len(bins_y)-1)
    
    return chip_qty
    

def division(data, width, length, inch_x, inch_y, axis, pitch = None):
    """
    원단을 chip으로 잘랐을 때의 chip 번호(열) 추가하기
    
    Parameters
    ----------
    data :  입력 데이터(dataframe)
    width : 폭(int)
    length : 길이(int)
    inch_x : 장변(float)
    inch_y : 단변(float)
    axis : 흡수축(0,90)
    pitch : 피치(int), 미 입력 시 inch_y와 같게 입력

    Returns
    -------
    data, total_qty : 수정된 데이터, 총 chip 수량(tuple)
    
    """
    
    X = data.copy()
    if axis == 0:
        inch_x, inch_y = inch_y, inch_x     
    if pitch == None:
        pitch = inch_y
    inch_y += (pitch%inch_y)/int(pitch/inch_y) 
    inch_y /= 1000
    bins_x = [(width%inch_x)/2 + i*inch_x for i in range(0, int(width/inch_x)+1)]
    bins_y = [i*inch_y for i in range(1, int(length/inch_y)+1)]
    labels_x = ['chip{}'.format(i) for i in range(1, len(bins_x))]
    labels_y = ['chip{}'.format(i) for i in range(1, len(bins_y))]
                
    X['cut_x'] = pd.cut(X['x'], bins = bins_x, labels = labels_x)
    X['cut_y'] = pd.cut(X['y'], bins = bins_y, labels = labels_y)
    chip_qty = len(labels_x) * len(labels_y)
    
    return X, chip_qty
  