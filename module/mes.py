# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 16:58:08 2017

@author: whikwon
"""

import pandas as pd
import query_state as qs
import pyodbc
import os


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
    
    return data
    
    
    
def yt_inspection(start_date, end_date):
    """
    기간 별 연태 검사 실적 불러오기 
    
    Parameters
    ----------
    start_date : 시작 날짜(int or str)
    end_date : 마지막 날짜(int or str)
    
    Returns
    -------
    data : 생산 정보(dataframe) 
    
    """
    gos = pyodbc.connect(db2)
    disp_factor_cd = {'Z87':'TAPE눌림','Z97':'홍선','Z116':'눌림','A06':'TAC이물','X02':'이형이물','Z104':'이형기포',
                  'Z100':'보호기포','R09':'보호Curl','R10':'이형Curl','R11':'wave','Z110':'궁Curl','A04':'각뜸',
                  'Z111':'변뜸','Z18':'Curl검사Loss','K16':'코팅눌림','Z96':'백점','Z86':'MD눌림','XXX':'이형이물',
                  'Z47':'TAC CRACK','Z112':'점착제빠짐','Z113':'MD얼룩','A01':'DBEF이물','Z85':'흑점','C01':'재단불량',
                  'C04':'테이블','Z75':'TAC CRACK','Z12':'TAC CRACK','C05':'파괴불량','R14':'표면S/C','R20':'점형눌림',
                  'S06':'TAC기포','Z07':'POL갈라짐','Z105':'귤피','Z106':'투영불량','Z115':'PIT','Z117':'입술얼룩',
                  'Z63':'손톱자국','Z77':'자동마킹','Z84':'TAC연결','C06':'정산조정','Z29':'보호이물','Z31':'선형눌림',
                  'Z33':'마킹불량','C08':'OQC LOSS', None:'불량없음'}
                  
    insp_data = pd.read_sql_query(qs.yt_inspection(start_date, end_date), gos)        
    insp_data['불량명'] =insp_data['불량명'].apply(lambda x: disp_factor_cd[x] if x in disp_factor_cd.keys() else x)
    insp_data.fillna('-', inplace = True)
    input_qty = insp_data[['검사','투입수']].drop_duplicates()
    insp_data = insp_data.groupby(['코팅','검사','제품명','REMARK','불량명'])[['불량수']].sum().unstack().reset_index().fillna(0)
    insp_data = pd.merge(insp_data, input_qty, how = 'left', on = '검사')
    
    return insp_data

    
    
def yt_defect_summary(file_name, file_path = '//Client/D$/#.Secure Work Folder/2.투입실적/17년 투입 실적/연태'):
    """
    연태 daily 공유 파일 정리하기 
    참고) Part-No로 정리되므로 Alice/NB1와 같은 동일 모델에 불량 입력의 경우 투입 수량이 합쳐져서 정리 됨. 
    
    Parameters
    ----------
    file_name : 파일 이름 (str)
    file_path : 파일 저장되어 있는 경로 (str)

    Returns
    -------
    'YT Defect 정리.xlsx' : 엑셀 파일
    
    """    
    
    os.chdir(file_path)

    defect_name = {'圆形':'원형','未':'미','贴附':'부착','凸起':'돌기','压痕':'눌림','分层':'층간박리','程度':'정도',
                   '不定型压痕':'부정형눌림','POL缺失':'Pol파손','压印':'눌림','异物':'이물','缺胶':'점착제빠짐','撞角':'꺾임',
                   '划伤':'정도','放反':'뒤집힘','程度不良':'정도','割伤':'S/C','延伸压痕':'MD눌림','气泡':'기포','折伤':'꺾임',
                   'PNL':'패널','破损':'깨짐','红线':'홍선','唇型斑纹':'입술얼룩','唇斑':'입술얼룩','粘着剂':'점착제빠짐',
                   '紫斑':'보라색얼룩','粘胶剂':'점착제빠짐','白线':'백선','脏污':'Dirty','斑纹':'얼룩','不良':'불량','延伸':'연신'}
                   
    check_result = {'圆形':'원형','未':'미','贴附':'부착','凸起':'돌기','压痕':'눌림','分层':'층간박리','程度':'정도',
                    '不定型压痕':'부정형눌림','POL缺失':'Pol파손','压印':'눌림','异物':'이물','缺胶':'점착제빠짐','撞角':'꺾임',
                    '划伤':'정도','放反':'뒤집힘','程度不良':'정도','割伤':'S/C','延伸压痕':'MD눌림','气泡':'기포','折伤':'꺾임',
                    'PNL':'패널','破损':'깨짐','红线':'홍선','唇型斑纹':'입술얼룩','唇斑':'입술얼룩','粘着剂':'점착제빠짐',
                    '紫斑':'보라색얼룩','粘胶剂':'점착제빠짐','白线':'백선','脏污':'Dirty','斑纹':'얼룩','延伸':'연신',
                    '不良':'불량','资材':'자재','无':'무','关':'관','保护膜':'보호필름','有':'유','现象':'현상','同一':'동일','角':'모서리','部':'부',
                    '去':'제거','后':'후','造成':'유발','好':'잘','胶':'점착제','撞伤':'부딪힌','痕迹':'흔적','线状':'선형','单品':'단품',
                    '确认':'확인','末端':'단말','强制':'강제','执行':'실행','表面':'표면','撞击':'부딪힌','设备':'설비','修理品':'수리품',
                    '卡的':'부딪힘','在产线':'라인내','线头':'실오라기','起始':'시작','位置':'위치','以内':'이내','扒过':'박리','撞':'데미지'}
    defect_data = pd.read_excel(file_name, sheetname = '复判不良', parse_cols = ('C:AK'))
    input_data = pd.read_excel(file_name, sheetname = '投入数量', parse_cols = ('B:L'))

    defect_data.columns = ['투입일','투입시간','Site','Model','상/하','Part-no','불량명','불량수량','불량Lot','LGC 미귀책 사유','확인자(CS)','장소','원형눌림','PIT','MD눌림','부정형눌림','보라색얼룩',
                           '눌림','돌기','적색돌기','기포','미부착','정도','패널 깨짐','꺾음','S/C','얼룩','입술얼룩','APF층간박리','HC층간박리','꺾임','점착제빠짐','이물','홍선','기타']                
    
    #defect_data 수정                      
    defect_data['투입일'] = defect_data['투입일'].apply(lambda x: pd.Timestamp('1899-12-30') + pd.Timedelta(days = x))
    defect_data.index = defect_data['투입일']
    defect_data['Model'] = defect_data['Model'].apply(lambda x: x.upper())
    defect_data['투입월'] = defect_data['투입일'].apply(lambda x: x.month)
    defect_data['투입일자'] = defect_data['투입일'].apply(lambda x: x.day)
    
    #번역 진행 
    defect_data['불량명'] = defect_data['불량명'].replace(defect_name, regex = True)
    defect_data['LGC 미귀책 사유'] = defect_data['LGC 미귀책 사유'].replace(check_result, regex = True)
    defect_data['LGC 미귀책 사유'].fillna('-', inplace = True)
    defect_data['불량Lot'] = defect_data['불량Lot'].replace({'不承认':'해당없음'}, regex = True)
    defect_data['불량Lot'].fillna('미확인')
    defect_data['상/하'] = defect_data['상/하'].replace({'上':'상','下':'하'}, regex = True)
    
    #Input_data 수정
    input_data.dropna(how = 'all', inplace = True)
    input_data.columns = ['투입일','투입시간','투입라인','Site','Part-no','Model','제품명','Lot no.','?','투입수량','비고']
    input_data.dropna(subset = ['Model'], inplace = True)
    input_data['투입일'] = input_data['투입일'].apply(lambda x: pd.Timestamp('1899-12-30') + pd.Timedelta(days = x))
    input_data['Model'] = input_data['Model'].apply(lambda x: x.upper())
    input_data['투입월'] = input_data['투입일'].apply(lambda x: x.month)
    input_data['투입일자'] = input_data['투입일'].apply(lambda x: x.day)
    
    input_data.index = input_data['투입일']
    
    #데이터 합치기
    defect_summary = defect_data[['투입월','투입일자','Model','Part-no','상/하','불량명','불량수량','LGC 미귀책 사유','불량Lot']]
    input_summary = input_data.groupby(['Part-no','투입월'])[['투입수량']].sum().reset_index()
    data = pd.merge(defect_summary, input_summary, how = 'left', on = ['Part-no','투입월'])
    
    #data 내보내기
    writer = pd.ExcelWriter('YT Defect 정리.xlsx')
    data.to_excel(writer, 'Sheet1', index = False)
    writer.save()
    
    #파일 열기
    os.startfile('YT Defect 정리.xlsx')
        
    
    
def gm_input_summary(file_name, file_path = '//Client/D$/#.Secure Work Folder/2.투입실적/17년 투입 실적'):
    """
    구미 투입 실적 파일 정리하기(연신,코팅 매칭)
    
    Parameters
    ----------
    file_name : 파일 이름 (str)
    file_path : 파일 저장되어 있는 경로 (str)

    Returns
    -------
    'A월(구미).xlsx' : 엑셀 파일
    
    """ 
    iepcs = pyodbc.connect(db1)
    os.chdir(file_path)
    
    data = pd.read_excel(file_name, sheetname = 'raw-data', encoding = 'euc-kr', skiprows = [0] + [i for i in range(2,2296)], parse_cols = ('B:BQ'))
    data = data[data['Maker'] == 'LGC']
    data.reset_index(drop = True, inplace = True)
    
    data['연신'], data['코팅'] = 'Lot','Lot'
    lot = data['Lot No.']
    
    for j in range(len(lot)):
        findlot = pd.read_sql_query(qs.find_lot1(lot.ix[j]), iepcs)
        try : 
            data.set_value(j, '연신', findlot['연신LOT'][0])
            data.set_value(j, '코팅', findlot['코팅LOT'][0])
            print('WORKING')
            
        except : 
            data.set_value(j, '연신', '확인 불가')
            data.set_value(j, '코팅', '확인 불가')
    
    data['이물계불량'] = data['(TAB)\n내부이물_실오라기'] + data['(TAB)\n내부이물_액정계'] + data['(TAB)\n내부이물_비액정계'] + data['(TAB)\n실오라기.내부']
    
    data.to_excel('{}(구미).xlsx'.format(file_name.split()[0]), index = False)
    os.startfile('{}(구미).xlsx'.format(file_name.split()[0]))
    