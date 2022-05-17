# -*- coding: UTF-8 -*-
import time, datetime
import urllib.request
import pymysql
#import pandas as pd
import numpy as np

INDEX_CODE = "sz300059"
TIME_RANGE = "_5min"


DB = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='share_index')
CURSOR = DB.cursor()

coor = 1
while (coor == 1):

    ## TIME ##
    NOW_TIMES = datetime.datetime.now()
    SELECT_DATE = NOW_TIMES.strftime('%Y%m%d')
    #SELECT_DATE = str(20220428)
    SELECT_HEAD_TIME = (NOW_TIMES-datetime.timedelta(minutes=5)).strftime('%H:%M')
    #SELECT_HEAD_TIME = str("14:55")
    SELECT_TAIL_TIME = (NOW_TIMES-datetime.timedelta(minutes=1)).strftime('%H:%M')
    #SELECT_TAIL_TIME = str("15:00")
    SELECT_HEAD_DATE = (NOW_TIMES-datetime.timedelta(days=15)).strftime('%Y%m%d')
    #SELECT_HEAD_DATE = str(20220405)


    ## BASE DATA ##
    SQL = "SELECT DATE,TIME,TIMESTAMP,INDEX_CODE,NOW_PRICE from "+INDEX_CODE+" where date = '"+SELECT_DATE+"' and time like '"+SELECT_HEAD_TIME+":%' order by time asc limit 1"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    NOW_DATE = ALLDATA[0]
    NOW_TIME = ALLDATA[1]
    TIMESTAMP = ALLDATA[2]
    INDEX_CODE = ALLDATA[3]
    OPEN_PRICE = ALLDATA[4]
    
    SQL = "SELECT NOW_PRICE from "+INDEX_CODE+" where date = '"+SELECT_DATE+"' and time BETWEEN '"+SELECT_HEAD_TIME+":00' AND '"+SELECT_TAIL_TIME+":59' order by time desc limit 1"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    NOW_PRICE = ALLDATA[0]

    MEDIAN_PRICE = round(((float(OPEN_PRICE) + float(NOW_PRICE)) / 2),2)
    RATE = round((NOW_PRICE - OPEN_PRICE) / OPEN_PRICE * 100,2)

    SQL = "SELECT max(A.NOW_PRICE),min(A.NOW_PRICE),avg(A.AVERAGE_PRICE),sum(A.DIFFERENCE) from (SELECT NOW_PRICE,AVERAGE_PRICE,DIFFERENCE from "+INDEX_CODE+" where date = '"+SELECT_DATE+"' and time BETWEEN '"+SELECT_HEAD_TIME+":00' AND '"+SELECT_TAIL_TIME+":59' ) A"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    HIGH_PRICE = ALLDATA[0]
    LOW_PRICE = ALLDATA[1]
    AVERAGE_PRICE = ALLDATA[2]
    DIFFERENCE = ALLDATA[3]


    ## MA ##
    SQL = "SELECT avg(A.NOW_PRICE) FROM (SELECT NOW_PRICE from "+INDEX_CODE+TIME_RANGE+" where date BETWEEN '"+SELECT_HEAD_DATE+"' AND '"+SELECT_DATE+"' order by TIMESTAMP desc limit 5) A"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    MA_5 = ALLDATA[0]

    SQL = "SELECT avg(A.NOW_PRICE) FROM (SELECT NOW_PRICE from "+INDEX_CODE+TIME_RANGE+" where date BETWEEN '"+SELECT_HEAD_DATE+"' AND '"+SELECT_DATE+"' order by TIMESTAMP desc limit 10) A"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    MA_10 = ALLDATA[0]

    SQL = "SELECT avg(A.NOW_PRICE) FROM (SELECT NOW_PRICE from "+INDEX_CODE+TIME_RANGE+" where date BETWEEN '"+SELECT_HEAD_DATE+"' AND '"+SELECT_DATE+"' order by TIMESTAMP desc limit 20) A"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    MA_20 = ALLDATA[0]

    SQL = "SELECT avg(A.NOW_PRICE) FROM (SELECT NOW_PRICE from "+INDEX_CODE+TIME_RANGE+" where date BETWEEN '"+SELECT_HEAD_DATE+"' AND '"+SELECT_DATE+"' order by TIMESTAMP desc limit 60) A"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    MA_60 = ALLDATA[0]


    ## KDJ ##
    SQL = "SELECT max(A.NOW_PRICE),min(A.NOW_PRICE) from (SELECT NOW_PRICE from "+INDEX_CODE+TIME_RANGE+" where date BETWEEN '"+SELECT_HEAD_DATE+"' AND '"+SELECT_DATE+"' order by time desc limit 9) A"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    KDJ_HIGH_PRICE = ALLDATA[0]
    KDJ_LOW_PRICE = ALLDATA[1]
    
    SQL = "SELECT KDJ_K,KDJ_D from "+INDEX_CODE+TIME_RANGE+" where date BETWEEN '"+SELECT_HEAD_DATE+"' AND '"+SELECT_DATE+"' order by time desc limit 1"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    LAST_K = round(float(ALLDATA[0]),2)
    LAST_D = round(float(ALLDATA[1]),2)

    RSV = round(float((NOW_PRICE-KDJ_LOW_PRICE) / (KDJ_HIGH_PRICE-KDJ_LOW_PRICE) * 100),2)
    KDJ_K = round((2/3 * LAST_K) + (1/3 * RSV),2)
    KDJ_D = round((2/3 * LAST_D) + (1/3 * KDJ_K),2)
    KDJ_J = round((KDJ_K * 3) - (KDJ_D * 2),2)


    ## MACD ##
    SQL = "SELECT avg(A.NOW_PRICE) FROM (SELECT NOW_PRICE from "+INDEX_CODE+TIME_RANGE+" where date BETWEEN '"+SELECT_HEAD_DATE+"' AND '"+SELECT_DATE+"' order by TIMESTAMP desc limit 12) A"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    MACD_AVG_12 = round(float(ALLDATA[0]),2)

    SQL = "SELECT avg(A.NOW_PRICE) FROM (SELECT NOW_PRICE from "+INDEX_CODE+TIME_RANGE+" where date BETWEEN '"+SELECT_HEAD_DATE+"' AND '"+SELECT_DATE+"' order by TIMESTAMP desc limit 26) A"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    MACD_AVG_26 = round(float(ALLDATA[0]),2)

    MACD_DIF = round((MACD_AVG_12 - MACD_AVG_26),2)

    SQL = "SELECT avg(A.MACD_DIF) FROM (SELECT MACD_DIF from "+INDEX_CODE+TIME_RANGE+" where date BETWEEN '"+SELECT_HEAD_DATE+"' AND '"+SELECT_DATE+"' order by TIMESTAMP desc limit 9) A"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchone()
    MACD_DEA = round(float(ALLDATA[0]),2)

    MACD_M = round((MACD_DIF - MACD_DEA) * 2,2)


    ## BOLL ##
    BOLL_MID = MA_20

    SQL = "SELECT NOW_PRICE from "+INDEX_CODE+TIME_RANGE+" where date BETWEEN '"+SELECT_HEAD_DATE+"' AND '"+SELECT_DATE+"' order by TIMESTAMP desc limit 20"
    CURSOR.execute(SQL)
    ALLDATA = CURSOR.fetchall()
    MA_20_LIST = []
    for SA in ALLDATA:
        MA_20_ONE = SA[0]
        MA_20_LIST.append(MA_20_ONE)

    BOLL_STD = np.std(MA_20_LIST, ddof = 1)
    BOLL_UP = round(BOLL_MID + BOLL_STD * 2,2)
    BOLL_LOW = round(BOLL_MID - BOLL_STD * 2,2)


    ## SQL COMMIT ##
    SQL = "INSERT INTO "+INDEX_CODE+TIME_RANGE+"(DATE,TIME,TIMESTAMP,INDEX_CODE,OPEN_PRICE,NOW_PRICE,HIGH_PRICE,LOW_PRICE,MEDIAN_PRICE,AVERAGE_PRICE,DIFFERENCE,RATE,MA_5,MA_10,MA_20,MA_60,KDJ_K,KDJ_D,KDJ_J,MACD_M,MACD_DIF,MACD_DEA,BOLL_MID,BOLL_UP,BOLL_LOW) \
            VALUES ('%s','%s',%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
            (NOW_DATE,NOW_TIME,TIMESTAMP,INDEX_CODE,OPEN_PRICE,NOW_PRICE,HIGH_PRICE,LOW_PRICE,MEDIAN_PRICE,AVERAGE_PRICE,DIFFERENCE,RATE,MA_5,MA_10,MA_20,MA_60,KDJ_K,KDJ_D,KDJ_J,MACD_M,MACD_DIF,MACD_DEA,BOLL_MID,BOLL_UP,BOLL_LOW) 
    CURSOR.execute(SQL)
    DB.commit()
    
    #print (NOW_DATE,NOW_TIME,TIMESTAMP,INDEX_CODE,OPEN_PRICE,NOW_PRICE,HIGH_PRICE,LOW_PRICE,MEDIAN_PRICE,AVERAGE_PRICE,DIFFERENCE,MA_5,MA_10,MA_20,MA_60,KDJ_K,KDJ_D,KDJ_J,MACD_M,MACD_DIF,MACD_DEA,BOLL_MID,BOLL_UP,BOLL_LOW)
    time.sleep(300)
DB.close()
