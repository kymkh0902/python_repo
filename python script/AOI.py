
# coding: utf-8

# In[ ]:


"""
Created on Fri Sep  2 20:47:56 2016

@author: whikwon
"""
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

#공정 정보 입력

광학계 = {'1':'크로스2', '2': '슬릿반사', '3': '미분투과', '4': '정투과', '5' : '미분투과', '6': '정반사B', '7':'정반사A', '8' : '사선경계', '9':'크로스1'}
names = ['날짜','AOI이름','Frame수', '카메라(PC)', '사용안함', 'INDEX', '불량유형(10진수)','X','y', 'X-Size','Y-Size', '불량이미지','Path','사용안함','Value','흑점','조명밝기']
Frame_2_2 = {'1' : 32.9474, '2' : 0, '3': 110.019, '4': 110.019, '5' : 0, '6' : 110.019, '7' : 146.687, '9' : 22.2042}
Frame_3_2 = {'1' : 46.9471, '2':48.7071, '3':0, 4:106.12, '4':106.12, '6':106.12, '7':106.12, '9':46.9471}
Frame_2_1 = {'1' : 33.2985, '2': 0, '3' : 103.357, '4' :103.357, '6': 103.357, '7' : 103.357, '9' : 34.3177 }
Frame_2_3 = {'1' : 22.3609, '2' : 0, '3' : 110.795, '4' : 73.8632, '5' : 0, '6' : 110.795, '7' : 147.726336, '8' : 110.794752, '9' : 22.3609 }
Frame_3_1 = {'1' : 47.6117, '2' : 0, '3' : 0, '4' :0, '6' : 0, '7' : 0, '9' : 0}
Frame = {'CC01' : Frame_2_1, 'CC02' : Frame_2_2, 'CC03' : Frame_2_3, 'DC02' : Frame_3_2, 'DC01' : Frame_3_1}

def inch_info(inch_x, inch_y, pitch, axis = 90):
    inch_x = inch_x + 1.2
    inch_y = inch_y + 1.2 #6323A
    if axis == 0:
        inch_x, inch_y = inch_y, inch_x    
    pitch = pitch 
    pitch_add = (pitch%inch_y)/int(pitch/inch_y)
    inch_y = (inch_y + pitch_add)
    return(inch_x, inch_y/1000)

def prod_ratio3(data, bin_x, bin_y, lot):
    result = []
    for i in data['불량명'].drop_duplicates(): #변경 : 불량명
        data_strong = data[(data['강/약'] == '강')&(data['불량명'] == i)] #변경 : 불량명
        before = data_strong[['cut_x','cut_y']].drop_duplicates().dropna() 
        chip_qty = ((len(bin_x)-1)*(len(bin_y)-1))
        prod_ratio= 100 - (1-((len(before)/chip_qty)))*100 
        result += [i, len(before), prod_ratio, lot] 
    data_strong = data[(data['강/약'] == '강')]
    before = data_strong[['cut_x','cut_y']].drop_duplicates().dropna() 
    chip_qty = ((len(bin_x)-1)*(len(bin_y)-1))
    prod_ratio= 100 - (1-((len(before)/chip_qty)))*100
    result += ['합계(총 수율)', len(before), prod_ratio, lot]
    return result

def read_lot(Folder):
    os.chdir(Folder)
    lot = []     
    lot = [i[:-4] for i in glob.glob('**') if len(i) > 12]
    return lot


def read_csvfile(lot, width, length, inch_x, inch_y, *args):
    AOI = pd.read_csv(lot+'.csv', usecols = [4, 6, 7, 12, 13, 16, 21, 23], skiprows = [0], encoding = 'euc-kr', names = ['Y','X','기호','Size','Value','광학계','강/약','불량명'], error_bad_lines=False)
    AOI['Y'] = AOI['Y']/1000   
    #연결부
    AOI['cut'] = pd.cut(AOI.Y, range(0, length, 1))
    cut = AOI[(AOI['강/약'] == '강')&(AOI['불량명'].isin(['기포(백)','기포(흑)']))].groupby('cut').size()
    CUT = cut[cut>75]
    conn = []
    for i in range(0, len(CUT)):
        conn.append(CUT.index[i])
    AOI = AOI[~AOI.cut.isin(conn)]
    print(lot, conn)
        
    #chip 나누기
    bin_x = chip_division(width, inch_x)
    bin_y = chip_division_y(length, inch_y)
    
    labels_x = label_maker('x', len(bin_x)-1)
    labels_y = label_maker('y', len(bin_y)-1)
    
    AOI['cut_x'] = pd.cut(AOI['X'], bin_x, labels = labels_x)
    AOI['cut_y'] = pd.cut(AOI['Y'], bin_y, labels = labels_y)
    
    Adjust_AOI = AOI[(AOI['광학계'].isin(args))]
    
    return Adjust_AOI
  
  
def read_file(lot, width, length, inch_x, inch_y, *args):
    AOI = pd.read_csv('%s.txt'%lot, sep = '\t', names = names)
    AOI['Frm_length'] = AOI['카메라(PC)'].apply(lambda x: Frame[lot[8:12]][str(x)[0:1]])
    AOI['광학계'] = AOI['카메라(PC)'].apply(lambda x: 광학계[str(x)[0:1]])
    AOI['Y'] = (AOI['Frm_length']*AOI['Frame수']+AOI['y'])/1000
    AOI['강/약'] = AOI['불량유형(10진수)'].apply(lambda x: '강' if x<60000 else '약')
    AOI['Size'] = (AOI['X-Size']+AOI['Y-Size'])/2
        
    #연결부
    AOI['cut'] = pd.cut(AOI.Y, range(0, length, 1))
    cut = AOI[AOI['불량유형(10진수)'].isin([1537, 1538])].groupby('cut').size() # 미분투과(이물), 정투과(이물 흑, 선), 정반사B(이물), 크로스2(군집S/C)
    CUT = cut[cut>75]
    conn = []
    for i in range(0, len(CUT)):
        conn.append(CUT.index[i])
    AOI = AOI[~AOI.cut.isin(conn)]
    print(lot, conn)
    
    #chip 나누기
    bin_x = chip_division(width, inch_x)
    bin_y = chip_division_y(length, inch_y)

    labels_x = label_maker('x', len(bin_x)-1)
    labels_y = label_maker('y', len(bin_y)-1)
    
    AOI['cut_x'] = pd.cut(AOI['X'], bin_x, labels = labels_x)
    AOI['cut_y'] = pd.cut(AOI['Y'], bin_y, labels = labels_y)

    Adjust_AOI = AOI[(AOI['불량유형(10진수)'].isin(args))]
    
    return Adjust_AOI

def revise_data(data, width, length, inch_x, inch_y):
    bin_x = chip_division(width, inch_x)
    bin_y = chip_division(length, inch_y)
    labels_x = label_maker('x', len(bin_x)-1)
    labels_y = label_maker('y', len(bin_y)-1)
    data['cut_x'] = pd.cut(data.X, bin_x, labels = labels_x)
    data['cut_y'] = pd.cut(data.Y, bin_y, labels = labels_y)
    return data  

def rank_in_weak(data, count):
    data_weak = data[data['강/약']=='약']
    data_weak = data_weak[['Size','Value','X-Size', 'Y-Size','X','Y','cut_x','cut_y']].sort_values(['Value'], ascending = False)
    data_weak.reset_index(drop = True, inplace = True)
    data_weak.reset_index(drop = False, inplace = True)
    data_weak['rank'] = data_weak['index'].apply(lambda x:'red' if x<count else 'blue')
    return data_weak


def marker(data, Value_st, Size_st):   # Size, Value 둘다 바꾸기
    mark_add = data[(data['Value']>=Value_st)&(data['Size']>=Size_st)][['cut_x','cut_y']]
    return mark_add    
    
    
def prod_ratio(Value, Size, bin_x, bin_y, data, data_2):
    data_strong = data[(data['Value']>=Value)&(data['Size']>=Size)][['cut_x','cut_y']]
    Before = data_strong.drop_duplicates().dropna()
    After = data_2.drop_duplicates().dropna()
    Chip_qty = ((len(bin_x)-1)*(len(bin_y)-1))
    Before_ratio = (len(Before)/Chip_qty)*100 # 짤림 마킹 고려
    After_ratio = (1-(len(After)/Chip_qty))*100
    result = [len(data_strong), len(data_2), Chip_qty, Before_ratio, After_ratio]
    return result
    
    
def prod_ratio2(bin_x, bin_y, data):
    data_weak = data[(data['강/약'] == '약')][['cut_x','cut_y']]
    data_strong = data[(data['강/약']=='강')][['cut_x','cut_y']]
    st_marking = data_strong.drop_duplicates().dropna()
    Chip_qty = ((len(bin_x)-1)*(len(bin_y)-1))
    marking_ratio = ((len(st_marking)/Chip_qty))*100 # 짤림 마킹 고려
    result = [len(data_strong), len(st_marking), len(data_weak), marking_ratio]
    return result


def chip_division(axis, inch):  # inch에 따라 label 만드는 함수 
    chip_label = []
    axis = axis
    scrap_side = (axis%inch)/2
    chip_qty = int(axis/inch)
    for i in range(0, chip_qty+1):
        chip_label.append(scrap_side + i*inch)
    return chip_label
    
    
def chip_division_y(axis, inch):
    chip_label = []
    chip_qty = int(axis/inch)
    for i in range(0, chip_qty+1):
        chip_label.append(i*inch)
    return chip_label


def label_maker(axis, num):   # chip x, y 행 열 정보
    label = [] 
    axis = axis
    if axis == 'x':
        for i in range(1,num+1):
            label.append('chip%d_x'%i)
    elif axis == 'y':
        for i in range(1,num+1):
            label.append('chip%d_y'%i)
    return label
    

def make_excel_file(worksheet, col):
    worksheet.write(1, col, 'Lot')
    worksheet.write(1, col+1, '기존 마킹 수')
    worksheet.write(1, col+2, '변경 마킹 수')
    worksheet.write(1, col+3, '재단 Chip 수')
    worksheet.write(1, col+4, '변경 이전 수율')
    worksheet.write(1, col+5, '변경 이후 수율')
    worksheet.write(1, col+6, '수율 변동')
    worksheet.write(1, col+7, '평균 수율 변동(r가중치)')



def insert_image(fig, worksheet, row=0, col=0, x_scale=0.5, y_scale=0.5):   # Map용 그래프 삽입
    imgdata = BytesIO()
    fig.savefig(imgdata, format = 'png')   
    worksheet.insert_image(row, col, '', {'image_data' : imgdata, 'x_scale' : x_scale, 'y_scale' : y_scale})
    
 
    
def insert_data(worksheet, row, lot, result, col=0):
    worksheet.write(row, col, lot)
    worksheet.write(row, col+1, result[0])
    worksheet.write(row, col+2, result[1])
    worksheet.write(row, col+3, result[2])
    worksheet.write(row, col+4, result[3])
    worksheet.write(row, col+5, result[4])
    worksheet.write(row, col+6, (result[4] - result[3]))
    
 
def graph(Data, lot, width, length, bin_x, bin_y):  # 약, 강 그래프 Mapping
    fig, ax = plt.subplots(1,1, figsize = (12,6))
    g = sns.regplot(x = 'X', y = 'Y', data = Data[Data['강/약'] == '약'], color = 'b', fit_reg = False, ax = ax)
    h = sns.regplot(x = 'X', y = 'Y', data = Data[Data['강/약'] == '강'], color = 'r', fit_reg = False, ax = ax)    
    g.set(xlim = (0, width), ylim = (0, length), xticks = bin_x, yticks = bin_y, title = '%s'%lot)
    return fig
   
def graph_1(Data, lot, width, length):   #Value, Size 값 그래프 화(강, 약)
    fig, ax = plt.subplots(1,1, figsize = (12, 6))
    x = sns.regplot(x = 'Value', y = 'Size', data = Data[Data['강/약'] == '약'], color = 'b', fit_reg = False, ax = ax)
    y = sns.regplot(x = 'Value', y = 'Size', data = Data[Data['강/약'] == '강'], color = 'r', fit_reg = False, ax = ax)
    x.set(xlim = (0,200), ylim = (0,2.0), xticks = range(0,200,10), yticks = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0], title = '%s'%lot)     
    return fig
    
def graph_2(Data, lot, width, length, Value_st, Size_st):   #Value, Size 값 그래프 화(강, 약)
    fig, ax = plt.subplots(1,1, figsize = (12, 6))
    x = sns.regplot(x = 'Value', y = 'Size', data = Data[(Data['Value'] >= Value_st)&(Data['Size'] >= Size_st)], color = 'r', fit_reg = False, ax = ax, label = 'red')
    y = sns.regplot(x = 'Value', y = 'Size', data = Data[(Data['Value'] < Value_st)|(Data['Size'] < Size_st)], color = 'b', fit_reg = False, ax = ax, label = 'blue')
    x.set(xlim = (0,200), ylim = (0,2.0), xticks = range(0,200,10), yticks = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0], title = '%s'%lot)
    plt.axhline(y = 0.05, color = 'k', linewidth = 1, linestyle = '--', label = 'change')
    plt.axvline(x = Value_st, color = 'k', linewidth = 1, linestyle = '--')
    ax.legend()
    return fig
    
def make_rank(Data, count):
    B1 = Data[Data['강/약']=='약']
    B1 = B1[['Size','Value','X','Y','cut_x','cut_y']].sort_values(['Value','Size'], ascending = False)
    B1.reset_index(inplace = True)
    B1.reset_index(inplace = True)
    B1['rank'] = B1['level_0'].apply(lambda x:'red' if x<count else 'blue')
    

def heat_map(Data):
    Data['Size'] = Data['Size']*1000
    
    bin_size = [70, 100, 125, 150, 175, 200]
    bin_value = [25, 35, 50, 75, 100, 125, 150, 175]        
    labels_size = ['70-100','100-125','125-150','150-175','175-200']
    labels_value = ['25-35','35-50','50-75','75-100','100-125','125-150','150-175']
   
    Data['cut_size'] = pd.cut(Data['Size'], bin_size, labels = labels_size)
    Data['cut_value'] = pd.cut(Data['Value'], bin_value, labels = labels_value)
    
    Data = Data.groupby(by = ['cut_size','cut_value']).size().reset_index(name = 'quantity')
    Data = Data.pivot('cut_size','cut_value','quantity')
    
    fig, ax = plt.subplots(1,1, figsize = (12,6))
    x = sns.heatmap(Data, annot = True, fmt = '2g')
    x.invert_yaxis()  
    
    return fig

