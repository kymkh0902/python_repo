# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 11:12:27 2017

@author: hellojyj
"""

#%%
import aoi
import pandas as pd
import os

#%%

os.chdir('D:/01. Issue/★내부 Issue/170606_폴란드 자동마킹 chip 개수')

#%%

lot_list = ['20170429DC01007', '20170517DC01014', '20170518DC01008']  # i

slit_width = [[990, 990],[1125, 750], [990,990]] # j

inch_x = [[956.90, 956.90], [956.90, 1229.20], [956.90,956.90]] # k

inch_y = [[541.95, 541.95], [541.95, 695.50], [541.95, 541,95]] # l

axis = [[90,90],[0,0],[90,90]] # m

#%%

def_matching  = {'2305' : 'Cross1_휘점(강)', '67841' : 'Cross1_휘점(약)', '2306' : 'Cross1_쿠닉(강)', '67842' : 'Cross1_쿠닉(약)',\
                 '2307' : 'Cross1_군집,S/C(강)', '67843' : 'Cross1_군집,S/C(약)', '257' : 'Cross2_휘점(강)', '65793' : 'Cross2_휘점(약)',\
                 '258' : 'Cross2_쿠닉(강)', '65794' : 'Cross2_쿠닉(약)', '259' : 'Cross2_군집,S/C(강)', '65795' : 'Cross2_군집,S/C(약)',\
                 '1793' : '정반사A_기포(백)(강)', '67329' : '정반사A_기포(백)(약)', '1794' : '정반사A_이물(흑)(강)', '67330' : '정반사A_이물(흑)(약)',\
                 '769' : '미분투과_이물(강)', '66305' : '미분투과_이물(약)', '770' : '미분투과_라미눌림(강)', '66306' : '미분투과_라미눌림(약)',\
                 '772' : '미분투과_S/C(강)', '66308' : '미분투과_S/C(약)', '1537' : '정반사B_기포(백)(강)', '67073' : '정반사B_기포(백)(약)',\
                 '1538' : '정반사B_이물(흑)(강)', '67074' : '정반사B_이물(흑)(약)', '1025' : '정투과_점이물(강)', '66561' : '정투과_점이물(약)',\
                 '1026' : '정투과_선이물(강)', '66562' : '정투과_선이물(약)', '1281' : '투영검사_백점(강)', '66817' : '투영검사_백점(약)',\
                 '1282' : '투영검사_흑점(강)', '66818' : '투영검사_흑점(약)', '69782' : 'Cross1_휘점(약)(주기)', '100059' : '정투과_점이물(약)(주기)',\
                 '108752' : 'Cross1_군집,S/C(약)(주기)', '99752' : '정투과_점이물(약)(주기)', '99772' : '정투과_점이물(약)(주기)', '34216' : '정투과_점이물(강)(주기)',\
                 '34236' : '정투과_점이물(강)(주기)', '5716' : 'Cross1_쿠닉(강)(주기)', '69932' : 'Cross1_휘점(약)(주기)' }

#%%


qty = pd.DataFrame([], columns = ['lot', 'os', 'ds'])


"""
Cross1 휘점 : 2305, 67841 
Cross1 쿠닉 : 2306, 67842
Cross1 군집S/C : 2307, 67843
Cross2 휘점 : 257, 65793
Cross2 쿠닉 : 258, 65794
Cross2 군집S/C : 259, 65795
정반사A 기포(백) : 1793, 67329
정반사A 이물(흑) : 1794, 67330
미분투과 이물 : 769, 66305
미분투과 라미눌림 : 770, 66306
미분투과 S/C : 772, 66308
정반사B 기포(백) : 1537, 67073
정반사B 이물(흑): 1538, 67074
정투과 점이물 : 1025, 66561
정투과 선이물 : 1026, 66562
투영검사 백점 : 1281, 66817
투영검사 흑점 : 1282, 66818
"""

writer = pd.ExcelWriter('170606_raw_data_2.xlsx', engine = 'xlsxwriter')
workbook = writer.book



for i,j,k,l,m in zip(lot_list, slit_width, inch_x, inch_y, axis):
    data = aoi.read_data(i)
    slit1, slit2 = aoi.preprocessing.slitting(data, j[0])
    width, length = aoi.read_lot_info(i)
    
    chip_qty1 = aoi.division(slit1, j[0],length, k[0],l[0],m[0])[1]
    chip_qty2 = aoi.division(slit1, j[1],length, k[1],l[1],m[1])[1]


    marking_info_1 = aoi.output.markinginfo(slit1, j[0], length,k[0], l[0], axis = m[0])
    marking_info_2 = aoi.output.markinginfo(slit2, j[1], length,k[1], l[1], axis = m[1])

    columns_1 = marking_info_1.columns
    columns_2 = marking_info_2.columns
     
    marking_info_1.columns = [def_matching[i] for i in columns_1]
    marking_info_2.columns = [def_matching[i] for i in columns_2]
   
    chip_qty = pd.DataFrame([i, chip_qty1, chip_qty2], index = ['lot', 'os', 'ds']).T
    qty = pd.concat([qty, chip_qty])
    
    marking_info_1.to_excel(writer, sheet_name = i +'os')
    marking_info_2.to_excel(writer, sheet_name = i +'ds')

qty.to_excel(writer, sheet_name = 'Lot별 칩 수량')
workbook.close()



#%%
data = aoi.read_data('20170429DC01007')
#%%
slit1, slit2 = aoi.preprocessing.slitting(data, 990)
#%%
width, length = aoi.read_lot_info('20170429DC01007')
#%%
marking_info = aoi.output.markinginfo(slit1, 990, length,956.90, 541.95, axis = 90)
