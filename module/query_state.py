# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 12:28:08 2017

@author: whikwon
"""


#폭 찾기
def find_width(lot):
    return("SELECT a.prod_nm FROM tb_iem903 a, tb_iem120 b WHERE a.prod_cd = b.prod_cd AND b.unique_lot_no = '{}'".format(lot))

#DAS data 
def find_das(lot):
    return("SELECT a.REMARK , b.UNIQUE_LOT_NO , CAMERA_NO, MAX_SIZE , MIN_SIZE , V_VLAUE , DEFECT_TYPE_CODE, FAULT_XPOS, FAULT_YPOS, PROD_WC_CD, FAULT_MARK from LAS_DATA a, LAS_MASTER b WITH (NOLOCK)  where a.IDN = b.IDN and UNIQUE_LOT_NO = '{}'".format(lot))
    
#생산량 찾기
def find_length(lot):
    return("SELECT normal_qty + normal_corr_qty AS 생산량 FROM tb_iem120 WHERE unique_lot_no = '{}'".format(lot))

#Lot 찾기
def find_lot(start_date, end_date, grade):
    return("SELECT F_ONE_LOT_TRACE_T(ar_warhs_create_no, '_E%', '%%') AS 연신Lot, unique_lot_no AS 코팅Lot, prod_cd AS 코드, normal_qty + normal_corr_qty AS prod_qty FROM tb_iem120 WHERE prod_date BETWEEN '{}' AND '{}' AND prod_cd LIKE '%{}%' AND prod_wc_cd LIKE '%_C%'".format(start_date, end_date, grade))
    
def find_lot1(lot):
    return("SELECT F_ONE_LOT_TRACE_T(ar_warhs_create_no, '_E%', '%%') AS 연신Lot, F_ONE_LOT_TRACE_T(ar_warhs_create_no, '_C%', '%%')  AS 코팅Lot FROM tb_iem120 WHERE unique_lot_no = '{}'".format(lot))

#불량 정보1
def defect_information1():
    return("SELECT A.DEFECT_MARK_NAME, A.DEFECT_MARK_SYMBOL, B.COMMENT_1 AS STATION_NAME, A.WORK_CENTER_ID FROM dbo.QA_DEFECT_MARK A\
           WITH(NOLOCK) LEFT OUTER JOIN dbo.MASTER_CODE B WITH(NOLOCK) ON B.CODE_CLASS = '03' AND B.USE_YN=  'Y' AND B.LANGUAGE_CODE = 'KR' \
           AND A.DEFECT_MARK_STATION_NAME = B.CODE_DATA")
    
#불량 정보2
def defect_information2():
    return("SELECT CODE_DATA, COMMENT_1 AS DEFECT_MARK_NAME, COMMENT_2 AS REMARK, COMMENT_3 AS '강/약' FROM MASTER_CODE WHERE CODE_CLASS = '29'")
    
#마킹 유무 정보
def marking_information(lot):
    return(
    '''
    SELECT TOP 1 * FROM QA_PARAMETER_MARKING_HIS WHERE PARAMETER_NAME = (SELECT substring(INSPEC_STATUS, 4, 40) FROM LAS_MASTER WHERE UNIQUE_LOT_NO = '{0}')
    AND PARAMETER_DATE <= substring('{0}', 1, 4)+'-'+substring('{0}', 5, 2)+'-'+substring('{0}', 7, 2) and WORK_CENTER_ID = substring('{0}', 9, 4)
    ORDER BY PARAMETER_DATE DESC
    '''.format(lot))
    
    
#Lot 10자리 --> 16자리 변경
def lotchanger(lot):
    if len(lot) < 10:
        return ('확인 불가')
    else:
        if int(lot[1],16)>=10: 
            return('201'+lot[0]+str(int(lot[1],16))+lot[2:6]+'0'+lot[6:10])  
        else:
            return('201'+lot[0]+'0'+str(int(lot[1],16))+lot[2:6]+'0'+lot[6:10])       
            
#전체 Lot 추적    
def lottrace_whole(lot): 
    return('''
                    SELECT
                    DECODE(LEVEL_CD,'0',UNIQUE_LOT_NO)  AS LOT1
                  , DECODE(LEVEL_CD,'0',PROD_CD)        AS 코드1
                  , DECODE(LEVEL_CD,'0',NOR_QTY)        AS 생산량1
                  , DECODE(LEVEL_CD,'1',UNIQUE_LOT_NO1) AS LOT2
                  , DECODE(LEVEL_CD,'1',PROD_CD1) AS 코드2
                  , DECODE(LEVEL_CD,'1',NOR_QTY1) AS 생산량2
                  , DECODE(LEVEL_CD,'2',UNIQUE_LOT_NO1) AS LOT3
                  , DECODE(LEVEL_CD,'2',PROD_CD1) AS 코드3
                  , DECODE(LEVEL_CD,'2',NOR_QTY1) AS 생산량3
                  , DECODE(LEVEL_CD,'3',UNIQUE_LOT_NO1) AS LOT4
                  , DECODE(LEVEL_CD,'3',PROD_CD1) AS 코드4
                  , DECODE(LEVEL_CD,'3',NOR_QTY1) AS 생산량4
                  , DECODE(LEVEL_CD,'4',UNIQUE_LOT_NO1) AS LOT5
                  , DECODE(LEVEL_CD,'4',PROD_CD1) AS 코드5
                  , DECODE(LEVEL_CD,'4',NOR_QTY1) AS 생산량5
                  , DECODE(LEVEL_CD,'5',UNIQUE_LOT_NO1) AS LOT6
                  , DECODE(LEVEL_CD,'5',PROD_CD1) AS 코드6
                  , DECODE(LEVEL_CD,'5',NOR_QTY1) AS 생산량6
                  , DECODE(LEVEL_CD,'6',UNIQUE_LOT_NO1) AS LOT7
                  , DECODE(LEVEL_CD,'6',PROD_CD1) AS 코드7
                  , DECODE(LEVEL_CD,'6',NOR_QTY1) AS 생산량7
                  , DECODE(LEVEL_CD,'7',UNIQUE_LOT_NO1) AS LOT8
                  , DECODE(LEVEL_CD,'7',PROD_CD1) AS 코드8
                  , DECODE(LEVEL_CD,'7',NOR_QTY1) AS 생산량8
                  , DECODE(LEVEL_CD,'8',UNIQUE_LOT_NO1) AS LOT9
                  , DECODE(LEVEL_CD,'8',PROD_CD1) AS 코드9
                  , DECODE(LEVEL_CD,'8',NOR_QTY1) AS 생산량9
                  , DECODE(LEVEL_CD,'9',UNIQUE_LOT_NO1) AS LOT10
                  , DECODE(LEVEL_CD,'9',PROD_CD1) AS 코드10
                  , DECODE(LEVEL_CD,'9',NOR_QTY1) AS 생산량10
                  , DECODE(LEVEL_CD,'10',UNIQUE_LOT_NO1) AS LOT11
                  , DECODE(LEVEL_CD,'10',PROD_CD1) AS 코드11
                  , DECODE(LEVEL_CD,'10',NOR_QTY1) AS 생산량11
                  , DECODE(LEVEL_CD,'11',UNIQUE_LOT_NO1) AS LOT12
                  , DECODE(LEVEL_CD,'11',PROD_CD1) AS 코드12
                  , DECODE(LEVEL_CD,'11',NOR_QTY1) AS 생산량12
                  , DECODE(LEVEL_CD,'12',UNIQUE_LOT_NO1) AS LOT13
                  , DECODE(LEVEL_CD,'12',PROD_CD1) AS 코드13
                  , DECODE(LEVEL_CD,'12',NOR_QTY1) AS 생산량13
                  , DECODE(LEVEL_CD,'13',UNIQUE_LOT_NO1) AS LOT14
                  , DECODE(LEVEL_CD,'13',PROD_CD1) AS 코드14
                  , DECODE(LEVEL_CD,'13',NOR_QTY1) AS 생산량14
                  , DECODE(LEVEL_CD,'14',UNIQUE_LOT_NO1) AS LOT15
                  , DECODE(LEVEL_CD,'14',PROD_CD1) AS 코드15
                  , DECODE(LEVEL_CD,'14',NOR_QTY1) AS 생산량15
                  , DECODE(LEVEL_CD,'15',UNIQUE_LOT_NO1) AS lOT16
                  , DECODE(LEVEL_CD,'15',PROD_CD1) AS 코드16
                  , DECODE(LEVEL_CD,'15',NOR_QTY1) AS 생산량16
             FROM (
                   SELECT
                         A.PLANT_CD,
                         C.UNIQUE_LOT_NO,
                         C.PROD_CD,
                         C.HOLD_YN,
                         C.WORK_GB,
                         C.PURCH_LOT_NO AS PURCH_LOT_NO,
                         (NVL(C.NORMAL_QTY,0)+NVL(C.NORMAL_CORR_QTY,0)) AS NOR_QTY,
                         B.UNIQUE_LOT_NO AS UNIQUE_LOT_NO1,
                         B.PROD_CD AS PROD_CD1,
                         B.HOLD_YN AS HOLD_YN1,
                         B.WORK_GB AS WORK_GB1,
                         (NVL(B.NORMAL_QTY,0)+NVL(B.NORMAL_CORR_QTY,0)) AS NOR_QTY1,
                         B.PURCH_LOT_NO AS PURCH_LOT_NO1,
                         A.LEVEL_CD,
                         A.ROW_CNT
                   FROM (
                         SELECT --LOT 추적
                             PLANT_CD                AS  PLANT_CD,
                             I_AR_WARHS_CREATE_NO    AS  I_AR_WARHS_CREATE_NO,
                             O_AR_WARHS_CREATE_NO    AS  O_AR_WARHS_CREATE_NO,
                             LEVEL                   AS  LEVEL_CD,
                             ROWNUM                  AS  ROW_CNT
                          FROM TB_IEM136
                         WHERE DEL_FLAG = 'A'
                         CONNECT BY  PRIOR    PLANT_CD              = PLANT_CD                AND
                                     PRIOR    O_AR_WARHS_CREATE_NO  = I_AR_WARHS_CREATE_NO    AND
                                              DEL_FLAG              = 'A'
                         START WITH           PLANT_CD              = 'A020'                  AND
                                              DEL_FLAG              = 'A'                     AND
                                              I_AR_WARHS_CREATE_NO IN     (
                                                                              SELECT AR_WARHS_CREATE_NO
                                                                              FROM TB_IEM120
                                                                             WHERE PLANT_CD = 'A020'
                                                                             AND   unique_lot_no IN ('{}')
                                                                              AND DEL_FLAG = 'A'
                                                                                                 )
                         ) A,
                         TB_IEM120 B,
                         TB_IEM120 C
                  WHERE A.PLANT_CD = B.PLANT_CD
                    AND A.O_AR_WARHS_CREATE_NO = B.AR_WARHS_CREATE_NO
                    AND B.DEL_FLAG = 'A'
                    AND A.PLANT_CD = C.PLANT_CD
                    AND A.I_AR_WARHS_CREATE_NO = C.AR_WARHS_CREATE_NO
                    AND C.DEL_FLAG = 'A'
             UNION
              SELECT PLANT_CD,
                     UNIQUE_LOT_NO,
                     PROD_CD,
             --      PROD_WC_CD,
             --      PROD_DATE,
                     HOLD_YN,
                     WORK_GB,
                     PURCH_LOT_NO AS PURCH_LOT_NO,
                      NOR_QTY,
                     '' AS UNIQUE_LOT_NO1,
                     '' AS PROD_CD1,
                     '' AS HOLD_YN1,
                     '' AS WORK_GB1,
                     0 AS NOR_QTY1  ,
                     '' AS PURCH_LOT_NO1,
                     0 AS LEVEL_CD,
                     TO_NUMBER(MIN(ROW_CNT)) AS ROW_CNT
                FROM(

                 SELECT
                         A.PLANT_CD,
                         C.UNIQUE_LOT_NO,
                         C.PROD_WC_CD,
                         C.LOT_START_ILSI,
                         C.PROD_CD,
                         C.HOLD_YN,
                         C.WORK_GB,
                         C.PURCH_LOT_NO AS PURCH_LOT_NO,
                         (NVL(C.NORMAL_QTY,0)+NVL(C.NORMAL_CORR_QTY,0)) AS NOR_QTY,
                         B.UNIQUE_LOT_NO AS UNIQUE_LOT_NO1,
                         B.PROD_CD AS PROD_CD1,
                         B.HOLD_YN AS HOLD_YN1,
                         B.WORK_GB AS WORK_GB1,
                         (NVL(B.NORMAL_QTY,0)+NVL(B.NORMAL_CORR_QTY,0)) AS NOR_QTY1,
                         B.PURCH_LOT_NO AS PURCH_LOT_NO1,
                         A.LEVEL_CD,
                         A.ROW_CNT
                   FROM (
                         SELECT --LOT 추적
                             PLANT_CD                AS  PLANT_CD,
                             I_AR_WARHS_CREATE_NO    AS  I_AR_WARHS_CREATE_NO,
                             O_AR_WARHS_CREATE_NO    AS  O_AR_WARHS_CREATE_NO,
                             LEVEL                   AS  LEVEL_CD,
                             ROWNUM                  AS  ROW_CNT
                          FROM TB_IEM136
                         WHERE DEL_FLAG = 'A'
                         CONNECT BY  PRIOR    PLANT_CD              = PLANT_CD                AND
                                     PRIOR    O_AR_WARHS_CREATE_NO  = I_AR_WARHS_CREATE_NO    AND
                                              DEL_FLAG              = 'A'
                         START WITH           PLANT_CD              = 'A020'                  AND
                                              DEL_FLAG              = 'A'                     AND
                                              I_AR_WARHS_CREATE_NO IN     (
                                                                             SELECT AR_WARHS_CREATE_NO
                                                                             FROM TB_IEM120
                                                                             WHERE PLANT_CD = 'A020'
                                                                             AND   unique_lot_no IN ('{}')
                                                                             AND   DEL_FLAG = 'A'
                                                                                                 )
                         ) A,
                         TB_IEM120 B,
                         TB_IEM120 C
                  WHERE A.PLANT_CD = B.PLANT_CD
                    AND A.O_AR_WARHS_CREATE_NO = B.AR_WARHS_CREATE_NO
                    AND B.DEL_FLAG = 'A'
                    AND A.PLANT_CD = C.PLANT_CD
                    AND A.I_AR_WARHS_CREATE_NO = C.AR_WARHS_CREATE_NO
                    AND C.DEL_FLAG = 'A'
                ) WHERE
                    unique_lot_no IN ('{}')
               GROUP BY PLANT_cD, UNIQUE_LOT_NO, PROD_CD, PROD_WC_CD, LOT_START_ILSI, HOLD_YN, WORK_GB ,PURCH_LOT_NO, NOR_QTY

              )ORDER BY ROW_CNT, LEVEL_CD ASC
            '''.format(lot, lot, lot)
            )
                                              
#본사 검사실적                                                                                          
def hq_inspection(start_date, end_date):
    return(
    '''       
       SELECT *
    FROM
         (
         SELECT I_BE_LOT_NO
              , IN_LOT_NO      AS IN_LOT_NO
              , LOT_NO         AS LOT_NO
              , PROD_NM        AS PROD_NM
              , S.PROD_CD        AS PROD_CD
              , LENG           AS LENG
              , MANA_NM        AS MANA_NM
              , S.NORMAL_QTY     AS NORMAL_QTY
              , QTY            AS QTY
              , DISPRODUCT_QTY AS DISPRODUCT_QTY
              , GOOD_RATE      AS GOOD_RATE
              , FACTOR_01      AS FACTOR_01
              , FACTOR_02      AS FACTOR_02
              , FACTOR_03      AS FACTOR_03
              , FACTOR_04      AS FACTOR_04
              , FACTOR_05      AS FACTOR_05
              , FACTOR_06      AS FACTOR_06
              , FACTOR_07      AS FACTOR_07
              , FACTOR_08      AS FACTOR_08
              , FACTOR_09      AS FACTOR_09
              , FACTOR_10      AS FACTOR_10
              , FACTOR_11      AS FACTOR_11
              , FACTOR_12      AS FACTOR_12
              , FACTOR_13      AS FACTOR_13
              , FACTOR_14      AS FACTOR_14
              , FACTOR_15      AS FACTOR_15
              , FACTOR_16      AS FACTOR_16
              , FACTOR_17      AS FACTOR_17
              , FACTOR_18      AS FACTOR_18
              , FACTOR_19      AS FACTOR_19
              , FACTOR_20      AS FACTOR_20
              , FACTOR_21      AS FACTOR_21
              , FACTOR_22      AS FACTOR_22
              , FACTOR_23      AS FACTOR_23
              , FACTOR_24      AS FACTOR_24
              , FACTOR_25      AS FACTOR_25
              , FACTOR_26      AS FACTOR_26
              , FACTOR_27      AS FACTOR_27
              , FACTOR_28      AS FACTOR_28
              , FACTOR_29      AS FACTOR_29
              , FACTOR_30      AS FACTOR_30
              , FACTOR_31      AS FACTOR_31
              , FACTOR_32      AS FACTOR_32
              , FACTOR_33      AS FACTOR_33
              , FACTOR_34      AS FACTOR_34
              , FACTOR_35      AS FACTOR_35
              , FACTOR_36      AS FACTOR_36
              , FACTOR_37      AS FACTOR_37
              , FACTOR_38      AS FACTOR_38
              , FACTOR_39      AS FACTOR_39
              , FACTOR_40      AS FACTOR_40
              , FACTOR_41      AS FACTOR_41
              , FACTOR_42      AS FACTOR_42
              , FACTOR_43      AS FACTOR_43
              , FACTOR_44      AS FACTOR_44
              , FACTOR_45      AS FACTOR_45
              , FACTOR_46      AS FACTOR_46
              , FACTOR_47      AS FACTOR_47
              , FACTOR_48      AS FACTOR_48
              , FACTOR_49      AS FACTOR_49
              , S.PROD_WC_CD     AS PROD_WC_CD
              , TOP_BOTTOM     AS TOP_BOTTOM
              , MANA_NM_       AS MANA_NM_
              , S.WORK_GB        AS WORK_GB
              , U.PROD_CD     AS I_BE_PROD_CD
              , S.INSERT_USER      AS INSERT_USER
              , S_WORK_GB        AS S_WORK_GB
              , I_DISP_FACTOR_NM AS I_DISP_FACTOR_NM
              , ROWNUM           AS ROW_CNT
              , S.REJECT_REMARK    AS REJECT_REMARK
              , FACTOR_50        AS FACTOR_50
              , FACTOR_51        AS FACTOR_51
              , FACTOR_52        AS FACTOR_52
              , FACTOR_53        AS FACTOR_53
              , FACTOR_54        AS FACTOR_54
              , FACTOR_55        AS FACTOR_55
              , FACTOR_56        AS FACTOR_56
              , FACTOR_57        AS FACTOR_57
              , FACTOR_58        AS FACTOR_58
              , FACTOR_59        AS FACTOR_59
              , FACTOR_60        AS FACTOR_60
              , FACTOR_61        AS FACTOR_61
              , FACTOR_62        AS FACTOR_62
              , FACTOR_64        AS FACTOR_64
              , FACTOR_65        AS FACTOR_65
              , FACTOR_66        AS FACTOR_66
              , FACTOR_67        AS FACTOR_67
              , FACTOR_68        AS FACTOR_68
              , FACTOR_69        AS FACTOR_69
              , FACTOR_70        AS FACTOR_70
              , FACTOR_71        AS FACTOR_71
              , FACTOR_72        AS FACTOR_72
              , FACTOR_73        AS FACTOR_73
              , FACTOR_74        AS FACTOR_74
              , FACTOR_75        AS FACTOR_75
              , FACTOR_76        AS FACTOR_76
              , FACTOR_77        AS FACTOR_77
              , FACTOR_78        AS FACTOR_78
              , FACTOR_79        AS FACTOR_79
              , FACTOR_80        AS FACTOR_80
              , FACTOR_81        AS FACTOR_81
              , FACTOR_82        AS FACTOR_82
              , FACTOR_83        AS FACTOR_83
              , FACTOR_84        AS FACTOR_84
              , FACTOR_85        AS FACTOR_85
              , FACTOR_86        AS FACTOR_86
              , PROD_GROUP       AS PROD_GROUP
              , PDAP       AS PDAP
              , SUBSTR(I_BE_PROD_CD,7,4) AS E_TOP_TAC
              , NORMAL_FACTOR_CD AS NORMAL_FACTOR_CD
              , FACTOR_87        AS FACTOR_87
              , FACTOR_88        AS FACTOR_88
              , FACTOR_89        AS FACTOR_89
              , FACTOR_90        AS FACTOR_90
              , FACTOR_91        AS FACTOR_91
              , FACTOR_92        AS FACTOR_92
              , FACTOR_93        AS FACTOR_93
              , FACTOR_94        AS FACTOR_94
              , FACTOR_95        AS FACTOR_95
              , FACTOR_96        AS FACTOR_96
              , FACTOR_97        AS FACTOR_97
              , FACTOR_98        AS FACTOR_98
              , FACTOR_99        AS FACTOR_99
              , FACTOR_100        AS FACTOR_100
              , FACTOR_101        AS FACTOR_101
              , FACTOR_102        AS FACTOR_102
              , FACTOR_103        AS FACTOR_103
              , FACTOR_104        AS FACTOR_104
              , FACTOR_105        AS FACTOR_105
              , FACTOR_106        AS FACTOR_106
              , FACTOR_107        AS FACTOR_107
              , FACTOR_108        AS FACTOR_108
              , FACTOR_109        AS FACTOR_109
              , FACTOR_110        AS FACTOR_110
              , FACTOR_111        AS FACTOR_111
              , NORMAL_FACTOR_CD2   AS NORMAL_FACTOR_CD2
              , REWORK_INSP_DIV     AS REWORK_INSP_DIV
           FROM
                (
                SELECT R.WORK_GB            AS WORK_GB
                     , ROWNUM               AS ROW_CNT
                     , R.AR_WARHS_CREATE_NO AS AR_WARHS_CREATE_NO
                     , R.LOT_NO             AS LOT_NO
                     , R.I_BE_LOT_NO        AS I_BE_LOT_NO
                     , DECODE( R.PURCH_LOT_NO, '', F_ONE_PROD_TRACE_T( R.PLANT_CD, R.AR_WARHS_CREATE_NO, '_E%', '%%' ), F_ONE_PROD_TRACE_T( R.PLANT_CD, F_AR_NO_RETURN_T( R.PURCH_LOT_NO ), '_E%', '%%' ) )       AS I_BE_PROD_CD
                     , DECODE( R.PURCH_LOT_NO, '', F_AR_NO_RETURN(R.PLANT_CD,F_ONE_LOT_TRACE_T( R.AR_WARHS_CREATE_NO, '_E%', '%%' )), F_AR_NO_RETURN(R.PLANT_CD,F_ONE_LOT_TRACE_T( F_AR_NO_RETURN_T( R.PURCH_LOT_NO ), '_E%', '%%' )) )       AS I_BE_AR_NO
                     , R.IN_LOT_NO          AS IN_LOT_NO
                     , R.INSP_CLASS         AS INSP_CLASS
                     , R.PROD_DATE          AS PROD_DATE
                     , R.PROD_CD            AS PROD_CD
                     , R.PROD_NM            AS PROD_NM
                     , R.LENG               AS LENG
                     , R.MANA_NM_           AS MANA_NM_
                     , R.MANA_NM            AS MANA_NM
                     , R.PROD_SIZE          AS PROD_SIZE
                     , R.NORMAL_QTY         AS NORMAL_QTY
                     , R.QTY                AS QTY
                     , R.DISPRODUCT_QTY     AS DISPRODUCT_QTY
                     , R.GOOD_RATE||'%'     AS GOOD_RATE
                     , R.FACTOR_01          AS FACTOR_01
                     , R.FACTOR_02          AS FACTOR_02
                     , R.FACTOR_03          AS FACTOR_03
                     , R.FACTOR_04          AS FACTOR_04
                     , R.FACTOR_05          AS FACTOR_05
                     , R.FACTOR_06          AS FACTOR_06
                     , R.FACTOR_07          AS FACTOR_07
                     , R.FACTOR_08          AS FACTOR_08
                     , R.FACTOR_09          AS FACTOR_09
                     , R.FACTOR_10          AS FACTOR_10
                     , R.FACTOR_11          AS FACTOR_11
                     , R.FACTOR_12          AS FACTOR_12
                     , R.FACTOR_13          AS FACTOR_13
                     , R.FACTOR_14          AS FACTOR_14
                     , R.FACTOR_15          AS FACTOR_15
                     , R.FACTOR_16          AS FACTOR_16
                     , R.FACTOR_17          AS FACTOR_17
                     , R.FACTOR_18          AS FACTOR_18
                     , R.FACTOR_19          AS FACTOR_19
                     , R.FACTOR_20          AS FACTOR_20
                     , R.FACTOR_21          AS FACTOR_21
                     , R.FACTOR_22          AS FACTOR_22
                     , R.FACTOR_23          AS FACTOR_23
                     , R.FACTOR_24          AS FACTOR_24
                     , R.FACTOR_25          AS FACTOR_25
                     , R.FACTOR_26          AS FACTOR_26
                     , R.FACTOR_27          AS FACTOR_27
                     , R.FACTOR_28          AS FACTOR_28
                     , R.FACTOR_29          AS FACTOR_29
                     , R.FACTOR_30          AS FACTOR_30
                     , R.FACTOR_31          AS FACTOR_31
                     , R.FACTOR_32          AS FACTOR_32
                     , R.FACTOR_33          AS FACTOR_33
                     , R.FACTOR_34          AS FACTOR_34
                     , R.FACTOR_35          AS FACTOR_35
                     , R.FACTOR_36          AS FACTOR_36
                     , R.FACTOR_37          AS FACTOR_37
                     , R.FACTOR_38          AS FACTOR_38
                     , R.FACTOR_39          AS FACTOR_39
                     , R.FACTOR_40          AS FACTOR_40
                     , R.FACTOR_41          AS FACTOR_41
                     , R.FACTOR_42          AS FACTOR_42
                     , R.FACTOR_43          AS FACTOR_43
                     , R.FACTOR_44          AS FACTOR_44
                     , R.FACTOR_45          AS FACTOR_45
                     , R.FACTOR_46          AS FACTOR_46
                     , R.FACTOR_47          AS FACTOR_47
                     , R.FACTOR_48          AS FACTOR_48
                     , R.FACTOR_49          AS FACTOR_49
                     , R.FACTOR_50          AS FACTOR_50
                     , R.FACTOR_51          AS FACTOR_51
                     , R.FACTOR_52          AS FACTOR_52
                     , R.FACTOR_53          AS FACTOR_53
                     , R.FACTOR_54          AS FACTOR_54
                     , R.FACTOR_55          AS FACTOR_55
                     , R.FACTOR_56          AS FACTOR_56
                     , R.FACTOR_57          AS FACTOR_57
                     , R.FACTOR_58          AS FACTOR_58
                     , R.FACTOR_59          AS FACTOR_59
                     , R.FACTOR_60          AS FACTOR_60
                     , R.FACTOR_61          AS FACTOR_61
                     , R.FACTOR_62          AS FACTOR_62
                     , R.FACTOR_64          AS FACTOR_64
                     , R.FACTOR_65          AS FACTOR_65
                     , R.FACTOR_66          AS FACTOR_66
                     , R.FACTOR_67          AS FACTOR_67
                     , R.FACTOR_68          AS FACTOR_68
                     , R.FACTOR_69          AS FACTOR_69
                     , R.FACTOR_70          AS FACTOR_70
                     , R.FACTOR_71          AS FACTOR_71
                     , R.FACTOR_72          AS FACTOR_72
                     , R.FACTOR_73          AS FACTOR_73
                     , R.FACTOR_74          AS FACTOR_74
                     , R.FACTOR_75          AS FACTOR_75
                     , R.FACTOR_76          AS FACTOR_76
                     , R.FACTOR_77          AS FACTOR_77
                     , R.FACTOR_78          AS FACTOR_78
                     , R.FACTOR_79          AS FACTOR_79
                     , R.FACTOR_80          AS FACTOR_80
                     , R.FACTOR_81          AS FACTOR_81
                     , R.FACTOR_82          AS FACTOR_82
                     , R.FACTOR_83          AS FACTOR_83
                     , R.FACTOR_84          AS FACTOR_84
                     , R.FACTOR_85          AS FACTOR_85
                     , R.FACTOR_86          AS FACTOR_86
                     , R.INSERT_USER        AS INSERT_USER
                     , R.S_WORK_GB          AS S_WORK_GB
                     , R.PROD_WC_CD         AS PROD_WC_CD
                     , R.TOP_BOTTOM         AS TOP_BOTTOM
                     , R.PLANT_CD           AS PLANT_CD
                     , R.PURCH_LOT_NO       AS PURCH_LOT_NO
                     , R.I_DISP_FACTOR_NM   AS I_DISP_FACTOR_NM
                     , R.REJECT_REMARK      AS REJECT_REMARK
                     , R.PROD_GROUP         AS PROD_GROUP
                     , R.PDAP         AS PDAP
                     , R.E_TOP_TAC          AS E_TOP_TAC
                     , R.NORMAL_FACTOR_CD          AS NORMAL_FACTOR_CD
                     , R.FACTOR_87          AS FACTOR_87
                     , R.FACTOR_88          AS FACTOR_88
                     , R.FACTOR_89          AS FACTOR_89
                     , R.FACTOR_90          AS FACTOR_90
                     , R.FACTOR_91          AS FACTOR_91
                     , R.FACTOR_92          AS FACTOR_92
                     , R.FACTOR_93          AS FACTOR_93
                     , R.FACTOR_94          AS FACTOR_94
                     , R.FACTOR_95          AS FACTOR_95
                     , R.FACTOR_96          AS FACTOR_96
                     , R.FACTOR_97          AS FACTOR_97
                     , R.FACTOR_98          AS FACTOR_98
                     , R.FACTOR_99          AS FACTOR_99
                     , R.FACTOR_100          AS FACTOR_100
                     , R.FACTOR_101          AS FACTOR_101
                     , R.FACTOR_102          AS FACTOR_102
                     , R.FACTOR_103          AS FACTOR_103
                     , R.FACTOR_104          AS FACTOR_104
                     , R.FACTOR_105          AS FACTOR_105
                     , R.FACTOR_106          AS FACTOR_106
                     , R.FACTOR_107          AS FACTOR_107
                     , R.FACTOR_108          AS FACTOR_108
                     , R.FACTOR_109          AS FACTOR_109
                     , R.FACTOR_110          AS FACTOR_110
                     , R.FACTOR_111          AS FACTOR_111
                     , R.NORMAL_FACTOR_CD2          AS NORMAL_FACTOR_CD2
                     , R.REWORK_INSP_DIV            AS REWORK_INSP_DIV
                  FROM
                       (
                       SELECT MAX( DECODE( P.NO, 2, O.WORK_GB, '동시생산 유/무' ) )  AS WORK_GB
                            , DECODE( P.NO, 1, '00', 2, '00'||O.KEY1 )               AS KEY1
                            , MAX( DECODE( P.NO, 2, O.AR_WARHS_CREATE_NO, '' ) )     AS AR_WARHS_CREATE_NO
                            , MAX( DECODE( P.NO, 2, O.LOT_NO, 'LOT' ) )              AS LOT_NO
                            , MAX( DECODE( P.NO, 2, I_BE_LOT_NO, '연신LOT' ) )       AS I_BE_LOT_NO
                            , MAX( DECODE( P.NO, 2, I_BE_PROD_CD, '연신제품코드' ) ) AS I_BE_PROD_CD
                            , MAX( DECODE( P.NO, 2, IN_LOT_NO, '재단/재검LOT' ) )    AS IN_LOT_NO
                            , MAX( DECODE( P.NO, 2, O.PROD_SIZE, '규격' ) )          AS PROD_SIZE
                            , MAX( DECODE( P.NO, 2, O.LENG, '길이' ) )               AS LENG
                            , MAX( DECODE( P.NO, 2, O.PROD_CD, '제품코드' ) )        AS PROD_CD
                            , MAX( DECODE( P.NO, 2, O.TOP_BOTTOM, '상/하구분' ) )    AS TOP_BOTTOM
                            , MAX( DECODE( P.NO, 2, O.PROD_DATE, '생산일자' ) )      AS PROD_DATE
                            , MAX( DECODE( P.NO, 2, O.PROD_WC_CD, '검사실' ) )       AS PROD_WC_CD
                            , MAX( DECODE( P.NO, 2, O.INSP_CLASS, '검사등급' ) )     AS INSP_CLASS
                            , MAX( DECODE( P.NO, 2, O.PROD_NM, '제품명' ) )          AS PROD_NM
                            , MAX( DECODE( P.NO, 2, MANA_NM_, 'GRADE_' ) )           AS MANA_NM_
                            , MAX( DECODE( P.NO, 2, MANA_NM, 'GRADE' ) )             AS MANA_NM
                            , MAX( DECODE( P.NO, 2, TRIM( TO_CHAR( O.NORMAL_QTY, '999,999,999' ) ), '생산량' ) )                    AS NORMAL_QTY
                            , MAX( DECODE( P.NO, 2, TRIM( TO_CHAR( O.NORMAL_QTY - O.DISPRODUCT_QTY, '999,999,999' ) ), '양품량' ) ) AS QTY
                            , MAX( DECODE( P.NO, 2, TRIM( TO_CHAR( O.DISPRODUCT_QTY, '999,999,999' ) ), '불량' ) )                  AS DISPRODUCT_QTY
                            , MAX( DECODE( P.NO, 2, TRIM( TO_CHAR( F_RATE( O.NORMAL_QTY - O.DISPRODUCT_QTY, O.NORMAL_QTY, 2 ), '999.9' ) ), '양품율' ) ) AS GOOD_RATE
                            , MAX( DECODE( P.NO, 1, O.FACTOR_01_NM, TRIM( TO_CHAR( O.FACTOR_01_QTY, '999,999,999' ) ) ) )                             AS FACTOR_01
                            , MAX( DECODE( P.NO, 1, O.FACTOR_02_NM, TRIM( TO_CHAR( O.FACTOR_02_QTY, '999,999,999' ) ) ) )                             AS FACTOR_02
                            , MAX( DECODE( P.NO, 1, O.FACTOR_03_NM, TRIM( TO_CHAR( O.FACTOR_03_QTY, '999,999,999' ) ) ) )                             AS FACTOR_03
                            , MAX( DECODE( P.NO, 1, O.FACTOR_04_NM, TRIM( TO_CHAR( O.FACTOR_04_QTY, '999,999,999' ) ) ) )                             AS FACTOR_04
                            , MAX( DECODE( P.NO, 1, O.FACTOR_05_NM, TRIM( TO_CHAR( O.FACTOR_05_QTY, '999,999,999' ) ) ) )                             AS FACTOR_05
                            , MAX( DECODE( P.NO, 1, O.FACTOR_06_NM, TRIM( TO_CHAR( O.FACTOR_06_QTY, '999,999,999' ) ) ) )                             AS FACTOR_06
                            , MAX( DECODE( P.NO, 1, O.FACTOR_07_NM, TRIM( TO_CHAR( O.FACTOR_07_QTY, '999,999,999' ) ) ) )                             AS FACTOR_07
                            , MAX( DECODE( P.NO, 1, O.FACTOR_08_NM, TRIM( TO_CHAR( O.FACTOR_08_QTY, '999,999,999' ) ) ) )                             AS FACTOR_08
                            , MAX( DECODE( P.NO, 1, O.FACTOR_09_NM, TRIM( TO_CHAR( O.FACTOR_09_QTY, '999,999,999' ) ) ) )                             AS FACTOR_09
                            , MAX( DECODE( P.NO, 1, O.FACTOR_10_NM, TRIM( TO_CHAR( O.FACTOR_10_QTY, '999,999,999' ) ) ) )                             AS FACTOR_10
                            , MAX( DECODE( P.NO, 1, O.FACTOR_11_NM, TRIM( TO_CHAR( O.FACTOR_11_QTY, '999,999,999' ) ) ) )                             AS FACTOR_11
                            , MAX( DECODE( P.NO, 1, O.FACTOR_12_NM, TRIM( TO_CHAR( O.FACTOR_12_QTY, '999,999,999' ) ) ) )                             AS FACTOR_12
                            , MAX( DECODE( P.NO, 1, O.FACTOR_13_NM, TRIM( TO_CHAR( O.FACTOR_13_QTY, '999,999,999' ) ) ) )                             AS FACTOR_13
                            , MAX( DECODE( P.NO, 1, O.FACTOR_14_NM, TRIM( TO_CHAR( O.FACTOR_14_QTY, '999,999,999' ) ) ) )                             AS FACTOR_14
                            , MAX( DECODE( P.NO, 1, O.FACTOR_15_NM, TRIM( TO_CHAR( O.FACTOR_15_QTY, '999,999,999' ) ) ) )                             AS FACTOR_15
                            , MAX( DECODE( P.NO, 1, O.FACTOR_16_NM, TRIM( TO_CHAR( O.FACTOR_16_QTY, '999,999,999' ) ) ) )                             AS FACTOR_16
                            , MAX( DECODE( P.NO, 1, O.FACTOR_17_NM, TRIM( TO_CHAR( O.FACTOR_17_QTY, '999,999,999' ) ) ) )                             AS FACTOR_17
                            , MAX( DECODE( P.NO, 1, O.FACTOR_18_NM, TRIM( TO_CHAR( O.FACTOR_18_QTY, '999,999,999' ) ) ) )                             AS FACTOR_18
                            , MAX( DECODE( P.NO, 1, O.FACTOR_19_NM, TRIM( TO_CHAR( O.FACTOR_19_QTY, '999,999,999' ) ) ) )                             AS FACTOR_19
                            , MAX( DECODE( P.NO, 1, O.FACTOR_20_NM, TRIM( TO_CHAR( O.FACTOR_20_QTY, '999,999,999' ) ) ) )                             AS FACTOR_20
                            , MAX( DECODE( P.NO, 1, O.FACTOR_21_NM, TRIM( TO_CHAR( O.FACTOR_21_QTY, '999,999,999' ) ) ) )                             AS FACTOR_21
                            , MAX( DECODE( P.NO, 1, O.FACTOR_22_NM, TRIM( TO_CHAR( O.FACTOR_22_QTY, '999,999,999' ) ) ) )                             AS FACTOR_22
                            , MAX( DECODE( P.NO, 1, O.FACTOR_23_NM, TRIM( TO_CHAR( O.FACTOR_23_QTY, '999,999,999' ) ) ) )                             AS FACTOR_23
                            , MAX( DECODE( P.NO, 1, O.FACTOR_24_NM, TRIM( TO_CHAR( O.FACTOR_24_QTY, '999,999,999' ) ) ) )                             AS FACTOR_24
                            , MAX( DECODE( P.NO, 1, O.FACTOR_25_NM, TRIM( TO_CHAR( O.FACTOR_25_QTY, '999,999,999' ) ) ) )                             AS FACTOR_25
                            , MAX( DECODE( P.NO, 1, O.FACTOR_26_NM, TRIM( TO_CHAR( O.FACTOR_26_QTY, '999,999,999' ) ) ) )                             AS FACTOR_26
                            , MAX( DECODE( P.NO, 1, O.FACTOR_27_NM, TRIM( TO_CHAR( O.FACTOR_27_QTY, '999,999,999' ) ) ) )                             AS FACTOR_27
                            , MAX( DECODE( P.NO, 1, O.FACTOR_28_NM, TRIM( TO_CHAR( O.FACTOR_28_QTY, '999,999,999' ) ) ) )                             AS FACTOR_28
                            , MAX( DECODE( P.NO, 1, O.FACTOR_29_NM, TRIM( TO_CHAR( O.FACTOR_29_QTY, '999,999,999' ) ) ) )                             AS FACTOR_29
                            , MAX( DECODE( P.NO, 1, O.FACTOR_30_NM, TRIM( TO_CHAR( O.FACTOR_30_QTY, '999,999,999' ) ) ) )                             AS FACTOR_30
                            , MAX( DECODE( P.NO, 1, O.FACTOR_31_NM, TRIM( TO_CHAR( O.FACTOR_31_QTY, '999,999,999' ) ) ) )                             AS FACTOR_31
                            , MAX( DECODE( P.NO, 1, O.FACTOR_32_NM, TRIM( TO_CHAR( O.FACTOR_32_QTY, '999,999,999' ) ) ) )                             AS FACTOR_32
                            , MAX( DECODE( P.NO, 1, O.FACTOR_33_NM, TRIM( TO_CHAR( O.FACTOR_33_QTY, '999,999,999' ) ) ) )                             AS FACTOR_33
                            , MAX( DECODE( P.NO, 1, O.FACTOR_34_NM, TRIM( TO_CHAR( O.FACTOR_34_QTY, '999,999,999' ) ) ) )                             AS FACTOR_34
                            , MAX( DECODE( P.NO, 1, O.FACTOR_35_NM, TRIM( TO_CHAR( O.FACTOR_35_QTY, '999,999,999' ) ) ) )                             AS FACTOR_35
                            , MAX( DECODE( P.NO, 1, O.FACTOR_36_NM, TRIM( TO_CHAR( O.FACTOR_36_QTY, '999,999,999' ) ) ) )                             AS FACTOR_36
                            , MAX( DECODE( P.NO, 1, O.FACTOR_37_NM, TRIM( TO_CHAR( O.FACTOR_37_QTY, '999,999,999' ) ) ) )                             AS FACTOR_37
                            , MAX( DECODE( P.NO, 1, O.FACTOR_38_NM, TRIM( TO_CHAR( O.FACTOR_38_QTY, '999,999,999' ) ) ) )                             AS FACTOR_38
                            , MAX( DECODE( P.NO, 1, O.FACTOR_39_NM, TRIM( TO_CHAR( O.FACTOR_39_QTY, '999,999,999' ) ) ) )                             AS FACTOR_39
                            , MAX( DECODE( P.NO, 1, O.FACTOR_40_NM, TRIM( TO_CHAR( O.FACTOR_40_QTY, '999,999,999' ) ) ) )                             AS FACTOR_40
                            , MAX( DECODE( P.NO, 1, O.FACTOR_41_NM, TRIM( TO_CHAR( O.FACTOR_41_QTY, '999,999,999' ) ) ) )                             AS FACTOR_41
                            , MAX( DECODE( P.NO, 1, O.FACTOR_42_NM, TRIM( TO_CHAR( O.FACTOR_42_QTY, '999,999,999' ) ) ) )                             AS FACTOR_42
                            , MAX( DECODE( P.NO, 1, O.FACTOR_43_NM, TRIM( TO_CHAR( O.FACTOR_43_QTY, '999,999,999' ) ) ) )                             AS FACTOR_43
                            , MAX( DECODE( P.NO, 1, O.FACTOR_44_NM, TRIM( TO_CHAR( O.FACTOR_44_QTY, '999,999,999' ) ) ) )                             AS FACTOR_44
                            , MAX( DECODE( P.NO, 1, O.FACTOR_45_NM, TRIM( TO_CHAR( O.FACTOR_45_QTY, '999,999,999' ) ) ) )                             AS FACTOR_45
                            , MAX( DECODE( P.NO, 1, O.FACTOR_46_NM, TRIM( TO_CHAR( O.FACTOR_46_QTY, '999,999,999' ) ) ) )                             AS FACTOR_46
                            , MAX( DECODE( P.NO, 1, O.FACTOR_47_NM, TRIM( TO_CHAR( O.FACTOR_47_QTY, '999,999,999' ) ) ) )                             AS FACTOR_47
                            , MAX( DECODE( P.NO, 1, O.FACTOR_48_NM, TRIM( TO_CHAR( O.FACTOR_48_QTY, '999,999,999' ) ) ) )                             AS FACTOR_48
                            , MAX( DECODE( P.NO, 1, O.FACTOR_49_NM, TRIM( TO_CHAR( O.FACTOR_49_QTY, '999,999,999' ) ) ) )                             AS FACTOR_49
                            , MAX( DECODE( P.NO, 1, O.FACTOR_50_NM, TRIM( TO_CHAR( O.FACTOR_50_QTY, '999,999,999' ) ) ) )                             AS FACTOR_50
                            , MAX( DECODE( P.NO, 1, O.FACTOR_51_NM, TRIM( TO_CHAR( O.FACTOR_51_QTY, '999,999,999' ) ) ) )                             AS FACTOR_51
                            , MAX( DECODE( P.NO, 1, O.FACTOR_52_NM, TRIM( TO_CHAR( O.FACTOR_52_QTY, '999,999,999' ) ) ) )                             AS FACTOR_52
                            , MAX( DECODE( P.NO, 1, O.FACTOR_53_NM, TRIM( TO_CHAR( O.FACTOR_53_QTY, '999,999,999' ) ) ) )                             AS FACTOR_53
                            , MAX( DECODE( P.NO, 1, O.FACTOR_54_NM, TRIM( TO_CHAR( O.FACTOR_54_QTY, '999,999,999' ) ) ) )                             AS FACTOR_54
                            , MAX( DECODE( P.NO, 1, O.FACTOR_55_NM, TRIM( TO_CHAR( O.FACTOR_55_QTY, '999,999,999' ) ) ) )                             AS FACTOR_55
                            , MAX( DECODE( P.NO, 1, O.FACTOR_56_NM, TRIM( TO_CHAR( O.FACTOR_56_QTY, '999,999,999' ) ) ) )                             AS FACTOR_56
                            , MAX( DECODE( P.NO, 1, O.FACTOR_57_NM, TRIM( TO_CHAR( O.FACTOR_57_QTY, '999,999,999' ) ) ) )                             AS FACTOR_57
                            , MAX( DECODE( P.NO, 1, O.FACTOR_58_NM, TRIM( TO_CHAR( O.FACTOR_58_QTY, '999,999,999' ) ) ) )                             AS FACTOR_58
                            , MAX( DECODE( P.NO, 1, O.FACTOR_59_NM, TRIM( TO_CHAR( O.FACTOR_59_QTY, '999,999,999' ) ) ) )                             AS FACTOR_59
                            , MAX( DECODE( P.NO, 1, O.FACTOR_60_NM, TRIM( TO_CHAR( O.FACTOR_60_QTY, '999,999,999' ) ) ) )                             AS FACTOR_60
                            , MAX( DECODE( P.NO, 1, O.FACTOR_61_NM, TRIM( TO_CHAR( O.FACTOR_61_QTY, '999,999,999' ) ) ) )                             AS FACTOR_61
                            , MAX( DECODE( P.NO, 1, O.FACTOR_62_NM, TRIM( TO_CHAR( O.FACTOR_62_QTY, '999,999,999' ) ) ) )                             AS FACTOR_62
                            , MAX( DECODE( P.NO, 1, O.FACTOR_64_NM, TRIM( TO_CHAR( O.FACTOR_64_QTY, '999,999,999' ) ) ) )                             AS FACTOR_64
                            , MAX( DECODE( P.NO, 1, O.FACTOR_65_NM, TRIM( TO_CHAR( O.FACTOR_65_QTY, '999,999,999' ) ) ) )                             AS FACTOR_65
                            , MAX( DECODE( P.NO, 1, O.FACTOR_66_NM, TRIM( TO_CHAR( O.FACTOR_66_QTY, '999,999,999' ) ) ) )                             AS FACTOR_66
                            , MAX( DECODE( P.NO, 1, O.FACTOR_67_NM, TRIM( TO_CHAR( O.FACTOR_67_QTY, '999,999,999' ) ) ) )                             AS FACTOR_67
                            , MAX( DECODE( P.NO, 1, O.FACTOR_68_NM, TRIM( TO_CHAR( O.FACTOR_68_QTY, '999,999,999' ) ) ) )                             AS FACTOR_68
                            , MAX( DECODE( P.NO, 1, O.FACTOR_69_NM, TRIM( TO_CHAR( O.FACTOR_69_QTY, '999,999,999' ) ) ) )                             AS FACTOR_69
                            , MAX( DECODE( P.NO, 1, O.FACTOR_70_NM, TRIM( TO_CHAR( O.FACTOR_70_QTY, '999,999,999' ) ) ) )                             AS FACTOR_70
                            , MAX( DECODE( P.NO, 1, O.FACTOR_71_NM, TRIM( TO_CHAR( O.FACTOR_71_QTY, '999,999,999' ) ) ) )                             AS FACTOR_71
                            , MAX( DECODE( P.NO, 1, O.FACTOR_72_NM, TRIM( TO_CHAR( O.FACTOR_72_QTY, '999,999,999' ) ) ) )                             AS FACTOR_72
                            , MAX( DECODE( P.NO, 1, O.FACTOR_73_NM, TRIM( TO_CHAR( O.FACTOR_73_QTY, '999,999,999' ) ) ) )                             AS FACTOR_73
                            , MAX( DECODE( P.NO, 1, O.FACTOR_74_NM, TRIM( TO_CHAR( O.FACTOR_74_QTY, '999,999,999' ) ) ) )                             AS FACTOR_74
                            , MAX( DECODE( P.NO, 1, O.FACTOR_75_NM, TRIM( TO_CHAR( O.FACTOR_75_QTY, '999,999,999' ) ) ) )                             AS FACTOR_75
                            , MAX( DECODE( P.NO, 1, O.FACTOR_76_NM, TRIM( TO_CHAR( O.FACTOR_76_QTY, '999,999,999' ) ) ) )                             AS FACTOR_76
                            , MAX( DECODE( P.NO, 1, O.FACTOR_77_NM, TRIM( TO_CHAR( O.FACTOR_77_QTY, '999,999,999' ) ) ) )                             AS FACTOR_77
                            , MAX( DECODE( P.NO, 1, O.FACTOR_78_NM, TRIM( TO_CHAR( O.FACTOR_78_QTY, '999,999,999' ) ) ) )                             AS FACTOR_78
                            , MAX( DECODE( P.NO, 1, O.FACTOR_79_NM, TRIM( TO_CHAR( O.FACTOR_79_QTY, '999,999,999' ) ) ) )                             AS FACTOR_79
                            , MAX( DECODE( P.NO, 1, O.FACTOR_80_NM, TRIM( TO_CHAR( O.FACTOR_80_QTY, '999,999,999' ) ) ) )                             AS FACTOR_80
                            , MAX( DECODE( P.NO, 1, O.FACTOR_81_NM, TRIM( TO_CHAR( O.FACTOR_81_QTY, '999,999,999' ) ) ) )                             AS FACTOR_81
                            , MAX( DECODE( P.NO, 1, O.FACTOR_82_NM, TRIM( TO_CHAR( O.FACTOR_82_QTY, '999,999,999' ) ) ) )                             AS FACTOR_82
                            , MAX( DECODE( P.NO, 1, O.FACTOR_83_NM, TRIM( TO_CHAR( O.FACTOR_83_QTY, '999,999,999' ) ) ) )                             AS FACTOR_83
                            , MAX( DECODE( P.NO, 1, O.FACTOR_84_NM, TRIM( TO_CHAR( O.FACTOR_84_QTY, '999,999,999' ) ) ) )                             AS FACTOR_84
                            , MAX( DECODE( P.NO, 1, O.FACTOR_85_NM, TRIM( TO_CHAR( O.FACTOR_85_QTY, '999,999,999' ) ) ) )                             AS FACTOR_85
                            , MAX( DECODE( P.NO, 1, O.FACTOR_86_NM, TRIM( TO_CHAR( O.FACTOR_86_QTY, '999,999,999' ) ) ) )                             AS FACTOR_86
                            , MAX( DECODE( P.NO, 2, O.INSERT_USER, '대표검사원' ) )                                                                   AS INSERT_USER
                            , MAX( DECODE( P.NO, 2, O.PLANT_CD, '' ) )                                                                                AS PLANT_CD
                            , MAX( DECODE( P.NO, 2, O.PURCH_LOT_NO, '' ) )                                                                            AS PURCH_LOT_NO
                            , MAX( DECODE( P.NO, 2, O.S_WORK_GB, '작업구분' ) )                                                                       AS S_WORK_GB
                            , MAX( DECODE( P.NO, 2, O.I_DISP_FACTOR_NM, '재가공요인' ) )                                                              AS I_DISP_FACTOR_NM
                            , MAX( DECODE( P.NO, 2, O.REJECT_REMARK, '비 고' ) )                                                                      AS REJECT_REMARK
                            , MAX( DECODE( P.NO, 2, O.PROD_GROUP, 'PROD_GROUP' ) )   AS PROD_GROUP
                            , MAX( DECODE( P.NO, 2, O.PDAP, 'PDAP' ) )               AS PDAP
                            , MAX( DECODE( P.NO, 2, O.E_TOP_TAC, '상TAC' ) )         AS E_TOP_TAC
                            , MAX( DECODE( P.NO, 2, O.NORMAL_FACTOR_CD, '일반검사 사유' ) )         AS NORMAL_FACTOR_CD
                            , MAX( DECODE( P.NO, 1, O.FACTOR_87_NM, TRIM( TO_CHAR( O.FACTOR_87_QTY, '999,999,999' ) ) ) )                             AS FACTOR_87
                            , MAX( DECODE( P.NO, 1, O.FACTOR_88_NM, TRIM( TO_CHAR( O.FACTOR_88_QTY, '999,999,999' ) ) ) )                             AS FACTOR_88
                            , MAX( DECODE( P.NO, 1, O.FACTOR_89_NM, TRIM( TO_CHAR( O.FACTOR_89_QTY, '999,999,999' ) ) ) )                             AS FACTOR_89
                            , MAX( DECODE( P.NO, 1, O.FACTOR_90_NM, TRIM( TO_CHAR( O.FACTOR_90_QTY, '999,999,999' ) ) ) )                             AS FACTOR_90
                            , MAX( DECODE( P.NO, 1, O.FACTOR_91_NM, TRIM( TO_CHAR( O.FACTOR_91_QTY, '999,999,999' ) ) ) )                             AS FACTOR_91
                            , MAX( DECODE( P.NO, 1, O.FACTOR_92_NM, TRIM( TO_CHAR( O.FACTOR_92_QTY, '999,999,999' ) ) ) )                             AS FACTOR_92
                            , MAX( DECODE( P.NO, 1, O.FACTOR_93_NM, TRIM( TO_CHAR( O.FACTOR_93_QTY, '999,999,999' ) ) ) )                             AS FACTOR_93
                            , MAX( DECODE( P.NO, 1, O.FACTOR_94_NM, TRIM( TO_CHAR( O.FACTOR_94_QTY, '999,999,999' ) ) ) )                             AS FACTOR_94
                            , MAX( DECODE( P.NO, 1, O.FACTOR_95_NM, TRIM( TO_CHAR( O.FACTOR_95_QTY, '999,999,999' ) ) ) )                             AS FACTOR_95
                            , MAX( DECODE( P.NO, 1, O.FACTOR_96_NM, TRIM( TO_CHAR( O.FACTOR_96_QTY, '999,999,999' ) ) ) )                             AS FACTOR_96
                            , MAX( DECODE( P.NO, 1, O.FACTOR_97_NM, TRIM( TO_CHAR( O.FACTOR_97_QTY, '999,999,999' ) ) ) )                             AS FACTOR_97
                            , MAX( DECODE( P.NO, 1, O.FACTOR_98_NM, TRIM( TO_CHAR( O.FACTOR_98_QTY, '999,999,999' ) ) ) )                             AS FACTOR_98
                            , MAX( DECODE( P.NO, 1, O.FACTOR_99_NM, TRIM( TO_CHAR( O.FACTOR_99_QTY, '999,999,999' ) ) ) )                             AS FACTOR_99
                            , MAX( DECODE( P.NO, 1, O.FACTOR_100_NM, TRIM( TO_CHAR( O.FACTOR_100_QTY, '999,999,999' ) ) ) )                             AS FACTOR_100
                            , MAX( DECODE( P.NO, 1, O.FACTOR_101_NM, TRIM( TO_CHAR( O.FACTOR_101_QTY, '999,999,999' ) ) ) )                             AS FACTOR_101
                            , MAX( DECODE( P.NO, 1, O.FACTOR_102_NM, TRIM( TO_CHAR( O.FACTOR_102_QTY, '999,999,999' ) ) ) )                             AS FACTOR_102
                            , MAX( DECODE( P.NO, 1, O.FACTOR_103_NM, TRIM( TO_CHAR( O.FACTOR_103_QTY, '999,999,999' ) ) ) )                             AS FACTOR_103
                            , MAX( DECODE( P.NO, 1, O.FACTOR_104_NM, TRIM( TO_CHAR( O.FACTOR_104_QTY, '999,999,999' ) ) ) )                             AS FACTOR_104
                            , MAX( DECODE( P.NO, 1, O.FACTOR_105_NM, TRIM( TO_CHAR( O.FACTOR_105_QTY, '999,999,999' ) ) ) )                             AS FACTOR_105
                            , MAX( DECODE( P.NO, 1, O.FACTOR_106_NM, TRIM( TO_CHAR( O.FACTOR_106_QTY, '999,999,999' ) ) ) )                             AS FACTOR_106
                            , MAX( DECODE( P.NO, 1, O.FACTOR_107_NM, TRIM( TO_CHAR( O.FACTOR_107_QTY, '999,999,999' ) ) ) )                             AS FACTOR_107
                            , MAX( DECODE( P.NO, 1, O.FACTOR_108_NM, TRIM( TO_CHAR( O.FACTOR_108_QTY, '999,999,999' ) ) ) )                             AS FACTOR_108
                            , MAX( DECODE( P.NO, 1, O.FACTOR_109_NM, TRIM( TO_CHAR( O.FACTOR_109_QTY, '999,999,999' ) ) ) )                             AS FACTOR_109
                            , MAX( DECODE( P.NO, 1, O.FACTOR_110_NM, TRIM( TO_CHAR( O.FACTOR_110_QTY, '999,999,999' ) ) ) )                             AS FACTOR_110
                            , MAX( DECODE( P.NO, 1, O.FACTOR_111_NM, TRIM( TO_CHAR( O.FACTOR_111_QTY, '999,999,999' ) ) ) )                             AS FACTOR_111
                            , MAX( DECODE( P.NO, 2, O.NORMAL_FACTOR_CD2, '일반검사 사유2' ) )         AS NORMAL_FACTOR_CD2
                            , MAX( DECODE( P.NO, 2, O.REWORK_INSP_DIV, '재가공 검사구분' ) )         AS REWORK_INSP_DIV
                         FROM
                              (
                              SELECT MAX( DECODE( K.NO, 2, J.WORK_GB, '' ) ) AS WORK_GB
                                   , DECODE( K.NO, 1, '0000', 2, '0000'||J.IN_LOT_NO||J.AR_WARHS_CREATE_NO ) AS KEY1
                                   , MAX( J.PLANT_CD )                                                       AS PLANT_CD
                                   , MAX( DECODE( K.NO, 2, J.WC_NM, '' ) )                                   AS PROD_WC_CD
                                   , MAX( DECODE( K.NO, 2, J.TOP_BOTTOM, '' ) )                              AS TOP_BOTTOM
                                   , MAX( DECODE( K.NO, 2, J.AR_WARHS_CREATE_NO ) )                          AS AR_WARHS_CREATE_NO
                                   , MAX( DECODE( K.NO, 2, J.LOT_NO, '' ) )                                  AS LOT_NO
                                   , MAX( DECODE( K.NO, 2, J.PROD_SIZE, '' ) )                               AS PROD_SIZE
                                   , MAX( DECODE( K.NO, 2, J.PROD_CD, '' ) )                                 AS PROD_CD
                                   , MAX( DECODE( K.NO, 2, J.LENG, '' ) )                                    AS LENG
                                   , MAX( DECODE( K.NO, 2, J.PROD_DATE, '' ) )                               AS PROD_DATE
                                   , MAX( DECODE( K.NO, 2, J.INSP_CLASS, '' ) )                              AS INSP_CLASS
                                   , MAX( DECODE( K.NO, 2, J.I_BE_LOT_NO, '' ) )                             AS I_BE_LOT_NO
                                   , MAX( DECODE( K.NO, 2, J.I_BE_PROD_CD, '' ) )                            AS I_BE_PROD_CD
                                   , MAX( DECODE( K.NO, 2, DECODE(SUBSTR(J.IN_LOT_NO,10,1),'N',F_FIND_INPUT_LOT(J.PLANT_CD,F_AR_NO_RETURN_T(J.IN_LOT_NO)),'U', F_ONE_LOT_TRACE_T( J.AR_WARHS_CREATE_NO, '%S%', '%' ),J.IN_LOT_NO), '' ))                               AS IN_LOT_NO
                                   , MAX( DECODE( K.NO, 2, J.PROD_NM, '[합      계]' ) )                     AS PROD_NM
                                   , MAX( DECODE( K.NO, 2, J.MANA_NO, '' ) )                                 AS MANA_NM_
                                   , MAX( DECODE( K.NO, 2, J.MANA_NM, '' ) )                                 AS MANA_NM
                                   , SUM( J.NORMAL_QTY )                                                     AS NORMAL_QTY
                                   , SUM( J.DISPRODUCT_QTY )                                                 AS DISPRODUCT_QTY
                                   , MAX( J.FACTOR_01_NM )                                                   AS FACTOR_01_NM
                                   , SUM( J.FACTOR_01_QTY )                                                  AS FACTOR_01_QTY
                                   , MAX( J.FACTOR_02_NM )                                                   AS FACTOR_02_NM
                                   , SUM( J.FACTOR_02_QTY )                                                  AS FACTOR_02_QTY
                                   , MAX( J.FACTOR_03_NM )                                                   AS FACTOR_03_NM
                                   , SUM( J.FACTOR_03_QTY )                                                  AS FACTOR_03_QTY
                                   , MAX( J.FACTOR_04_NM )                                                   AS FACTOR_04_NM
                                   , SUM( J.FACTOR_04_QTY )                                                  AS FACTOR_04_QTY
                                   , MAX( J.FACTOR_05_NM )                                                   AS FACTOR_05_NM
                                   , SUM( J.FACTOR_05_QTY )                                                  AS FACTOR_05_QTY
                                   , MAX( J.FACTOR_06_NM )                                                   AS FACTOR_06_NM
                                   , SUM( J.FACTOR_06_QTY )                                                  AS FACTOR_06_QTY
                                   , MAX( J.FACTOR_07_NM )                                                   AS FACTOR_07_NM
                                   , SUM( J.FACTOR_07_QTY )                                                  AS FACTOR_07_QTY
                                   , MAX( J.FACTOR_08_NM )                                                   AS FACTOR_08_NM
                                   , SUM( J.FACTOR_08_QTY )                                                  AS FACTOR_08_QTY
                                   , MAX( J.FACTOR_09_NM )                                                   AS FACTOR_09_NM
                                   , SUM( J.FACTOR_09_QTY )                                                  AS FACTOR_09_QTY
                                   , MAX( J.FACTOR_10_NM )                                                   AS FACTOR_10_NM
                                   , SUM( J.FACTOR_10_QTY )                                                  AS FACTOR_10_QTY
                                   , MAX( J.FACTOR_11_NM )                                                   AS FACTOR_11_NM
                                   , SUM( J.FACTOR_11_QTY )                                                  AS FACTOR_11_QTY
                                   , MAX( J.FACTOR_12_NM )                                                   AS FACTOR_12_NM
                                   , SUM( J.FACTOR_12_QTY )                                                  AS FACTOR_12_QTY
                                   , MAX( J.FACTOR_13_NM )                                                   AS FACTOR_13_NM
                                   , SUM( J.FACTOR_13_QTY )                                                  AS FACTOR_13_QTY
                                   , MAX( J.FACTOR_14_NM )                                                   AS FACTOR_14_NM
                                   , SUM( J.FACTOR_14_QTY )                                                  AS FACTOR_14_QTY
                                   , MAX( J.FACTOR_15_NM )                                                   AS FACTOR_15_NM
                                   , SUM( J.FACTOR_15_QTY )                                                  AS FACTOR_15_QTY
                                   , MAX( J.FACTOR_16_NM )                                                   AS FACTOR_16_NM
                                   , SUM( J.FACTOR_16_QTY )                                                  AS FACTOR_16_QTY
                                   , MAX( J.FACTOR_17_NM )                                                   AS FACTOR_17_NM
                                   , SUM( J.FACTOR_17_QTY )                                                  AS FACTOR_17_QTY
                                   , MAX( J.FACTOR_18_NM )                                                   AS FACTOR_18_NM
                                   , SUM( J.FACTOR_18_QTY )                                                  AS FACTOR_18_QTY
                                   , MAX( J.FACTOR_19_NM )                                                   AS FACTOR_19_NM
                                   , SUM( J.FACTOR_19_QTY )                                                  AS FACTOR_19_QTY
                                   , MAX( J.FACTOR_20_NM )                                                   AS FACTOR_20_NM
                                   , SUM( J.FACTOR_20_QTY )                                                  AS FACTOR_20_QTY
                                   , MAX( J.FACTOR_21_NM )                                                   AS FACTOR_21_NM
                                   , SUM( J.FACTOR_21_QTY )                                                  AS FACTOR_21_QTY
                                   , MAX( J.FACTOR_22_NM )                                                   AS FACTOR_22_NM
                                   , SUM( J.FACTOR_22_QTY )                                                  AS FACTOR_22_QTY
                                   , MAX( J.FACTOR_23_NM )                                                   AS FACTOR_23_NM
                                   , SUM( J.FACTOR_23_QTY )                                                  AS FACTOR_23_QTY
                                   , MAX( J.FACTOR_24_NM )                                                   AS FACTOR_24_NM
                                   , SUM( J.FACTOR_24_QTY )                                                  AS FACTOR_24_QTY
                                   , MAX( J.FACTOR_25_NM )                                                   AS FACTOR_25_NM
                                   , SUM( J.FACTOR_25_QTY )                                                  AS FACTOR_25_QTY
                                   , MAX( J.FACTOR_26_NM )                                                   AS FACTOR_26_NM
                                   , SUM( J.FACTOR_26_QTY )                                                  AS FACTOR_26_QTY
                                   , MAX( J.FACTOR_27_NM )                                                   AS FACTOR_27_NM
                                   , SUM( J.FACTOR_27_QTY )                                                  AS FACTOR_27_QTY
                                   , MAX( J.FACTOR_28_NM )                                                   AS FACTOR_28_NM
                                   , SUM( J.FACTOR_28_QTY )                                                  AS FACTOR_28_QTY
                                   , MAX( J.FACTOR_29_NM )                                                   AS FACTOR_29_NM
                                   , SUM( J.FACTOR_29_QTY )                                                  AS FACTOR_29_QTY
                                   , MAX( J.FACTOR_30_NM )                                                   AS FACTOR_30_NM
                                   , SUM( J.FACTOR_30_QTY )                                                  AS FACTOR_30_QTY
                                   , MAX( J.FACTOR_31_NM )                                                   AS FACTOR_31_NM
                                   , SUM( J.FACTOR_31_QTY )                                                  AS FACTOR_31_QTY
                                   , MAX( J.FACTOR_32_NM )                                                   AS FACTOR_32_NM
                                   , SUM( J.FACTOR_32_QTY )                                                  AS FACTOR_32_QTY
                                   , MAX( J.FACTOR_33_NM )                                                   AS FACTOR_33_NM
                                   , SUM( J.FACTOR_33_QTY )                                                  AS FACTOR_33_QTY
                                   , MAX( J.FACTOR_34_NM )                                                   AS FACTOR_34_NM
                                   , SUM( J.FACTOR_34_QTY )                                                  AS FACTOR_34_QTY
                                   , MAX( J.FACTOR_35_NM )                                                   AS FACTOR_35_NM
                                   , SUM( J.FACTOR_35_QTY )                                                  AS FACTOR_35_QTY
                                   , MAX( J.FACTOR_36_NM )                                                   AS FACTOR_36_NM
                                   , SUM( J.FACTOR_36_QTY )                                                  AS FACTOR_36_QTY
                                   , MAX( J.FACTOR_37_NM )                                                   AS FACTOR_37_NM
                                   , SUM( J.FACTOR_37_QTY )                                                  AS FACTOR_37_QTY
                                   , MAX( J.FACTOR_38_NM )                                                   AS FACTOR_38_NM
                                   , SUM( J.FACTOR_38_QTY )                                                  AS FACTOR_38_QTY
                                   , MAX( J.FACTOR_39_NM )                                                   AS FACTOR_39_NM
                                   , SUM( J.FACTOR_39_QTY )                                                  AS FACTOR_39_QTY
                                   , MAX( J.FACTOR_40_NM )                                                   AS FACTOR_40_NM
                                   , SUM( J.FACTOR_40_QTY )                                                  AS FACTOR_40_QTY
                                   , MAX( J.FACTOR_41_NM )                                                   AS FACTOR_41_NM
                                   , SUM( J.FACTOR_41_QTY )                                                  AS FACTOR_41_QTY
                                   , MAX( J.FACTOR_42_NM )                                                   AS FACTOR_42_NM
                                   , SUM( J.FACTOR_42_QTY )                                                  AS FACTOR_42_QTY
                                   , MAX( J.FACTOR_43_NM )                                                   AS FACTOR_43_NM
                                   , SUM( J.FACTOR_43_QTY )                                                  AS FACTOR_43_QTY
                                   , MAX( J.FACTOR_44_NM )                                                   AS FACTOR_44_NM
                                   , SUM( J.FACTOR_44_QTY )                                                  AS FACTOR_44_QTY
                                   , MAX( J.FACTOR_45_NM )                                                   AS FACTOR_45_NM
                                   , SUM( J.FACTOR_45_QTY )                                                  AS FACTOR_45_QTY
                                   , MAX( J.FACTOR_46_NM )                                                   AS FACTOR_46_NM
                                   , SUM( J.FACTOR_46_QTY )                                                  AS FACTOR_46_QTY
                                   , MAX( J.FACTOR_47_NM )                                                   AS FACTOR_47_NM
                                   , SUM( J.FACTOR_47_QTY )                                                  AS FACTOR_47_QTY
                                   , MAX( J.FACTOR_48_NM )                                                   AS FACTOR_48_NM
                                   , SUM( J.FACTOR_48_QTY )                                                  AS FACTOR_48_QTY
                                   , MAX( J.FACTOR_49_NM )                                                   AS FACTOR_49_NM
                                   , SUM( J.FACTOR_49_QTY )                                                  AS FACTOR_49_QTY
                                   , MAX( J.FACTOR_50_NM )                                                   AS FACTOR_50_NM
                                   , SUM( J.FACTOR_50_QTY )                                                  AS FACTOR_50_QTY
                                   , MAX( J.FACTOR_51_NM )                                                   AS FACTOR_51_NM
                                   , SUM( J.FACTOR_51_QTY )                                                  AS FACTOR_51_QTY
                                   , MAX( J.FACTOR_52_NM )                                                   AS FACTOR_52_NM
                                   , SUM( J.FACTOR_52_QTY )                                                  AS FACTOR_52_QTY
                                   , MAX( J.FACTOR_53_NM )                                                   AS FACTOR_53_NM
                                   , SUM( J.FACTOR_53_QTY )                                                  AS FACTOR_53_QTY
                                   , MAX( J.FACTOR_54_NM )                                                   AS FACTOR_54_NM
                                   , SUM( J.FACTOR_54_QTY )                                                  AS FACTOR_54_QTY
                                   , MAX( J.FACTOR_55_NM )                                                   AS FACTOR_55_NM
                                   , SUM( J.FACTOR_55_QTY )                                                  AS FACTOR_55_QTY
                                   , MAX( J.FACTOR_56_NM )                                                   AS FACTOR_56_NM
                                   , SUM( J.FACTOR_56_QTY )                                                  AS FACTOR_56_QTY
                                   , MAX( J.FACTOR_57_NM )                                                   AS FACTOR_57_NM
                                   , SUM( J.FACTOR_57_QTY )                                                  AS FACTOR_57_QTY
                                   , MAX( J.FACTOR_58_NM )                                                   AS FACTOR_58_NM
                                   , SUM( J.FACTOR_58_QTY )                                                  AS FACTOR_58_QTY
                                   , MAX( J.FACTOR_59_NM )                                                   AS FACTOR_59_NM
                                   , SUM( J.FACTOR_59_QTY )                                                  AS FACTOR_59_QTY
                                   , MAX( J.FACTOR_60_NM )                                                   AS FACTOR_60_NM
                                   , SUM( J.FACTOR_60_QTY )                                                  AS FACTOR_60_QTY
                                   , MAX( J.FACTOR_61_NM )                                                   AS FACTOR_61_NM
                                   , SUM( J.FACTOR_61_QTY )                                                  AS FACTOR_61_QTY
                                   , MAX( J.FACTOR_62_NM )                                                   AS FACTOR_62_NM
                                   , SUM( J.FACTOR_62_QTY )                                                  AS FACTOR_62_QTY
                                   , MAX( J.FACTOR_64_NM )                                                   AS FACTOR_64_NM
                                   , SUM( J.FACTOR_64_QTY )                                                  AS FACTOR_64_QTY
                                   , MAX( J.FACTOR_65_NM )                                                   AS FACTOR_65_NM
                                   , SUM( J.FACTOR_65_QTY )                                                  AS FACTOR_65_QTY
                                   , MAX( J.FACTOR_66_NM )                                                   AS FACTOR_66_NM
                                   , SUM( J.FACTOR_66_QTY )                                                  AS FACTOR_66_QTY
                                   , MAX( J.FACTOR_67_NM )                                                   AS FACTOR_67_NM
                                   , SUM( J.FACTOR_67_QTY )                                                  AS FACTOR_67_QTY
                                   , MAX( J.FACTOR_68_NM )                                                   AS FACTOR_68_NM
                                   , SUM( J.FACTOR_68_QTY )                                                  AS FACTOR_68_QTY
                                   , MAX( J.FACTOR_69_NM )                                                   AS FACTOR_69_NM
                                   , SUM( J.FACTOR_69_QTY )                                                  AS FACTOR_69_QTY
                                   , MAX( J.FACTOR_70_NM )                                                   AS FACTOR_70_NM
                                   , SUM( J.FACTOR_70_QTY )                                                  AS FACTOR_70_QTY
                                   , MAX( J.FACTOR_71_NM )                                                   AS FACTOR_71_NM
                                   , SUM( J.FACTOR_71_QTY )                                                  AS FACTOR_71_QTY
                                   , MAX( J.FACTOR_72_NM )                                                   AS FACTOR_72_NM
                                   , SUM( J.FACTOR_72_QTY )                                                  AS FACTOR_72_QTY
                                   , MAX( J.FACTOR_73_NM )                                                   AS FACTOR_73_NM
                                   , SUM( J.FACTOR_73_QTY )                                                  AS FACTOR_73_QTY
                                   , MAX( J.FACTOR_74_NM )                                                   AS FACTOR_74_NM
                                   , SUM( J.FACTOR_74_QTY )                                                  AS FACTOR_74_QTY
                                   , MAX( J.FACTOR_75_NM )                                                   AS FACTOR_75_NM
                                   , SUM( J.FACTOR_75_QTY )                                                  AS FACTOR_75_QTY
                                   , MAX( J.FACTOR_76_NM )                                                   AS FACTOR_76_NM
                                   , SUM( J.FACTOR_76_QTY )                                                  AS FACTOR_76_QTY
                                   , MAX( J.FACTOR_77_NM )                                                   AS FACTOR_77_NM
                                   , SUM( J.FACTOR_77_QTY )                                                  AS FACTOR_77_QTY
                                   , MAX( J.FACTOR_78_NM )                                                   AS FACTOR_78_NM
                                   , SUM( J.FACTOR_78_QTY )                                                  AS FACTOR_78_QTY
                                   , MAX( J.FACTOR_79_NM )                                                   AS FACTOR_79_NM
                                   , SUM( J.FACTOR_79_QTY )                                                  AS FACTOR_79_QTY
                                   , MAX( J.FACTOR_80_NM )                                                   AS FACTOR_80_NM
                                   , SUM( J.FACTOR_80_QTY )                                                  AS FACTOR_80_QTY
                                   , MAX( J.FACTOR_81_NM )                                                   AS FACTOR_81_NM
                                   , SUM( J.FACTOR_81_QTY )                                                  AS FACTOR_81_QTY
                                   , MAX( J.FACTOR_82_NM )                                                   AS FACTOR_82_NM
                                   , SUM( J.FACTOR_82_QTY )                                                  AS FACTOR_82_QTY
                                   , MAX( J.FACTOR_83_NM )                                                   AS FACTOR_83_NM
                                   , SUM( J.FACTOR_83_QTY )                                                  AS FACTOR_83_QTY
                                   , MAX( J.FACTOR_84_NM )                                                   AS FACTOR_84_NM
                                   , SUM( J.FACTOR_84_QTY )                                                  AS FACTOR_84_QTY
                                   , MAX( J.FACTOR_85_NM )                                                   AS FACTOR_85_NM
                                   , SUM( J.FACTOR_85_QTY )                                                  AS FACTOR_85_QTY
                                   , MAX( J.FACTOR_86_NM )                                                   AS FACTOR_86_NM
                                   , SUM( J.FACTOR_86_QTY )                                                  AS FACTOR_86_QTY
                                   , MAX( DECODE( K.NO, 2, J.INSERT_USER, '' ) )                             AS INSERT_USER
                                   , MAX( DECODE( K.NO, 2, J.PURCH_LOT_NO, '' ) )                            AS PURCH_LOT_NO
                                   , MAX( DECODE( K.NO, 2, J.S_WORK_GB, '' ) )                               AS S_WORK_GB
                                   , MAX( DECODE( K.NO, 2, J.I_DISP_FACTOR_NM, '' ) )                        AS I_DISP_FACTOR_NM
                                   , MAX( DECODE( K.NO, 2, J.REJECT_REMARK, '' ) )                           AS REJECT_REMARK
                                   , MAX( DECODE( K.NO, 2, J.PROD_GROUP, '' ) )                              AS PROD_GROUP
                                   , MAX( DECODE( K.NO, 2, J.PDAP, '' ) )                                    AS PDAP
                                   , MAX( DECODE( K.NO, 2, J.E_TOP_TAC, '' ) )                               AS E_TOP_TAC
                                   , MAX( DECODE( K.NO, 2, J.NORMAL_FACTOR_CD, '' ) )                               AS NORMAL_FACTOR_CD
                                   , MAX( J.FACTOR_87_NM )                                                   AS FACTOR_87_NM
                                   , SUM( J.FACTOR_87_QTY )                                                  AS FACTOR_87_QTY
                                   , MAX( J.FACTOR_88_NM )                                                   AS FACTOR_88_NM
                                   , SUM( J.FACTOR_88_QTY )                                                  AS FACTOR_88_QTY
                                   , MAX( J.FACTOR_89_NM )                                                   AS FACTOR_89_NM
                                   , SUM( J.FACTOR_89_QTY )                                                  AS FACTOR_89_QTY
                                   , MAX( J.FACTOR_90_NM )                                                   AS FACTOR_90_NM
                                   , SUM( J.FACTOR_90_QTY )                                                  AS FACTOR_90_QTY
                                   , MAX( J.FACTOR_91_NM )                                                   AS FACTOR_91_NM
                                   , SUM( J.FACTOR_91_QTY )                                                  AS FACTOR_91_QTY
                                   , MAX( J.FACTOR_92_NM )                                                   AS FACTOR_92_NM
                                   , SUM( J.FACTOR_92_QTY )                                                  AS FACTOR_92_QTY
                                   , MAX( J.FACTOR_93_NM )                                                   AS FACTOR_93_NM
                                   , SUM( J.FACTOR_93_QTY )                                                  AS FACTOR_93_QTY
                                   , MAX( J.FACTOR_94_NM )                                                   AS FACTOR_94_NM
                                   , SUM( J.FACTOR_94_QTY )                                                  AS FACTOR_94_QTY
                                   , MAX( J.FACTOR_95_NM )                                                   AS FACTOR_95_NM
                                   , SUM( J.FACTOR_95_QTY )                                                  AS FACTOR_95_QTY
                                   , MAX( J.FACTOR_96_NM )                                                   AS FACTOR_96_NM
                                   , SUM( J.FACTOR_96_QTY )                                                  AS FACTOR_96_QTY
                                   , MAX( J.FACTOR_97_NM )                                                   AS FACTOR_97_NM
                                   , SUM( J.FACTOR_97_QTY )                                                  AS FACTOR_97_QTY
                                   , MAX( J.FACTOR_98_NM )                                                   AS FACTOR_98_NM
                                   , SUM( J.FACTOR_98_QTY )                                                  AS FACTOR_98_QTY
                                   , MAX( J.FACTOR_99_NM )                                                   AS FACTOR_99_NM
                                   , SUM( J.FACTOR_99_QTY )                                                  AS FACTOR_99_QTY
                                   , MAX( J.FACTOR_100_NM )                                                   AS FACTOR_100_NM
                                   , SUM( J.FACTOR_100_QTY )                                                  AS FACTOR_100_QTY
                                   , MAX( J.FACTOR_101_NM )                                                   AS FACTOR_101_NM
                                   , SUM( J.FACTOR_101_QTY )                                                  AS FACTOR_101_QTY
                                   , MAX( J.FACTOR_102_NM )                                                   AS FACTOR_102_NM
                                   , SUM( J.FACTOR_102_QTY )                                                  AS FACTOR_102_QTY
                                   , MAX( J.FACTOR_103_NM )                                                   AS FACTOR_103_NM
                                   , SUM( J.FACTOR_103_QTY )                                                  AS FACTOR_103_QTY
                                   , MAX( J.FACTOR_104_NM )                                                   AS FACTOR_104_NM
                                   , SUM( J.FACTOR_104_QTY )                                                  AS FACTOR_104_QTY
                                   , MAX( J.FACTOR_105_NM )                                                   AS FACTOR_105_NM
                                   , SUM( J.FACTOR_105_QTY )                                                  AS FACTOR_105_QTY
                                   , MAX( J.FACTOR_106_NM )                                                   AS FACTOR_106_NM
                                   , SUM( J.FACTOR_106_QTY )                                                  AS FACTOR_106_QTY
                                   , MAX( J.FACTOR_107_NM )                                                   AS FACTOR_107_NM
                                   , SUM( J.FACTOR_107_QTY )                                                  AS FACTOR_107_QTY
                                   , MAX( J.FACTOR_108_NM )                                                   AS FACTOR_108_NM
                                   , SUM( J.FACTOR_108_QTY )                                                  AS FACTOR_108_QTY
                                   , MAX( J.FACTOR_109_NM )                                                   AS FACTOR_109_NM
                                   , SUM( J.FACTOR_109_QTY )                                                  AS FACTOR_109_QTY
                                   , MAX( J.FACTOR_110_NM )                                                   AS FACTOR_110_NM
                                   , SUM( J.FACTOR_110_QTY )                                                  AS FACTOR_110_QTY
                                   , MAX( J.FACTOR_111_NM )                                                   AS FACTOR_111_NM
                                   , SUM( J.FACTOR_111_QTY )                                                  AS FACTOR_111_QTY
                                   , MAX( DECODE( K.NO, 2, J.NORMAL_FACTOR_CD2, '' ) )                        AS NORMAL_FACTOR_CD2
                                   , MAX( DECODE( K.NO, 2, J.REWORK_INSP_DIV, '' ) )                          AS REWORK_INSP_DIV
                                FROM
                                     (
                                     SELECT MAX( X.WORK_GB ) AS WORK_GB
                                          , X.PLANT_CD       AS PLANT_CD
                                          , X.PROD_WC_CD     AS PROD_WC_CD
                                          , MAX( X.WC_NM )   AS WC_NM
                                          , X.TOP_BOTTOM     AS TOP_BOTTOM
                                          , MAX( NVL( R.INSPECT_LOT_NO, DECODE( PURCH_LOT_NO, '', F_ONE_LOT_TRACE_T( X.AR_WARHS_CREATE_NO, '%%', '1' ), PURCH_LOT_NO ) ) ) AS IN_LOT_NO
                                          , MAX( X.AR_WARHS_CREATE_NO )                                                                                                    AS AR_WARHS_CREATE_NO
                                          , MAX(DECODE( X.PURCH_LOT_NO, '', DECODE(SUBSTR(X.IN_LOT_NO,11,1),'E',F_ONE_LOT_TRACE_T( X.AR_WARHS_CREATE_NO, '_E%', '%%' ),F_ONE_LOT_TRACE_T( X.AR_WARHS_CREATE_NO, '_E%', '%%' )), DECODE(SUBSTR(X.IN_LOT_NO,11,1),'E',F_ONE_LOT_TRACE_T( F_AR_NO_RETURN_T( X.PURCH_LOT_NO ), '_E%', '%%' ),F_ONE_LOT_TRACE_T( F_AR_NO_RETURN_T( X.PURCH_LOT_NO ), '_E%', '%%' )) )) AS I_BE_LOT_NO
                                          , MAX( X.I_BE_PROD_CD )                                                                                                          AS I_BE_PROD_CD
                                          , MAX( X.LOT_NO )                                                                                                                AS LOT_NO
                                          , MAX( X.PROD_SIZE )                                                                                                             AS PROD_SIZE
                                          , MAX( X.INSP_CLASS )                                                                                                            AS INSP_CLASS
                                          , MAX( X.PROD_CD )                                                                                                               AS PROD_CD
                                          , MAX( X.LENG )                                                                                                                  AS LENG
                                          , MAX( X.LOT_END_ILSI )                                                                                                          AS LOT_END_ILSI
                                          , MAX( X.PROD_DATE )                                                                                                             AS PROD_DATE
                                          , MAX( X.PROD_NM )                                                                                                               AS PROD_NM
                                          , MAX( X.MANA_NM )                                                                                                               AS MANA_NM
                                          , MAX( X.MANA_NO )                                                                                                               AS MANA_NO
                                          , MAX( X.NORMAL_QTY )                                                                                                            AS NORMAL_QTY
                                          , SUM( X.DISPRODUCT_QTY )                                                                                                        AS DISPRODUCT_QTY
                                          , MAX( DECODE( RANKING, 1, X.DISP_FACTOR_NM ) )                                                                                  AS FACTOR_01_NM
                                          , SUM( DECODE( RANKING, 1, X.DISPRODUCT_QTY, 0 ) )                                                                               AS FACTOR_01_QTY
                                          , MAX( DECODE( RANKING, 2, X.DISP_FACTOR_NM ) )                                                                                  AS FACTOR_02_NM
                                          , SUM( DECODE( RANKING, 2, X.DISPRODUCT_QTY, 0 ) )                                                                               AS FACTOR_02_QTY
                                          , MAX( DECODE( RANKING, 3, X.DISP_FACTOR_NM ) )                                                                                  AS FACTOR_03_NM
                                          , SUM( DECODE( RANKING, 3, X.DISPRODUCT_QTY, 0 ) )                                                                               AS FACTOR_03_QTY
                                          , MAX( DECODE( RANKING, 4, X.DISP_FACTOR_NM ) )                                                                                  AS FACTOR_04_NM
                                          , SUM( DECODE( RANKING, 4, X.DISPRODUCT_QTY, 0 ) )                                                                               AS FACTOR_04_QTY
                                          , MAX( DECODE( RANKING, 5, X.DISP_FACTOR_NM ) )                                                                                  AS FACTOR_05_NM
                                          , SUM( DECODE( RANKING, 5, X.DISPRODUCT_QTY, 0 ) )                                                                               AS FACTOR_05_QTY
                                          , MAX( DECODE( RANKING, 6, X.DISP_FACTOR_NM ) )                                                                                  AS FACTOR_06_NM
                                          , SUM( DECODE( RANKING, 6, X.DISPRODUCT_QTY, 0 ) )                                                                               AS FACTOR_06_QTY
                                          , MAX( DECODE( RANKING, 7, X.DISP_FACTOR_NM ) )                                                                                  AS FACTOR_07_NM
                                          , SUM( DECODE( RANKING, 7, X.DISPRODUCT_QTY, 0 ) )                                                                               AS FACTOR_07_QTY
                                          , MAX( DECODE( RANKING, 8, X.DISP_FACTOR_NM ) )                                                                                  AS FACTOR_08_NM
                                          , SUM( DECODE( RANKING, 8, X.DISPRODUCT_QTY, 0 ) )                                                                               AS FACTOR_08_QTY
                                          , MAX( DECODE( RANKING, 9, X.DISP_FACTOR_NM ) )                                                                                  AS FACTOR_09_NM
                                          , SUM( DECODE( RANKING, 9, X.DISPRODUCT_QTY, 0 ) )                                                                               AS FACTOR_09_QTY
                                          , MAX( DECODE( RANKING, 10, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_10_NM
                                          , SUM( DECODE( RANKING, 10, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_10_QTY
                                          , MAX( DECODE( RANKING, 11, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_11_NM
                                          , SUM( DECODE( RANKING, 11, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_11_QTY
                                          , MAX( DECODE( RANKING, 12, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_12_NM
                                          , SUM( DECODE( RANKING, 12, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_12_QTY
                                          , MAX( DECODE( RANKING, 13, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_13_NM
                                          , SUM( DECODE( RANKING, 13, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_13_QTY
                                          , MAX( DECODE( RANKING, 14, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_14_NM
                                          , SUM( DECODE( RANKING, 14, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_14_QTY
                                          , MAX( DECODE( RANKING, 15, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_15_NM
                                          , SUM( DECODE( RANKING, 15, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_15_QTY
                                          , MAX( DECODE( RANKING, 16, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_16_NM
                                          , SUM( DECODE( RANKING, 16, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_16_QTY
                                          , MAX( DECODE( RANKING, 17, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_17_NM
                                          , SUM( DECODE( RANKING, 17, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_17_QTY
                                          , MAX( DECODE( RANKING, 18, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_18_NM
                                          , SUM( DECODE( RANKING, 18, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_18_QTY
                                          , MAX( DECODE( RANKING, 19, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_19_NM
                                          , SUM( DECODE( RANKING, 19, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_19_QTY
                                          , MAX( DECODE( RANKING, 20, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_20_NM
                                          , SUM( DECODE( RANKING, 20, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_20_QTY
                                          , MAX( DECODE( RANKING, 21, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_21_NM
                                          , SUM( DECODE( RANKING, 21, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_21_QTY
                                          , MAX( DECODE( RANKING, 22, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_22_NM
                                          , SUM( DECODE( RANKING, 22, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_22_QTY
                                          , MAX( DECODE( RANKING, 23, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_23_NM
                                          , SUM( DECODE( RANKING, 23, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_23_QTY
                                          , MAX( DECODE( RANKING, 24, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_24_NM
                                          , SUM( DECODE( RANKING, 24, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_24_QTY
                                          , MAX( DECODE( RANKING, 25, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_25_NM
                                          , SUM( DECODE( RANKING, 25, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_25_QTY
                                          , MAX( DECODE( RANKING, 26, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_26_NM
                                          , SUM( DECODE( RANKING, 26, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_26_QTY
                                          , MAX( DECODE( RANKING, 27, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_27_NM
                                          , SUM( DECODE( RANKING, 27, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_27_QTY
                                          , MAX( DECODE( RANKING, 28, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_28_NM
                                          , SUM( DECODE( RANKING, 28, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_28_QTY
                                          , MAX( DECODE( RANKING, 29, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_29_NM
                                          , SUM( DECODE( RANKING, 29, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_29_QTY
                                          , MAX( DECODE( RANKING, 30, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_30_NM
                                          , SUM( DECODE( RANKING, 30, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_30_QTY
                                          , MAX( DECODE( RANKING, 31, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_31_NM
                                          , SUM( DECODE( RANKING, 31, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_31_QTY
                                          , MAX( DECODE( RANKING, 32, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_32_NM
                                          , SUM( DECODE( RANKING, 32, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_32_QTY
                                          , MAX( DECODE( RANKING, 33, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_33_NM
                                          , SUM( DECODE( RANKING, 33, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_33_QTY
                                          , MAX( DECODE( RANKING, 34, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_34_NM
                                          , SUM( DECODE( RANKING, 34, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_34_QTY
                                          , MAX( DECODE( RANKING, 35, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_35_NM
                                          , SUM( DECODE( RANKING, 35, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_35_QTY
                                          , MAX( DECODE( RANKING, 36, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_36_NM
                                          , SUM( DECODE( RANKING, 36, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_36_QTY
                                          , MAX( DECODE( RANKING, 37, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_37_NM
                                          , SUM( DECODE( RANKING, 37, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_37_QTY
                                          , MAX( DECODE( RANKING, 38, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_38_NM
                                          , SUM( DECODE( RANKING, 38, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_38_QTY
                                          , MAX( DECODE( RANKING, 39, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_39_NM
                                          , SUM( DECODE( RANKING, 39, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_39_QTY
                                          , MAX( DECODE( RANKING, 40, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_40_NM
                                          , SUM( DECODE( RANKING, 40, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_40_QTY
                                          , MAX( DECODE( RANKING, 41, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_41_NM
                                          , SUM( DECODE( RANKING, 41, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_41_QTY
                                          , MAX( DECODE( RANKING, 42, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_42_NM
                                          , SUM( DECODE( RANKING, 42, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_42_QTY
                                          , MAX( DECODE( RANKING, 43, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_43_NM
                                          , SUM( DECODE( RANKING, 43, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_43_QTY
                                          , MAX( DECODE( RANKING, 44, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_44_NM
                                          , SUM( DECODE( RANKING, 44, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_44_QTY
                                          , MAX( DECODE( RANKING, 45, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_45_NM
                                          , SUM( DECODE( RANKING, 45, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_45_QTY
                                          , MAX( DECODE( RANKING, 46, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_46_NM
                                          , SUM( DECODE( RANKING, 46, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_46_QTY
                                          , MAX( DECODE( RANKING, 47, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_47_NM
                                          , SUM( DECODE( RANKING, 47, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_47_QTY
                                          , MAX( DECODE( RANKING, 48, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_48_NM
                                          , SUM( DECODE( RANKING, 48, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_48_QTY
                                          , MAX( DECODE( RANKING, 49, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_49_NM
                                          , SUM( DECODE( RANKING, 49, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_49_QTY
                                          , MAX( DECODE( RANKING, 50, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_50_NM
                                          , SUM( DECODE( RANKING, 50, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_50_QTY
                                          , MAX( DECODE( RANKING, 51, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_51_NM
                                          , SUM( DECODE( RANKING, 51, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_51_QTY
                                          , MAX( DECODE( RANKING, 52, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_52_NM
                                          , SUM( DECODE( RANKING, 52, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_52_QTY
                                          , MAX( DECODE( RANKING, 53, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_53_NM
                                          , SUM( DECODE( RANKING, 53, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_53_QTY
                                          , MAX( DECODE( RANKING, 54, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_54_NM
                                          , SUM( DECODE( RANKING, 54, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_54_QTY
                                          , MAX( DECODE( RANKING, 55, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_55_NM
                                          , SUM( DECODE( RANKING, 55, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_55_QTY
                                          , MAX( DECODE( RANKING, 56, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_56_NM
                                          , SUM( DECODE( RANKING, 56, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_56_QTY
                                          , MAX( DECODE( RANKING, 57, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_57_NM
                                          , SUM( DECODE( RANKING, 57, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_57_QTY
                                          , MAX( DECODE( RANKING, 58, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_58_NM
                                          , SUM( DECODE( RANKING, 58, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_58_QTY
                                          , MAX( DECODE( RANKING, 59, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_59_NM
                                          , SUM( DECODE( RANKING, 59, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_59_QTY
                                          , MAX( DECODE( RANKING, 60, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_60_NM
                                          , SUM( DECODE( RANKING, 60, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_60_QTY
                                          , MAX( DECODE( RANKING, 61, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_61_NM
                                          , SUM( DECODE( RANKING, 61, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_61_QTY
                                          , MAX( DECODE( RANKING, 62, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_62_NM
                                          , SUM( DECODE( RANKING, 62, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_62_QTY
                                          , MAX( DECODE( RANKING, 64, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_64_NM
                                          , SUM( DECODE( RANKING, 64, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_64_QTY
                                          , MAX( DECODE( RANKING, 65, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_65_NM
                                          , SUM( DECODE( RANKING, 65, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_65_QTY
                                          , MAX( DECODE( RANKING, 66, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_66_NM
                                          , SUM( DECODE( RANKING, 66, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_66_QTY
                                          , MAX( DECODE( RANKING, 67, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_67_NM
                                          , SUM( DECODE( RANKING, 67, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_67_QTY
                                          , MAX( DECODE( RANKING, 68, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_68_NM
                                          , SUM( DECODE( RANKING, 68, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_68_QTY
                                          , MAX( DECODE( RANKING, 69, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_69_NM
                                          , SUM( DECODE( RANKING, 69, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_69_QTY
                                          , MAX( DECODE( RANKING, 70, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_70_NM
                                          , SUM( DECODE( RANKING, 70, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_70_QTY
                                          , MAX( DECODE( RANKING, 71, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_71_NM
                                          , SUM( DECODE( RANKING, 71, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_71_QTY
                                          , MAX( DECODE( RANKING, 72, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_72_NM
                                          , SUM( DECODE( RANKING, 72, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_72_QTY
                                          , MAX( DECODE( RANKING, 73, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_73_NM
                                          , SUM( DECODE( RANKING, 73, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_73_QTY
                                          , MAX( DECODE( RANKING, 74, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_74_NM
                                          , SUM( DECODE( RANKING, 74, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_74_QTY
                                          , MAX( DECODE( RANKING, 75, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_75_NM
                                          , SUM( DECODE( RANKING, 75, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_75_QTY
                                          , MAX( DECODE( RANKING, 76, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_76_NM
                                          , SUM( DECODE( RANKING, 76, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_76_QTY
                                          , MAX( DECODE( RANKING, 77, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_77_NM
                                          , SUM( DECODE( RANKING, 77, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_77_QTY
                                          , MAX( DECODE( RANKING, 78, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_78_NM
                                          , SUM( DECODE( RANKING, 78, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_78_QTY
                                          , MAX( DECODE( RANKING, 79, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_79_NM
                                          , SUM( DECODE( RANKING, 79, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_79_QTY
                                          , MAX( DECODE( RANKING, 80, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_80_NM
                                          , SUM( DECODE( RANKING, 80, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_80_QTY
                                          , MAX( DECODE( RANKING, 81, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_81_NM
                                          , SUM( DECODE( RANKING, 81, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_81_QTY
                                          , MAX( DECODE( RANKING, 82, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_82_NM
                                          , SUM( DECODE( RANKING, 82, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_82_QTY
                                          , MAX( DECODE( RANKING, 83, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_83_NM
                                          , SUM( DECODE( RANKING, 83, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_83_QTY
                                          , MAX( DECODE( RANKING, 84, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_84_NM
                                          , SUM( DECODE( RANKING, 84, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_84_QTY
                                          , MAX( DECODE( RANKING, 85, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_85_NM
                                          , SUM( DECODE( RANKING, 85, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_85_QTY
                                          , MAX( DECODE( RANKING, 86, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_86_NM
                                          , SUM( DECODE( RANKING, 86, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_86_QTY
                                          , MAX( X.INSERT_USER )                                                                                                           AS INSERT_USER
                                          , MAX( X.PURCH_LOT_NO )                                                                                                          AS PURCH_LOT_NO
                                          , MAX( X.S_WORK_GB )                                                                                                             AS S_WORK_GB
                                          , MAX( X.I_DISP_FACTOR_NM )                                                                                                      AS I_DISP_FACTOR_NM
                                          , MAX( X.REJECT_REMARK )                                                                                                         AS REJECT_REMARK
                                          , MAX (X.PROD_GROUP)                        AS PROD_GROUP
                                          , MAX (X.PDAP)                              AS PDAP
                                          , MAX( SUBSTR(X.PROD_CD,7,4) )              AS E_TOP_TAC
                                          , MAX(X.NORMAL_FACTOR_CD)              AS NORMAL_FACTOR_CD
                                          , MAX( DECODE( RANKING, 87, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_87_NM
                                          , SUM( DECODE( RANKING, 87, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_87_QTY
                                          , MAX( DECODE( RANKING, 88, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_88_NM
                                          , SUM( DECODE( RANKING, 88, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_88_QTY
                                          , MAX( DECODE( RANKING, 89, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_89_NM
                                          , SUM( DECODE( RANKING, 89, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_89_QTY
                                          , MAX( DECODE( RANKING, 90, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_90_NM
                                          , SUM( DECODE( RANKING, 90, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_90_QTY
                                          , MAX( DECODE( RANKING, 91, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_91_NM
                                          , SUM( DECODE( RANKING, 91, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_91_QTY
                                          , MAX( DECODE( RANKING, 92, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_92_NM
                                          , SUM( DECODE( RANKING, 92, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_92_QTY
                                          , MAX( DECODE( RANKING, 93, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_93_NM
                                          , SUM( DECODE( RANKING, 93, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_93_QTY
                                          , MAX( DECODE( RANKING, 94, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_94_NM
                                          , SUM( DECODE( RANKING, 94, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_94_QTY
                                          , MAX( DECODE( RANKING, 95, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_95_NM
                                          , SUM( DECODE( RANKING, 95, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_95_QTY
                                          , MAX( DECODE( RANKING, 96, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_96_NM
                                          , SUM( DECODE( RANKING, 96, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_96_QTY
                                          , MAX( DECODE( RANKING, 97, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_97_NM
                                          , SUM( DECODE( RANKING, 97, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_97_QTY
                                          , MAX( DECODE( RANKING, 98, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_98_NM
                                          , SUM( DECODE( RANKING, 98, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_98_QTY
                                          , MAX( DECODE( RANKING, 99, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_99_NM
                                          , SUM( DECODE( RANKING, 99, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_99_QTY
                                          , MAX( DECODE( RANKING, 100, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_100_NM
                                          , SUM( DECODE( RANKING, 100, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_100_QTY
                                          , MAX( DECODE( RANKING, 101, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_101_NM
                                          , SUM( DECODE( RANKING, 101, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_101_QTY
                                          , MAX( DECODE( RANKING, 102, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_102_NM
                                          , SUM( DECODE( RANKING, 102, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_102_QTY
                                          , MAX( DECODE( RANKING, 103, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_103_NM
                                          , SUM( DECODE( RANKING, 103, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_103_QTY
                                          , MAX( DECODE( RANKING, 104, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_104_NM
                                          , SUM( DECODE( RANKING, 104, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_104_QTY
                                          , MAX( DECODE( RANKING, 105, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_105_NM
                                          , SUM( DECODE( RANKING, 105, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_105_QTY
                                          , MAX( DECODE( RANKING, 106, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_106_NM
                                          , SUM( DECODE( RANKING, 106, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_106_QTY
                                          , MAX( DECODE( RANKING, 107, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_107_NM
                                          , SUM( DECODE( RANKING, 107, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_107_QTY
                                          , MAX( DECODE( RANKING, 108, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_108_NM
                                          , SUM( DECODE( RANKING, 108, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_108_QTY
                                          , MAX( DECODE( RANKING, 109, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_109_NM
                                          , SUM( DECODE( RANKING, 109, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_109_QTY
                                          , MAX( DECODE( RANKING, 110, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_110_NM
                                          , SUM( DECODE( RANKING, 110, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_110_QTY
                                          , MAX( DECODE( RANKING, 111, X.DISP_FACTOR_NM ) )                                                                                 AS FACTOR_111_NM
                                          , SUM( DECODE( RANKING, 111, X.DISPRODUCT_QTY, 0 ) )                                                                              AS FACTOR_111_QTY
                                          , MAX(X.NORMAL_FACTOR_CD2)            AS NORMAL_FACTOR_CD2
                                          , MAX(X.REWORK_INSP_DIV)              AS REWORK_INSP_DIV
                                       FROM
                                            (
                                            SELECT N.WORK_GB            AS WORK_GB
                                                 , ''                   AS IN_LOT_NO
                                                 , ''                   AS I_BE_LOT_NO
                                                 , ''                   AS I_BE_PROD_CD
                                                 , N.PLANT_CD           AS PLANT_CD
                                                 , N.PROD_WC_CD         AS PROD_WC_CD
                                                 , N.PURCH_LOT_NO       AS PURCH_LOT_NO
                                                 , N.WC_NM              AS WC_NM
                                                 , N.TOP_BOTTOM         AS TOP_BOTTOM
                                                 , N.INSP_CLASS         AS INSP_CLASS
                                                 , N.AR_WARHS_CREATE_NO AS AR_WARHS_CREATE_NO
                                                 , N.LOT_NO             AS LOT_NO
                                                 , N.PROD_SIZE          AS PROD_SIZE
                                                 , N.PROD_CD            AS PROD_CD
                                                 , N.LENG               AS LENG
                                                 , N.LOT_END_ILSI       AS LOT_END_ILSI
                                                 , N.PROD_DATE          AS PROD_DATE
                                                 , N.PROD_NM            AS PROD_NM
                                                 , N.MANA_NM            AS MANA_NM
                                                 , N.MANA_NO            AS MANA_NO
                                                 , N.NORMAL_QTY         AS NORMAL_QTY
                                                 , M.DISP_FACTOR_CD     AS DISP_FACTOR_CD
                                                 , M.RANKING            AS RANKING
                                                 , M.DISP_FACTOR_NM     AS DISP_FACTOR_NM
                                                 , N.INSERT_USER        AS INSERT_USER
                                                 , N.S_WORK_GB          AS S_WORK_GB
                                                 , N.DISPRODUCT_QTY     AS DISPRODUCT_QTY
                                                 , N.I_DISP_FACTOR_NM   AS I_DISP_FACTOR_NM
                                                 , N.REJECT_REMARK      AS REJECT_REMARK
                                                 , N.PROD_GROUP AS PROD_GROUP
                                                 , (SELECT ETC_NM FROM TB_IEM916 WHERE PLANT_CD='A020' AND GUBN_CD='PDAP'AND DEL_FLAG = 'A' AND ETC_CD = N.PDAP) AS PDAP
                                                 , O.ETC_NM AS NORMAL_FACTOR_CD
                                                 , P.ETC_NM    AS NORMAL_FACTOR_CD2
                                                 , Q.ETC_NM    AS REWORK_INSP_DIV
                                              FROM
                                                   (
                                                   SELECT MAX( DECODE( A.G_WORK_GB, 'E', 'Y', 'N' ) )             AS WORK_GB
                                                        , A.PLANT_CD                                              AS PLANT_CD
                                                        , A.PROD_WC_CD                                            AS PROD_WC_CD
                                                        , CASE WHEN MAX(SUBSTR(A.LOT_NO,13,3)) BETWEEN '400' AND '699' AND MAX(INSTR(E.WC_NM,'AIP')) > 0
                                                               THEN REPLACE(MAX(E.WC_NM ),'AIP','SI')
                                                               WHEN MAX(SUBSTR(A.LOT_NO,13,3)) BETWEEN '700' AND '999' AND MAX(INSTR(E.WC_NM,'AIP')) > 0
                                                               THEN REPLACE(MAX(E.WC_NM ),'AIP','CI')
                                                          ELSE MAX( E.WC_NM ) END AS WC_NM
                                                        , MAX( A.AR_WARHS_CREATE_NO )                             AS AR_WARHS_CREATE_NO
                                                        , ''  AS TOP_AR_WARHS_CREATE_NO
                                                        , MAX( A.G_PURCH_LOT_NO )                                 AS PURCH_LOT_NO
                                                        , MAX( A.INSP_CLASS )                                     AS INSP_CLASS
                                                        , DECODE( B.DISP_FACTOR_CD, '', 'S40', B.DISP_FACTOR_CD ) AS DISP_FACTOR_CD
                                                        , MAX( A.LOT_NO )                                         AS LOT_NO
                                                        , MAX( C.PROD_SIZE )                                      AS PROD_SIZE
                                                        , MAX( A.PROD_CD )                                        AS PROD_CD
                                                        , MAX( C.LENG )                                           AS LENG
                                                        , MAX( C.TOP_BOTTOM )                                     AS TOP_BOTTOM
                                                        , MAX( A.LOT_END_ILSI )                                   AS LOT_END_ILSI
                                                        , MAX( A.PROD_DATE )                                      AS PROD_DATE
                                                        , MAX( C.PROD_NM )                                        AS PROD_NM
                                                        , MAX( D.MANA_NM )                                        AS MANA_NO
                                                        , MAX( F_MANA_NM( A.PLANT_CD, D.MANA_NO ) )               AS MANA_NM
                                                        , MAX( A.NORMAL_QTY )                                     AS NORMAL_QTY
                                                        , MAX( A.INSERT_USER )                                    AS INSERT_USER
                                                        , MAX( H.ETC_NM )                                         AS S_WORK_GB
                                                        , SUM( NVL( B.DISPRODUCT_QTY, 0 ) + NVL( B.DISPRODUCT_CORR_QTY, 0 ) ) AS DISPRODUCT_QTY
                                                        , MAX( A.REJECT_REMARK )                                              AS REJECT_REMARK
                                                        , MAX(J.DISP_FACTOR_NM) AS I_DISP_FACTOR_NM
                                                         , MAX(C.PROD_GROUP) AS PROD_GROUP
                                                        , MAX(C.PDAP) AS PDAP
                                                        , MAX(K.NORMAL_FACTOR_CD)  AS NORMAL_FACTOR_CD
                                                        , MAX(K.NORMAL_FACTOR_CD2)   AS NORMAL_FACTOR_CD2
                                                        , MAX(K.REWORK_INSP_DIV)   AS REWORK_INSP_DIV
                                                     FROM
                                                          (
                                                          SELECT /*+ INDEX(G0 TB_IEM120_X22) */
                                                                 A0.PLANT_CD
                                                               , A0.AR_WARHS_CREATE_NO
                                                               , DECODE( MAX(A0.PROD_WC_CD), 'CS00', MAX(SUBSTR(A0.PROD_WC_CD,1,3))||MAX(SUBSTR(A0.PROD_SEQ_NO,1,1)), MAX(A0.PROD_WC_CD)) AS PROD_WC_CD
                                                               , MAX( A0.INSP_CLASS )                                          AS INSP_CLASS
                                                               , MAX( A0.PROD_DATE||A0.PROD_WC_CD||A0.PROD_SEQ_NO )            AS LOT_NO
                                                               , MAX( A0.PROD_CD )                                             AS PROD_CD
                                                               , MAX( A0.LOT_END_ILSI )                                        AS LOT_END_ILSI
                                                               , MAX( A0.PROD_DATE )                                           AS PROD_DATE
                                                               , MAX( NVL( A0.NORMAL_QTY, 0 ) + NVL( A0.NORMAL_CORR_QTY, 0 ) ) AS NORMAL_QTY
                                                               , MAX( A0.INSERT_USER )                                         AS INSERT_USER
                                                               , MAX( A0.REJECT_REMARK )                                       AS REJECT_REMARK
                                                               , MAX( A0.WORK_GB )                                             AS WORK_GB
                                                               , MAX( G0.AR_WARHS_CREATE_NO )                                  AS G_AR_WARHS_CREATE_NO
                                                               , MAX( G0.WORK_GB )                                             AS G_WORK_GB
                                                               , MAX( G0.PURCH_LOT_NO )                                        AS G_PURCH_LOT_NO
                                                               , SUM( F0.WC_INPUT_QTY )                                        AS F_WC_INPUT_QTY
                                                            FROM TB_IEM120 A0
                                                               , TB_IEM124 F0
                                                               , TB_IEM120 G0
                                                           WHERE A0.PLANT_CD = 'A020'
                                                             AND A0.PROD_DATE BETWEEN '{}' AND '{}'
                                                             AND (A0.PROD_WC_CD IN (SELECT WC_CD FROM TB_IEM908 WHERE PLANT_CD = 'A020' AND WC_CD LIKE '%S%' AND USE_YN = 'Y' AND DEL_FLAG = 'A') OR (A0.PROD_WC_CD = 'CS00' AND SUBSTR(A0.PROD_WC_CD,1,3)||SUBSTR(A0.PROD_SEQ_NO,1,1) IN (SELECT WC_CD FROM TB_IEM908 WHERE PLANT_CD = 'A020' AND WC_CD LIKE '%S%' AND USE_YN = 'Y' AND DEL_FLAG = 'A')))
                                                             AND A0.WORK_GB LIKE '%%'
                                                             AND A0.DEL_FLAG = 'A'
                                                             AND A0.PLANT_CD = F0.PLANT_CD(+)
                                                             AND A0.AR_WARHS_CREATE_NO = F0.O_AR_WARHS_CREATE_NO(+)
                                                             AND F0.DEL_FLAG(+) = A0.DEL_FLAG
                                                             AND F0.PLANT_CD = G0.PLANT_CD(+)
                                                             AND F0.I_AR_WARHS_CREATE_NO = G0.AR_WARHS_CREATE_NO(+)
                                                             AND G0.DEL_FLAG(+) = F0.DEL_FLAG
                                                             AND DECODE( DECODE( A0.OUT_WC_CD,'RTSX','C',A0.WORK_GB), 'C', 1, 'D',1, DECODE( SUBSTR( G0.PROD_WC_CD, 2, 1 ), 'X', 1, F0.WC_INPUT_QTY ) ) <> 0
                                                           GROUP BY A0.PLANT_CD
                                                               , A0.AR_WARHS_CREATE_NO
                                                          ) A
                                                        , TB_IEM401 B
                                                        , TB_IEM903 C
                                                        , TB_IEM902 D
                                                        , TB_IEM908 E
                                                        , TB_IEM916 H
                                                        , TB_IEM127 I
                                                        , TB_IEM930 J
                                                        , TB_IEM12M K
                                                    WHERE B.PLANT_CD(+) = A.PLANT_CD
                                                      AND B.AR_WARHS_CREATE_NO(+) = A.AR_WARHS_CREATE_NO
                                                      AND B.DEL_FLAG(+) = 'A'
                                                      AND B.DISP_GUBN(+) = 'A'
                                                      AND C.PLANT_CD = A.PLANT_CD
                                                      AND C.PROD_CD = A.PROD_CD
                                                      AND C.PROD_CD LIKE '%'
                                                       AND C.PDAP LIKE '%'
                                                       AND D.PLANT_CD(+) = C.PLANT_CD
                                                      AND D.MANA_NO (+) = C.MANA_NO
                                                      AND A.PLANT_CD = E.PLANT_CD
                                                      AND A.PROD_WC_CD = E.WC_CD
                                                      AND E.DEL_FLAG = 'A'
                                                      AND E.USE_YN = 'Y'
                                                      AND A.PLANT_CD = H.PLANT_CD(+)
                                                      AND A.WORK_GB = H.ETC_CD(+)
                                                      AND H.DEL_FLAG(+) = 'A'
                                                      AND H.GUBN_CD(+) = '06'
                                                      AND I.PLANT_CD(+) = A.PLANT_CD
                                                      AND I.AR_WARHS_CREATE_NO(+) = A.AR_WARHS_CREATE_NO
                                                      AND I.DEL_FLAG(+) = 'A'
                                                      AND J.DISP_FACTOR_CD(+) = I.DISP_FACTOR_CD
                                                      AND J.DEL_FLAG(+) = 'A'
                                                      AND K.DEL_FLAG(+) = 'A'
                                                      AND K.AR_WARHS_CREATE_NO(+) = A.AR_WARHS_CREATE_NO
                                                      AND K.PLANT_CD(+) = A.PLANT_CD
                                                      AND K.INSPECTION_SEQ(+) = '1'
                                                      AND DECODE( A.WORK_GB, 'D', DECODE(I.DISP_FACTOR_CD, 'R12', 1, F_WC_INPUT_QTY), 1) <> 0
                                                    GROUP BY A.PLANT_CD
                                                        , A.G_AR_WARHS_CREATE_NO
                                                        , A.PROD_WC_CD
                                                        , A.AR_WARHS_CREATE_NO
                                                        , DECODE( B.DISP_FACTOR_CD, '', 'S40', B.DISP_FACTOR_CD )
                                                 UNION ALL
                                                   SELECT MAX( DECODE( A.G_WORK_GB, 'E', 'Y', 'N' ) )             AS WORK_GB
                                                        , A.PLANT_CD                                              AS PLANT_CD
                                                        , A.PROD_WC_CD                                            AS PROD_WC_CD
                                                        , CASE WHEN MAX(SUBSTR(A.LOT_NO,13,3)) BETWEEN '400' AND '699' AND MAX(INSTR(E.WC_NM,'AIP')) > 0
                                                               THEN REPLACE(MAX(E.WC_NM ),'AIP','SI')
                                                               WHEN MAX(SUBSTR(A.LOT_NO,13,3)) BETWEEN '700' AND '999' AND MAX(INSTR(E.WC_NM,'AIP')) > 0
                                                               THEN REPLACE(MAX(E.WC_NM ),'AIP','CI')
                                                          ELSE MAX( E.WC_NM ) END AS WC_NM
                                                        , MAX( A.AR_WARHS_CREATE_NO )                             AS AR_WARHS_CREATE_NO
                                                        , MAX( A.TOP_AR_WARHS_CREATE_NO )                         AS TOP_AR_WARHS_CREATE_NO
                                                        , MAX( A.G_PURCH_LOT_NO )                                 AS PURCH_LOT_NO
                                                        , MAX( A.INSP_CLASS )                                     AS INSP_CLASS
                                                        , 'S40'                                                   AS DISP_FACTOR_CD
                                                        , MAX( A.LOT_NO )                                         AS LOT_NO
                                                        , MAX( C.PROD_SIZE )                                      AS PROD_SIZE
                                                        , MAX( A.PROD_CD )                                        AS PROD_CD
                                                        , MAX( C.LENG )                                           AS LENG
                                                        , MAX( C.TOP_BOTTOM )                                     AS TOP_BOTTOM
                                                        , MAX( A.LOT_END_ILSI )                                   AS LOT_END_ILSI
                                                        , MAX( A.PROD_DATE )                                      AS PROD_DATE
                                                        , MAX( C.PROD_NM )                                        AS PROD_NM
                                                        , MAX( D.MANA_NM )                                        AS MANA_NO
                                                        , MAX( F_MANA_NM( A.PLANT_CD, D.MANA_NO ) )               AS MANA_NM
                                                        , MAX( A.NORMAL_QTY )                                     AS NORMAL_QTY
                                                        , MAX( A.INSERT_USER )                                    AS INSERT_USER
                                                        , MAX( H.ETC_NM )                                         AS S_WORK_GB
                                                        , SUM( NVL( B.DISPRODUCT_QTY, 0 ) + NVL( B.DISPRODUCT_CORR_QTY, 0 ) ) AS DISPRODUCT_QTY
                                                        , MAX( A.REJECT_REMARK )                                              AS REJECT_REMARK
                                                        , MAX(C.PROD_GROUP) AS PROD_GROUP
                                                        , MAX(C.PDAP) AS PDAP
                                                        , MAX(J.DISP_FACTOR_NM) AS I_DISP_FACTOR_NM
                                                         , MAX(K.NORMAL_FACTOR_CD)  AS NORMAL_FACTOR_CD
                                                         , MAX(K.NORMAL_FACTOR_CD2)   AS NORMAL_FACTOR_CD2
                                                         , MAX(K.REWORK_INSP_DIV)   AS REWORK_INSP_DIV
                                                      FROM
                                                          (
                                                          SELECT /*+ ORDERED */
                                                                    ZZ.PLANT_CD       AS PLANT_CD
                                                                    ,ZZ.AR_WARHS_CREATE_NO     AS AR_WARHS_CREATE_NO
                                                                    ,K0.AR_WARHS_CREATE_NO    AS TOP_AR_WARHS_CREATE_NO
                                                                    ,ZZ.PROD_WC_CD         AS PROD_WC_CD
                                                                    ,ZZ.INSP_CLASS        AS INSP_CLASS
                                                                    ,ZZ.LOT_NO            AS LOT_NO
                                                                    ,ZZ.PROD_CD           AS PROD_CD
                                                                    ,ZZ.LOT_END_ILSI      AS LOT_END_ILSI
                                                                    ,ZZ.PROD_DATE         AS PROD_DATE
                                                                    ,NVL( K0.NORMAL_QTY, 0 ) + NVL( K0.NORMAL_CORR_QTY, 0 ) AS NORMAL_QTY
                                                                    ,ZZ.INSERT_USER            AS INSERT_USER
                                                                    ,ZZ.REJECT_REMARK          AS REJECT_REMARK
                                                                    ,ZZ.WORK_GB                AS WORK_GB
                                                                    ,ZZ.G_AR_WARHS_CREATE_NO    AS G_AR_WARHS_CREATE_NO
                                                                    ,ZZ.G_WORK_GB        AS G_WORK_GB
                                                                    ,ZZ.G_PURCH_LOT_NO   AS G_PURCH_LOT_NO
                                                                    ,ZZ.F_WC_INPUT_QTY   AS F_WC_INPUT_QTY
                                                           from (
                                                          SELECT /*+ INDEX(G0 TB_IEM120_X22) */
                                                                 A0.PLANT_CD
                                                               , A0.AR_WARHS_CREATE_NO
                                                               , DECODE( MAX(A0.PROD_WC_CD), 'CS00', MAX(SUBSTR(A0.PROD_WC_CD,1,3))||MAX(SUBSTR(A0.PROD_SEQ_NO,1,1)), MAX(A0.PROD_WC_CD)) AS PROD_WC_CD
                                                               , MAX( A0.INSP_CLASS )                                          AS INSP_CLASS
                                                               , MAX( A0.PROD_DATE||A0.PROD_WC_CD||A0.PROD_SEQ_NO )            AS LOT_NO
                                                               , MAX( A0.PROD_CD )                                             AS PROD_CD
                                                               , MAX( A0.LOT_END_ILSI )                                        AS LOT_END_ILSI
                                                               , MAX( A0.PROD_DATE )                                           AS PROD_DATE
                                                               , MAX( NVL( A0.NORMAL_QTY, 0 ) + NVL( A0.NORMAL_CORR_QTY, 0 ) ) AS NORMAL_QTY
                                                               , MAX( A0.INSERT_USER )                                         AS INSERT_USER
                                                               , MAX( A0.REJECT_REMARK )                                       AS REJECT_REMARK
                                                               , MAX( A0.WORK_GB )                                             AS WORK_GB
                                                               , MAX( G0.AR_WARHS_CREATE_NO )                                  AS G_AR_WARHS_CREATE_NO
                                                               , MAX( G0.WORK_GB )                                             AS G_WORK_GB
                                                               , MAX( G0.PURCH_LOT_NO )                                        AS G_PURCH_LOT_NO
                                                               , SUM( F0.WC_INPUT_QTY )                                        AS F_WC_INPUT_QTY
                                                            FROM TB_IEM120 A0
                                                               , TB_IEM124 F0
                                                               , TB_IEM120 G0
                                                           WHERE A0.PLANT_CD = 'A020'
                                                             AND A0.PROD_DATE BETWEEN '{}' AND '{}'
                                                             AND (A0.PROD_WC_CD IN (SELECT WC_CD FROM TB_IEM908 WHERE PLANT_CD = 'A020' AND WC_CD LIKE '%S%' AND USE_YN = 'Y' AND DEL_FLAG = 'A') OR (A0.PROD_WC_CD = 'CS00' AND SUBSTR(A0.PROD_WC_CD,1,3)||SUBSTR(A0.PROD_SEQ_NO,1,1) IN (SELECT WC_CD FROM TB_IEM908 WHERE PLANT_CD = 'A020' AND WC_CD LIKE '%S%' AND USE_YN = 'Y' AND DEL_FLAG = 'A')))
                                                             AND A0.WORK_GB LIKE '%%'
                                                             AND A0.DEL_FLAG = 'A'
                                                             AND A0.PLANT_CD = F0.PLANT_CD(+)
                                                             AND A0.AR_WARHS_CREATE_NO = F0.O_AR_WARHS_CREATE_NO(+)
                                                             AND F0.DEL_FLAG(+) = A0.DEL_FLAG
                                                             AND F0.PLANT_CD = G0.PLANT_CD(+)
                                                             AND F0.I_AR_WARHS_CREATE_NO = G0.AR_WARHS_CREATE_NO(+)
                                                             AND G0.DEL_FLAG(+) = F0.DEL_FLAG
                                                             AND DECODE( DECODE( A0.OUT_WC_CD,'RTSX','C',A0.WORK_GB), 'C', 1, 'D',1, DECODE( SUBSTR( G0.PROD_WC_CD, 2, 1 ), 'X', 1, F0.WC_INPUT_QTY ) ) <> 0
                                                           GROUP BY A0.PLANT_CD
                                                               , A0.AR_WARHS_CREATE_NO
                                                          ) ZZ
                                                          ,TB_IEM120 K0
                                                          WHERE K0.PLANT_CD = ZZ.PLANT_CD
                                                          AND K0.TOP_AR_WARHS_CREATE_NO = ZZ.AR_WARHS_CREATE_NO
                                                          AND K0.DEL_FLAG = 'A'
                                                          ) A
                                                        , TB_IEM401 B
                                                        , TB_IEM903 C
                                                        , TB_IEM902 D
                                                        , TB_IEM908 E
                                                        , TB_IEM916 H
                                                        , TB_IEM127 I
                                                        , TB_IEM930 J
                                                        , TB_IEM12M K
                                                    WHERE B.PLANT_CD(+) = A.PLANT_CD
                                                      AND B.AR_WARHS_CREATE_NO(+) = A.TOP_AR_WARHS_CREATE_NO
                                                      AND B.DEL_FLAG(+) = 'A'
                                                      AND B.DISP_GUBN(+) = 'A'
                                                      AND C.PLANT_CD = A.PLANT_CD
                                                      AND C.PROD_CD = A.PROD_CD
                                                      AND C.PROD_CD LIKE '%'
                                                       AND C.PDAP LIKE '%'
                                                       AND D.PLANT_CD(+) = C.PLANT_CD
                                                      AND D.MANA_NO (+) = C.MANA_NO
                                                      AND A.PLANT_CD = E.PLANT_CD
                                                      AND A.PROD_WC_CD = E.WC_CD
                                                      AND E.DEL_FLAG = 'A'
                                                      AND E.USE_YN = 'Y'
                                                      AND A.PLANT_CD = H.PLANT_CD(+)
                                                      AND A.WORK_GB = H.ETC_CD(+)
                                                      AND H.DEL_FLAG(+) = 'A'
                                                      AND H.GUBN_CD(+) = '06'
                                                      AND I.PLANT_CD(+) = A.PLANT_CD
                                                      AND I.AR_WARHS_CREATE_NO(+) = A.AR_WARHS_CREATE_NO
                                                      AND I.DEL_FLAG(+) = 'A'
                                                      AND J.DISP_FACTOR_CD(+) = I.DISP_FACTOR_CD
                                                      AND J.DEL_FLAG(+) = 'A'
                                                      AND K.DEL_FLAG(+) = 'A'
                                                      AND K.AR_WARHS_CREATE_NO(+) = A.AR_WARHS_CREATE_NO
                                                      AND K.PLANT_CD(+) = A.PLANT_CD
                                                      AND K.INSPECTION_SEQ(+) = '1'
                                                      AND DECODE( A.WORK_GB, 'D', DECODE(I.DISP_FACTOR_CD, 'R12', 1, F_WC_INPUT_QTY), 1) <> 0
                                                      AND MANA_NM LIKE '3D%'
                                                    GROUP BY A.PLANT_CD
                                                        , A.TOP_AR_WARHS_CREATE_NO
                                                        , A.PROD_WC_CD
                                                        , A.AR_WARHS_CREATE_NO
                                                   ) N
                                                 ,
                                                   (
                                                   SELECT ROWNUM AS RANKING
                                                        , DISP_FACTOR_CD AS DISP_FACTOR_CD
                                                        , DISP_FACTOR_NM AS DISP_FACTOR_NM
                                                     FROM
                                                          (
                                                          SELECT DISTINCT DISP_FACTOR_CD AS DISP_FACTOR_CD
                                                               , LEVEL_CD                AS LEVEL_CD
                                                               , DISP_FACTOR_NM          AS DISP_FACTOR_NM
                                                            FROM
                                                                 (
                                                                 SELECT D.LEVEL_CD AS LEVEL_CD
                                                                      , D.DISP_FACTOR_CD AS DISP_FACTOR_CD
                                                                      , 0                AS DISPRODUCT_QTY
                                                                      , C.DISP_FACTOR_NM AS DISP_FACTOR_NM
                                                                   FROM TB_IEM930 C
                                                                      , TB_IEM914 D
                                                                  WHERE D.PLANT_CD = 'A020'
                                                                    AND D.WC_CD IN
                                                                        (
                                                                        SELECT WC_CD
                                                                          FROM TB_IEM908
                                                                         WHERE PLANT_CD = 'A020'
                                                                           AND LEVEL_CD =
                                                                               (
                                                                               SELECT SUBSTR( LEVEL_CD, 1, 4 ) AS LEVEL_CD
                                                                                 FROM TB_IEM908
                                                                                WHERE PLANT_CD = 'A020'
                                                                                  AND WC_CD = 'YY09'
                                                                                  AND DEL_FLAG = 'A'
                                                                               )
                                                                           AND DEL_FLAG = 'A'
                                                                        )
                                                                    AND C.DISP_FACTOR_CD = D.DISP_FACTOR_CD
                                                                    AND C.DEL_FLAG = 'A'
                                                                    AND D.DEL_FLAG = 'A'
                                                                 )
                                                        ORDER BY LEVEL_CD
                                                               , DISP_FACTOR_CD ASC
                                                          )
                                                   ) M
                                                   , TB_IEM916 O, TB_IEM916 P ,TB_IEM916 Q
                                             WHERE N.DISP_FACTOR_CD (+)= M.DISP_FACTOR_CD
                                             AND O.ETC_CD(+)= N.NORMAL_FACTOR_CD
                                             AND O.DEL_FLAG(+) = 'A'
                                             AND O.PLANT_CD(+) = N.PLANT_CD
                                             AND P.ETC_CD(+)= N.NORMAL_FACTOR_CD2
                                             AND P.DEL_FLAG(+) = 'A'
                                             AND P.PLANT_CD(+) = N.PLANT_CD
                                             AND Q.GUBN_CD(+)  = 'RID'
                                             AND Q.ETC_CD(+)   = N.REWORK_INSP_DIV
                                             AND Q.DEL_FLAG(+) = 'A'
                                             AND Q.PLANT_CD(+) = N.PLANT_CD
                                            ) X
                                          , TB_IEM713 R
                                      WHERE X.PLANT_CD = R.PLANT_CD(+)
                                        AND X.PURCH_LOT_NO = R.BOX_LOT_NO(+)
                                        AND R.DEL_FLAG(+) = 'A'
                                      GROUP BY X.PLANT_CD
                                          , X.PROD_WC_CD
                                          , X.TOP_BOTTOM
                                          , X.IN_LOT_NO
                                          , X.LOT_NO
                                          , DECODE( R.INSPECT_LOT_NO, NULL, X.AR_WARHS_CREATE_NO||X.PURCH_LOT_NO, R.INSPECT_LOT_NO )
                                     ) J
                                   , TB_PCS_COPY K
                               WHERE K.NO <= 2
                                 AND J.PROD_GROUP = '344100'
                               GROUP BY DECODE( K.NO, 1, '0000', 2, '0000'||J.IN_LOT_NO||J.AR_WARHS_CREATE_NO )
                              ) O
                            , TB_PCS_COPY P
                        WHERE P.NO <= 2
                        GROUP BY DECODE( P.NO, 1, '00', 2, '00'||KEY1 )
                       ) R
                )S, TB_IEM120 U
                WHERE S.PLANT_CD = U.PLANT_CD(+)
                AND S.I_BE_AR_NO = U.AR_WARHS_CREATE_NO(+)
         )

         '''.format(start_date, end_date, start_date, end_date)
         )                                                                    
                                                                               
#연신, 코팅 Lot 추적                                                                               
def lottrace(lot):
    return(
    '''
    SELECT unique_lot_no, prod_cd, prod_wc_cd, norm_qty FROM

	(SELECT DISTINCT unique_lot_no, prod_cd, prod_wc_cd, norm_qty FROM
 
		(SELECT unique_lot_no, prod_date, prod_wc_cd, prod_seq_no, o_global_create_no, i_global_create_no, prod_cd, normal_qty + normal_corr_qty norm_qty FROM tb_iem120,
		
           (SELECT o_global_create_no, i_global_create_no FROM tb_iem131 a, tb_iem120 b WHERE a.i_global_create_no = b.global_create_no AND a.del_flag = 'A' AND b.prod_wc_cd LIKE '%%')
		WHERE o_global_create_no = global_create_no)
  
		START WITH prod_date = '{}' AND prod_wc_cd = '{}' AND prod_seq_no = '{}'
		CONNECT BY PRIOR i_global_create_no = o_global_create_no)

    WHERE SUBSTR(prod_wc_cd, 2, 1) in ('E', 'C')    
     
    AND NOT SUBSTR(prod_cd, 3, 3) in ('APF')                   
    '''.format(lot[:8], lot[8:12], lot[12::]))
  
#코팅 Lot 추적
def lottrace2(lot):
    return(
   '''
    SELECT unique_lot_no, prod_cd, prod_wc_cd, norm_qty FROM

	(SELECT DISTINCT unique_lot_no, prod_cd, prod_wc_cd, norm_qty FROM
 
		(SELECT unique_lot_no, prod_date, prod_wc_cd, prod_seq_no, o_global_create_no, i_global_create_no, prod_cd, normal_qty + normal_corr_qty norm_qty FROM tb_iem120,
		
           (SELECT o_global_create_no, i_global_create_no FROM tb_iem131 a, tb_iem120 b WHERE a.i_global_create_no = b.global_create_no AND a.del_flag = 'A' AND b.prod_wc_cd LIKE '%%')
		WHERE o_global_create_no = global_create_no)
  
		START WITH prod_date = '{}' AND prod_wc_cd = '{}' AND prod_seq_no = '{}'
		CONNECT BY PRIOR i_global_create_no = o_global_create_no)

    WHERE SUBSTR(prod_wc_cd, 2, 1) in ('E', 'C')  
       
    AND NOT SUBSTR(prod_cd, 3, 3) in ('APF')                      
    '''.format(lot[:8], lot[8:12], lot[12::]))

  
#%%
def after_coating(lot):
    return(
   '''
    SELECT unique_lot_no FROM

	(SELECT DISTINCT unique_lot_no, prod_cd, prod_wc_cd, norm_qty FROM

		(SELECT unique_lot_no, prod_date, prod_wc_cd, prod_seq_no, o_global_create_no, i_global_create_no, prod_cd, normal_qty + normal_corr_qty norm_qty FROM tb_iem120,

           (SELECT o_global_create_no, i_global_create_no FROM tb_iem131 a, tb_iem120 b WHERE a.i_global_create_no = b.global_create_no AND a.del_flag = 'A' AND b.prod_wc_cd LIKE '%%')

		WHERE i_global_create_no = global_create_no)

    START WITH prod_date = '{}' AND prod_wc_cd = '{}' AND prod_seq_no = '{}'

    CONNECT BY PRIOR o_global_create_no = i_global_create_no)

    WHERE SUBSTR(prod_wc_cd, 2, 1) in ('C', 'L', 'H')

    AND NOT SUBSTR(prod_cd, 3, 3) in ('APF')                     
    '''.format(lot[:8], lot[8:12], lot[12::]))
  
  
  

#연태 검사실적
def yt_inspection(start_date, end_date):
    return(
    '''
    SELECT F_FIND_CC_LOT(X.global_create_no) 코팅, Z.unique_lot_no 재단, 검사, 투입수, 불량수, 불량명, 코드, 제품명, 생산호기, z.remark FROM

        (SELECT 
              global_create_no, normal_qty 투입수, disproduct_qty 불량수, unique_lot_no 검사, d.prod_cd 코드, d.prod_nm 제품명, c.disp_factor_cd 불량명, prod_wc_cd 생산호기
		FROM
        		tb_iem401 b,
			tb_iem120 a,
			(SELECT * FROM tb_iem930 WHERE plant_cd = 'G181' AND dong_cd ='G18101') c,
			(SELECT * FROM tb_iem903 WHERE plant_cd = 'G181' AND dong_cd = 'G18101') d
		WHERE
			a.ar_warhs_create_no = b.ar_warhs_create_no(+) AND
   
			b.disp_factor_cd = c.disp_factor_cd(+) AND
   
			d.prod_cd = a.prod_cd AND
   
			prod_date BETWEEN '{}' AND '{}' AND
   
			prod_wc_cd LIKE '%FS%' AND
   
			d.prod_nm LIKE '%LH%' AND
   
			a.del_flag = 'A' AND
           
                 b.del_flag(+) = 'A'
   
			) X, tb_iem131 Y, tb_iem120 Z 
        
    WHERE X.global_create_no = Y.o_global_create_no AND 
    
    Z.global_create_no = Y.i_global_create_no
    '''.format(start_date, end_date)
    )
                                                                         
# LQMS 물성 데이터
def lqms_data(prod_wc_cd, prod_cd, start_date, end_date, *items):
    
    if len(items) == 1:
        return(
        '''
        SELECT lot_no, c.prod_cd, b.measure_nm1, unit, a.measure_cnt, measure_value, then_usl, then_lsl, measure_judge FROM L_LOT_MEASURE_RESULT a,

        (SELECT measure_cd, measure_nm1, unit FROM L_MEASURE_MASTER WHERE global_site_cd = 'KROC01') b,
    
        tb_iem120@iepcs c
    
        WHERE a.measure_cd = b.measure_cd
    
        AND lot_no = c.unique_lot_no
    
        AND lot_no LIKE '%{}%'
        
        AND prod_cd LIKE '%{}%'
    
        AND prod_date BETWEEN '{}' AND '{}'
    
        AND measure_nm1 = '{}'
    
        '''.format(prod_wc_cd, prod_cd, start_date, end_date, items[0])
        )
        
    if len(items) > 1:
        return(
        '''
        SELECT lot_no, c.prod_cd, b.measure_nm1, unit, a.measure_cnt, measure_value, then_usl, then_lsl, measure_judge FROM L_LOT_MEASURE_RESULT a,

        (SELECT measure_cd, measure_nm1, unit FROM L_MEASURE_MASTER WHERE global_site_cd = 'KROC01') b,
    
        tb_iem120@iepcs c
    
        WHERE a.measure_cd = b.measure_cd
    
        AND lot_no = c.unique_lot_no
    
        AND lot_no LIKE '%{}%'
        
        AND prod_cd LIKE '%{}%'
    
        AND prod_date BETWEEN '{}' AND '{}'
    
        AND measure_nm1 IN {}
    
        '''.format(prod_wc_cd, prod_cd, start_date, end_date, items)
        )        
        
    else:
        return( 
        '''
        SELECT lot_no, c.prod_cd, b.measure_nm1, unit, a.measure_cnt, measure_value, then_usl, then_lsl, measure_judge FROM L_LOT_MEASURE_RESULT a,

        (SELECT measure_cd, measure_nm1, unit FROM L_MEASURE_MASTER WHERE global_site_cd = 'KROC01') b,
    
        tb_iem120@iepcs c
    
        WHERE a.measure_cd = b.measure_cd
    
        AND lot_no = c.unique_lot_no
    
        AND lot_no LIKE '%{}%'
        
        AND prod_cd LIKE '%{}%'
    
        AND prod_date BETWEEN '{}' AND '{}'
        
        '''.format(prod_wc_cd, prod_cd, start_date, end_date)
        )
                                                                                  
def read_model(customer, grade, model):
    return(
    '''
    SELECT customer, npi_grade as grade, part_no, up_down, model, stickiness, stickiness2, npi_mode_type as mode_type,
    
    npi_app_type as app_type FROM PRODUCE_RESULT_DETAIL where customer LIKE '%{}%' and npi_grade LIKE '%{}%' and model LIKE '%{}%'  
    
    '''.format(customer, grade, model)

)
                                                                                