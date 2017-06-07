# -*- coding: utf-8 -*-
"""
Created on Fri May 19 22:08:04 2017

@author: hellojyj
"""

"""

Project1 : 투입실적 Lot 자동매칭

-. 목표 : LGD파주 투입실적 파일에 연신/코팅 lot 을 자동매칭한다.

-. 단계별 구상

    a. 엑셀 data 를 python으로 불러온다.
        package : import pandas as pd
        변수 : input_data (LGD투입실적)
        함수 : pd.read_excel(17년LGD (파주) 투입실적_5월(송부).xlsx)
    b. python에서 sql 서버에 접속한다.
        package : pyodbc
        변수 : db1
        함수 : pyodbc(connect)  # 그냥 복사 붙여넣기 했음
        
    c. 검사 Lot(15자리) 에 연신, 코팅 Lot을 불러와 matching
        변수 : input_data['Lot No.']
        함수 : Lot추적 (추후 공유)
        제어문 : for문 # 역시 복사 붙여넣기 했음
    d. Data를 excel 로 내보낸다.
        변수 : input_data
        함수 : pd.to_excel
        
        
Project2 : OLED모델 테크노시스 - 알파텍 이송 후 Curl NG율 계산

-. 목표 : NG 율 계산하여 문제가 되는 Curl 유형을 확인 후 개선요청한다.

-. 단게별 구상

    a. 엑셀 data 를 python으로 불러온다.
        package : import pandas as pd
        변수1 : data_alpha
        변수2 : data_tecno
        변수3 : data_result # data 두 개 매칭된 변수? 뜻이 맞는지 확인 좀
        함수 : pd.read_excel(알파텍_2017년_OLED curl 측정결과)
               pd.read_excel(테크노시스_2017년_OLED curl 측정결과)        
    b. 동일 Lot & 동일 Box No. 를 매칭하고(공통, E열 : 'Lot' // {테크노, X},{알파텍, Y열} : '판정')
       테크노시스 OK → 알파텍 NG로 판정 되었는지 count 및 수량({알파텍, G열} : '입고 수량') 파악
        package : ??
        함수 : count, 
        제어문 : for문 (+if)
        기타 : pandas data 가공 부분 추가 공부 필요 (drop, merge 등)
    c. Data를 excel 로 내보낸다.
        변수 : data_result
        함수 : pd.to_excel

Porject3 : 코팅 초기롤 찾기 + 검사실적 / 자동검사기 data 매칭