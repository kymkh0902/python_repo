# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 11:54:34 2017

@author: whikwon
"""

import pandas as pd
import pyodbc
import query_state as qs
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from plotly.offline import init_notebook_mode, iplot
from plotly.graph_objs import Scatter, Layout, Figure, Heatmap

init_notebook_mode()
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
sns.set_context('notebook')

"""Database 목록"""

db1 = 'DRIVER={SQL Server};SERVER=165.244.114.87;DATABASE=LGCOPTMP;UID=sa;PWD=@admin123'      
db2 = 'DRIVER={Oracle in OraClient11g_home1};DBQ=iepcs;UID=iepcs_view;PWD=viewdb7388;'   
db3 = 'DRIVER={Oracle in OraClient11g_home1};DBQ=iegosp;UID=iegos_view;PWD=viewdb7388;'               
      
"""폭 정보"""
width_list = {'W1' : 1280, 'W3' : 1400, 'W4' : 1930, 'W5' : 2200}

    
class output():
    """
    데이터를 처리해서 특정 원하는 결과 값을 가져올 때 사용한다. 
    """
   
    def ratio(data, width, length, inch_x, inch_y, axis, pitch = None, augment = True, x_mark = 12, y_mark = 0.012): 
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
        X = X[['x','y']]
        X1, X2, X3, X4 = X.copy(), X.copy(), X.copy(), X.copy()
        X1['x'], X1['y'] = X1['x'] + x_mark, X1['y'] + y_mark 
        X2['x'], X2['y'] = X2['x'] + x_mark, X2['y'] - y_mark
        X3['x'], X3['y'] = X3['x'] - x_mark, X3['y'] - y_mark
        X4['x'], X4['y'] = X4['x'] - x_mark, X4['y'] + y_mark

        X = pd.concat([X1, X2, X3, X4], axis = 0)                            
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
        marking_info = X.groupby(['cut_x','cut_y','불량명','size','value','x','y'])['x'].count().unstack(2)
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
        *args : 데이터 불량 번호(str), 순차적으로 입력
        
        Returns
        -------
        X : 수정된 데이터 (dataframe)

        """
        X = data.copy()
        if len(args) != 0:        
            X = X[X['불량번호'].isin([i for i in args])]
            
        return X
    
        
    def slitting(data, slitting_width):
        """
        slitting 했을 시 데이터 분할
        
        Paramters 
        ---------
        data : 입력 데이터(dataframe)
        slitting_width : 폭(int)
        
        Returns
        -------
        slit1, slit2 : 분할된 데이터 2개 값 출력 (tuple)
        
        """
           
        slit1 = data[data['x'] < slitting_width]
        slit2 = data[data['x'] >= slitting_width]
        slit2['x'] = slit2['x'] - slitting_width
        
        return slit1, slit2
        

        
class plot():     
    """
    그래프 그릴 때 사용한다.
    """
    
    def scatter(lot, data1, width, length, data2 = None, figsize = (8, 6)):
        """
        scatter plot, 자동검사기 맵 출력
        
        Parameter
        ---------
        lot : lot(str)
        data1 : 입력 데이터(dataframe)/'강' 불량 입력
        width : 폭(int)
        length : 길이(int)
        data2 : 입력 데이터(dataframe)/'약' 불량 입력
        figsize : 그래프 크기
        
        Return
        ------
        fig : 그래프 
        
        """
        fig, ax = plt.subplots(1,1, figsize = figsize)
        ax.scatter(data1['x'], data1['y'], s = 10, c = 'r', linewidth = 0)
        
        if data2 is not None:
            ax.scatter(data2['x'], data2['y'], s = 10, c = 'b', linewidth = 0)
    
        ax.set_xlim(0, width) 
        ax.set_ylim(0, length) 
        ax.set_xticks([i for i in range(0, width, 100)])  
        ax.set_yticks([i for i in range(0, length, 100)]) 
        ax.tick_params(axis = 'both', which = 'both', length = 0) 
        ax.grid(linewidth = 0.3)
        ax.set_title(lot)
            
        return fig
        
        
        
    def heatmap(lot, data, bins_size, bins_value, labels_size, labels_value, figsize = (12,8)):    
        """
        heatmap plot, 자동검사기 조건 별 마킹 개수 출력
        
        Parameter
        ---------
        lot : lot(str)
        data : 입력 데이터(dataframe)
        bins_size : size 나눌 값(list)
        bins_value : value 나눌 값(list)
        labels_size : size 나눌 label(list)
        labels_value : value 나눌 label(list)
        figsize : 그래프 크기
        
        Return
        ------
        fig : 그래프
        
        """
        
        X = data.copy()
        X['cut_size'] = pd.cut(X['size'], bins_size, labels = labels_size)
        X['cut_value'] = pd.cut(X['value'], bins_value, labels = labels_value)
        X = X.groupby(by = ['cut_size','cut_value']).size().unstack()
        fig, ax = plt.subplots(1,1, figsize = figsize)
        x = sns.heatmap(X, annot = True, fmt = '2g', ax = ax)
        x.invert_yaxis()
        ax.set_title(lot)

    
        return fig
                
    
class i_plot():
    """
    Interactive 그래프 그릴 때 사용한다.
    """
    
    def scatter(coating_lot, data, width, length, criteria = '광학계', slitting_width = None, 
                slitting_lot1 = None, slitting_lot2 = None, figsize = (900, 1000)):
        """
        Interactive plot, 자동검사기 맵 출력
        
        Parameters
        ----------
        coating_lot : 코팅lot(str)
        data : 입력 데이터(dataframe)
        width : 폭(int)
        length : 길이(int)
        criteria : 광학계/불량번호(str)
        slitting_width : 슬리팅 폭(int)
        slitting_lot1 : 슬리팅 첫번째 lot(str)
        slitting_lot2 : 슬리팅 두번째 lot(str)
        slitting_line : 슬리팅 기준선(int)
        figsize : 그래프 크기(tuple)
        
        Returns
        -------
        Jupyter 내 그래프 출력        
        
        """
        
        graph = []
        defect_list = [i for i in data[criteria].drop_duplicates()]
        for i in defect_list:            
            trace = Scatter(
                        x = data[data[criteria] == i]['x'],        
                        y = data[data[criteria] == i]['y'],     
                        mode = 'markers',
                        hoverinfo = 'text',
                        name = i,
                        text = [i + '<br>size:%.2f<br>value:%.f'%(j,k) for j,k in zip(data['size'],data['value'])],
                        marker = dict(
                            size = 5,
                            )
                        )
            graph.append(trace)
            
        if slitting_width:
            annotations = [dict(
                        x=slitting_width/2,
                        y=length/2,
                        xref='x',
                        yref='y',
                        text=slitting_lot1,
                        showarrow=False,                        
                        ),
                        dict(
                        x=slitting_width+(width-slitting_width)/2,
                        y=length/2,
                        xref='x',
                        yref='y',
                        text= slitting_lot2,
                        showarrow=False,                        
                        )
                        ]
            shapes = [
                        {
                        'type':'line',
                        'x0':slitting_width,
                        'y0':0,
                        'x1':slitting_width,
                        'y1':length,      
                        'line': {
                                'color': 'black',
                                'width': 1,
                                'dash': 'dot',
                            },
                        }
                    ]            

            layout = Layout(
                    title = coating_lot,
                    height = figsize[0],
                    width = figsize[1],
                    hovermode = 'closest',
                    xaxis = dict(
                        mirror = 'ticks',
                        showline = True,
                        tick0 = 0,
                        dtick = 100,
                        autotick = False,
                        showgrid = False,
                        range = [0,width]
                        ),
                    yaxis = dict(
                        mirror = 'ticks',
                        showline = True,
                        tick0 = 0,
                        dtick = 100,
                        autotick = False,
                        showgrid = True,
                        range = [0,length]
                        ),
                    margin = dict(
                        l=50,
                        r=30,
                        b=60,
                        t=160,                
                        ),
                    annotations = annotations,
                    shapes = shapes
                    )
        else:             
            layout = Layout(
                    title = coating_lot,
                    height = figsize[0],
                    width = figsize[1],
                    hovermode = 'closest',
                    xaxis = dict(                        
                        mirror = 'ticks',
                        showline = True,
                        tick0 = 0,
                        dtick = 100,
                        autotick = False,
                        showgrid = False,
                        range = [0,width]
                        ),
                    yaxis = dict(
                        mirror = 'ticks',
                        showline = True,
                        tick0 = 0,
                        dtick = 100,
                        autotick = False,
                        showgrid = True,
                        range = [0,length]
                        ),
                    margin = dict(
                        l=50,
                        r=30,
                        b=60,
                        t=160,                
                        ),
                    )
            
        fig = Figure(data=graph, layout = layout)
        iplot(fig)
                
    def heatmap(lot, data, bins_size, bins_value, labels_size, labels_value, figsize = (700,1000)):
        """
        Interactive plot, 자동검사기 맵 출력
	
        Parameter
        ---------
        lot : lot(str)
        data : 입력 데이터(dataframe)
        bins_size : size 나눌 값(list)
        bins_value : value 나눌 값(list)
        labels_size : size 나눌 label(list)
        labels_value : value 나눌 label(list)
        figsize : 그래프 크기(tuple)

        Return
        ------
        fig : 그래프
        
        """

        X = data.copy()
        X['cut_size'] = pd.cut(X['size'], bins_size, labels = labels_size)
        X['cut_value'] = pd.cut(X['value'], bins_value, labels = labels_value)
        X = X.groupby(by = ['cut_size','cut_value']).size().unstack()
        
        trace = Heatmap(
                z=[X.iloc[i] for i in range(len(X.index))],
                x=X.columns,
                y=X.index,
                colorscale='Viridis',
               )
        layout = Layout(
                title = lot,
                height = figsize[0],
                width = figsize[1],
                hovermode = 'closest',
                xaxis = dict(
                    title = 'value',
                    mirror = 'ticks',
                    showline = False,
                    ),
                yaxis = dict(               
                    mirror = 'ticks',
                    showline = False,
                    side = 'left',
                    ),                
                margin = dict(
                    l=80,
                    r=150,
                    b=50,
                    t=160,                
                    )
                )
        fig = Figure(data = [trace], layout = layout)
        iplot(fig)
        
def read_data(lot, rotate = False, slitting = False):   
    """
    데이터 불러오기(DAS)
    
    Parameters
    ----------
    lot : 입력 lot(str)
    rotate : 이 후 공정에 따른 x, y값 조정
    slitting : 이 후 공정에 슬리팅 포함될 시에 y값 반대로 조정
    
        
    Returns
    -------
    data : 해당 lot의 코팅 raw-data 
    
    """
    das = pyodbc.connect(db1)
    gos = pyodbc.connect(db3)
    
    data = pd.read_sql_query(qs.find_das(lot), das)

    data = marking_match(data, lot)
    data = data.rename(columns = {'REMARK':'광학계','UNIQUE_LOT_NO':'lot','CAMERA_NO':'카메라 번호','MAX_SIZE':'size(max)',
                                  'MIN_SIZE':'size(min)','V_VLAUE':'value','DEFECT_TYPE_CODE':'불량번호','FAULT_XPOS':'x',
                                  'FAULT_YPOS':'y','DEFECT_MARK_NAME':'불량명'})
    
    
    data['size'] = (data['size(max)'] + data['size(min)'])/2
    data['y'] /= 1000
    data.drop(['size(max)','size(min)'], axis = 1, inplace = True)
    if rotate:
        after_coating_info = pd.read_sql_query(qs.after_coating(lot), gos)
        if len(after_coating_info)%2 != 0:            
            width, length = read_lot_info(lot)
            data['x'] = width - data['x']
            data['y'] = length - data['y']
            if slitting:
                data['x'] = width - data['x']
                data['y'] = length - data['y']

    del das, gos      

    return data      
    
    
    
def read_excel(file_path):
    """
    데이터 불러오기(txt,csv)
    
    Parmaters
    ---------
    file_path : 파일 경로
    
    Returns
    -------
    data : 파일의 코팅 raw-data
        
    """
    try:
        X = pd.read_csv(file_path, sep = '\t', encoding = 'euc-kr')
    except:
        fin = open(file_path, 'r')        
        data_list = fin.readlines()
        fin.close()   
        del data_list[:6]        
        fout = open(file_path, 'w')
        fout.writelines(data_list)
        fout.close() 
        X = pd.read_csv(file_path, sep = '\t', encoding = 'euc-kr')
    
    X.columns = ['날짜','LOT이름','Frame','카메라','사용안함','INDEX','불량유형','x','y','size(min)','size(max)','img','사용안함','사용안함','백점','흑점','평균밝기']
    return X
    
    
def read_lot_info(lot, test_width = None):
    """
    lot 정보 불러오기(width, length)
    
    Parameters
    ----------
    lot : 입력 lot(str)
    width : TEST 제품의 경우 수동 입력(int)
    
    Returns
    -------
    width, length : 폭, 길이(tuple)
    
    """
    iepcs = pyodbc.connect(db2)
    
    if lot[9] in ['E', 'C']:  #코팅lot
        width = pd.read_sql_query(qs.find_width(lot), iepcs).iloc[0][0][:2]
        try:
            width = int(width_list[width])                        
        except:
            if test_width != None:
                width = test_width 
            else:
                raise Exception('TEST 제품입니다. 폭을 입력해주세요')
        length = int(pd.read_sql_query(qs.find_length(lot), iepcs).iloc[0][0])

    elif lot[9] == 'D': #슬리팅lot
        width = float(pd.read_sql_query(qs.find_width(lot), iepcs).iloc[0].str.extract('[(](\d+.\d*)[)]')[0])
        length = int(pd.read_sql_query(qs.find_length(lot), iepcs).iloc[0][0])
    
    del iepcs
    
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
    X, total_qty : 수정된 데이터, 총 chip 수량(tuple)
    
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
    
    
    
def marking_match(data, lot):
    """
    원단 불량 정보랑 마킹 유무 정보를 매칭한다
    
    Parameters
    ----------
    data : 입력 데이터(dataframe)
    
    Returns
    -------
    X : 마킹 유무 정보 포함된 데이터
    
    
    """
    das = pyodbc.connect(db1)
    
    X = data.copy()
    X['REMARK'] = X['REMARK'].apply(lambda x: '크로스1' if x == '크로스' else x)
    X['강/약'] = X['DEFECT_TYPE_CODE'].apply(lambda x: '약' if int(x)>60000 else '강')
    
    #불량명 데이터1
    defect_info1 = pd.read_sql_query(qs.defect_information1(), das)
    defect_info1 = defect_info1.rename(columns = {'WORK_CENTER_ID':'PROD_WC_CD', 'DEFECT_MARK_SYMBOL':'FAULT_MARK','STATION_NAME':'REMARK'})
    
    #마킹 유무 판별
    marking_info = pd.read_sql_query(qs.marking_information(lot), das).iloc[:,3:].T
    marking_info.reset_index(drop = False, inplace = True)
    marking_info.columns = ['CODE_DATA','ON/OFF']
    
    #불량명 데이터2
    defect_info2 = pd.read_sql_query(qs.defect_information2(), das)
    matching = {'점이물':'이물(점)','선이물':'이물(선)'} # 서버 내 오 기입된 값 따로 매칭.
    defect_info2['DEFECT_MARK_NAME'] = defect_info2['DEFECT_MARK_NAME'].apply(lambda x: matching[x] if x in matching.keys() else x)

    #불량명에 따른 마킹 유무 취합
    marking_status = pd.merge(defect_info2, marking_info, how = 'left', on = 'CODE_DATA') # 합칠 수 있을 거 같은데 JOIN문 알면   
    Y = pd.merge(X, defect_info1, how = 'left', on = ['PROD_WC_CD','FAULT_MARK','REMARK'])
    
    #최종 데이터
    X = pd.merge(Y, marking_status, how = 'left', on = ['DEFECT_MARK_NAME','REMARK','강/약'])
    X.drop('CODE_DATA', axis = 1, inplace = True)
    
    del das
    
    return X
