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


"""기타 정보"""
columns = ['광학계','lot','카메라 번호', 'size(max)','size(min)','value','불량번호','x','y']
width_list = {'W1' : 1280, 'W3' : 1400, 'W4' : 1930, 'W5' : 2200}

"""마킹 정보"""
defect_matching = {'2305' : 'Cross1_휘점(강)', '67841' : 'Cross1_휘점(약)', '2306' : 'Cross1_쿠닉(강)', '67842' : 'Cross1_쿠닉(약)',
                   '2307' : 'Cross1_군집,S/C(강)', '67843' : 'Cross1_군집,S/C(약)', '257' : 'Cross2_휘점(강)', '65793' : 'Cross2_휘점(약)',
                   '258' : 'Cross2_쿠닉(강)', '65794' : 'Cross2_쿠닉(약)', '259' : 'Cross2_군집,S/C(강)', '65795' : 'Cross2_군집,S/C(약)',
                   '1793' : '정반사A_기포(백)(강)', '67329' : '정반사A_기포(백)(약)', '1794' : '정반사A_이물(흑)(강)', '67330' : '정반사A_이물(흑)(약)',
                   '769' : '미분투과_이물(강)', '66305' : '미분투과_이물(약)', '770' : '미분투과_라미눌림(강)', '66306' : '미분투과_라미눌림(약)',
                   '772' : '미분투과_S/C(강)', '66308' : '미분투과_S/C(약)', '1537' : '정반사B_기포(백)(강)', '67073' : '정반사B_기포(백)(약)',
                   '1538' : '정반사B_이물(흑)(강)', '67074' : '정반사B_이물(흑)(약)', '1025' : '정투과_점이물(강)', '66561' : '정투과_점이물(약)',
                   '1026' : '정투과_선이물(강)', '66562' : '정투과_선이물(약)', '1281' : '투영검사_백점(강)', '66817' : '투영검사_백점(약)',
                   '1282' : '투영검사_흑점(강)', '66818' : '투영검사_흑점(약)', '69782' : 'Cross1_휘점(약)(주기)', '100059' : '정투과_점이물(약)(주기)',
                   '108752' : 'Cross1_군집,S/C(약)(주기)', '99752' : '정투과_점이물(약)(주기)', '99772' : '정투과_점이물(약)(주기)', '34216' : '정투과_점이물(강)(주기)',
                   '34236' : '정투과_점이물(강)(주기)', '5716' : 'Cross1_쿠닉(강)(주기)', '69932' : 'Cross1_휘점(약)(주기)', '84767' : '84767',
                   '84772' : '84772', '84837' : '84837', '84732' : '84732' }


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
            X = data.drop(['광학계','lot','카메라 번호','value','불량번호','size'], axis = 1)
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
    
        
    def slitting(data, width):
        """
        slitting 했을 시 데이터 분할
        
        Paramters 
        ---------
        data : 입력 데이터(dataframe)
        width : 폭(int)
        
        Returns
        -------
        slit1, slit2 : 분할된 데이터 2개 값 출력 (tuple)
        
        """
           
        slit1 = data[data['x'] < width]
        slit2 = data[data['x'] >= width]
        slit2['x'] = slit2['x'] - width
        
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
    
    data = pd.read_sql_query(qs.find_das(lot), db1)
    data.columns = columns 
    data['size'] = (data['size(max)'] + data['size(min)'])/2
    data['y'] /= 1000
    data.drop(['size(max)','size(min)'], axis = 1, inplace = True)
    data['불량명'] = data['불량번호'].apply(lambda x: defect_matching[x] if x in defect_matching.keys() else x)
    if rotate:
        after_coating_info = pd.read_sql_query(qs.after_coating(lot), db3)
        if len(after_coating_info)%2 != 0:            
            width, length = read_lot_info(lot)
            data['x'] = width - data['x']
            data['y'] = length - data['y']
        if slitting:
            data['y'] = length - data['y']

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
    '업데이트 예정'
    
  
    
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
    if lot[9] in ['E', 'C']:  #코팅lot
        width = pd.read_sql_query(qs.find_width(lot), db2).iloc[0][0][:2]
        try:
            width = int(width_list[width])                        
        except:
            if test_width != None:
                width = test_width 
            else:
                raise Exception('TEST 제품입니다. 폭을 입력해주세요')
        length = int(pd.read_sql_query(qs.find_length(lot), db2).iloc[0][0])

    elif lot[9] == 'D': #슬리팅lot
        width = int(pd.read_sql_query(qs.find_width('20170517DD03047'), db2).iloc[0].str.extract('[(](\d*)[)]')[0])
        length = int(pd.read_sql_query(qs.find_length(lot), db2).iloc[0][0])

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