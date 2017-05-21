# -*- coding: utf-8 -*-
"""
Created on Wed May 17 13:08:25 2017

@author: hellojyj
"""

import xlwings as xw
import os

os.chdir('C:/Users/Whi Kwon/Documents/카카오톡 받은 파일')
wb1 = xw.Book('원본_170511(by흥).xls')

sht1 = wb1.sheets['주문 현황']

for i in range(1, 30):
    if sht1.range('AN{}'.format(i)).value == 27:
        sht1.range('AM{}'.format(i)).value = 23
        break
    
