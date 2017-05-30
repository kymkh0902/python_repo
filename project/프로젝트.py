# -*- coding: utf-8 -*-
"""
Created on Sat May 20 20:33:55 2017

@author: youngchan
"""
'''
--"Project : W4/5폭 개발 테스트품 예상수율 예측 프로그램"

--"문제점 : W4/5 테스품의 경우 일부 구간에 불량이 있을 경우 비켜쳐서 버리는 경우가 많아"
  "        면적효율을 고려하는 실제 양산 기준의 수율과의 Gap 차이가 많이 발생함"
  
--"해결점 : 실제 양산 환경과 같이 면적효율을 고려하여 수율 예측 실시"
--"        → 2,3열 슬리팅/재단 고려하여 수율 예측 가능할 수 있도록 설계" 

--"방법 : ① DAS에서 대상 코팅Lot 마킹정보를 끌어온다"
--"         → 마킹정보 외에 코팅Lot 양품량(길이)도 가지고 온다" 
--"       ② 몇 개의 열로 슬리팅/재단할 지를 넣어준다"
--"         → 실제 슬리팅/재단되어지는 열 외에 OS/DS 널링부의 scrap 폭도 넣어준다 
--"       ③ 각 열의 폭을 넣어준다"
--"       ④ 각 열에 재단 되어지는 TD/MD방향 길이를 넣어준다" 
--"          → 상폴 : MD_장변/TD_단변, 하폴: MD_단변/TD_장변 " 
--"       ⑥ 각 열별로 수율을 보여주고 코팅Lot 전체에 대한 수율도 보여준다"
'''

#1. data 불러오기
import os
os.getcwd()
os.chdir('//Client/D$/#.Secure Work Folder/Github/optical_python/project') #작업할 폴더의 경로를 지정해준다

import pandas as pd
data = pd.read_excel('x20170418DC02025.xlsx', sheetnames = 'das_defect_raw_20170418DC02025') #코팅Lot의 마킹 정보를 불러온다


#2.원단 폭/길이, 슬리팅 폭, 널링부/scrap, 모델 사이즈를 입력한다

width = 2250                  # 코팅 원단 폭 입력
length = 1350                 # 코팅 원단 길이 입력
nullingwidth_1 = 30           # 사이드 널링부 입력
slittingwidth_1 = 1219.4      # 슬리팅 원단 1 폭 입력
slittingwidth_2 = 1219.4      # 슬리팅 원단 2 폭 입력
nullingwidth_2 = width - (nullingwidth_1 + slittingwidth_1 + slittingwidth_2)  #반대쪽 사이드 널링 폭
model_define = 0              # 상폴/하폴 구분을 위해 흡수축 입력 → 장변, 단변 변수에 자동적으로 입력되도록 하기 위해 설정한 것임
model_X = 1219.4              # 모델 장변
model_Y = 691.2               # 모델 단변


#3. 슬리팅을 친다.

slitting_row_1 = width - nullingwidth_1 - (slittingwidth_2 + nullingwidth_2)
slitting_row_2 = width - nullingwidth_1 - slittingwidth_1 - nullingwidth_2


#4. 수율을 구한다.

  #1) 원단을 2개로 나누세요(slitting)
     # pandas 조건문, x좌표 조건 활용.
  #2) 나뉜 원단을 Chip 장변, 단변으로 쪼개 봅시다. 
     # pd.cut 함수 활용.
  #3) 전체 Chip 개수를 확인합니다.  
     # len 함수 활용.
  #4) 불량 Chip 개수를 확인합시다. 불량 유형을 보고 강/약으로 구분해야겠죠
     # apply, lambda 함수 
  #5) 동일 chip 내에 불량을 1개만 세야하니까 중복된 값들을 제거합시다.
     # cut으로 x, y 나눈 값 사용. drop_duplicates 함수 
  #6) 불량 chip을 세봅시다.
     # len 함수 활용.
  #7) 수율을 구합니다.
     # 사칙연산
     
     
#5. 자동화를 합니다.

# for Lot in [수율 구하려는 Lot List](MES): 
  
  #1) DAS에서 데이터를 불러옵니다. (DAS)

  #2) 원단의 길이, 폭 등 정보를 불러옵니다. (MES)
   
  #3) Slitting 시에 재권취가 되었는지 안 되었는지를 확인합니다. (MES)

  #4) 이제 위에서 진행한 로직 그대로 적용하시면 원하는 모든 Lot에 대한 수율을 구할 수 있습니다. 


# ※ 사소하지만 더 자동화 할 수 있는 것들을 찾아주세요. 사람 손을 안 타면 안 탈 수록 실수가 줄어듭니다. 
     

     
