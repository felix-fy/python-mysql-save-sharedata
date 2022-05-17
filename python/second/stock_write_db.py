# -*- coding: UTF-8 -*-
import time,datetime
import urllib.request
import pymysql

LASTURNOVER = 0
for i in range(1,1000000000000000000000000000):
    NOW_TIMES = datetime.datetime.now()
    NOW_WEEK = NOW_TIMES.isoweekday()
    NOW_DATE = NOW_TIMES.strftime('%Y%m%d')
    NOW_TIME = NOW_TIMES.strftime('%H:%M:%S')
    TIMESTAMP = int(time.mktime(NOW_TIMES.timetuple()))
    INDEX_CODE = 'sz300059'
    URL = ('https://qt.gtimg.cn/q=%s' % (INDEX_CODE))
    REP = urllib.request.urlopen(URL)
    RES_DATA = str(REP.read())
    REP = RES_DATA.split("~",37)
    OPEN_PRICE = (REP)[5]
    NOW_PRICE = (REP)[3]
    HIGH_PRICE = (REP)[33]
    LOW_PRICE = (REP)[34]
    MEDIAN_PRICE = round(((float(OPEN_PRICE) + float(NOW_PRICE)) / 2),2) 
    TURNOVER = int((float((REP)[36]) * 100)) 
    RAB_DATA = (REP)[35]
    RAB = RAB_DATA.split("/",2)
    AMOUNT = (RAB)[2]
    AVERAGE_PRICE = round((float(AMOUNT) / float(TURNOVER)),2)
    DIFFERENCE = (float(TURNOVER) - float(LASTURNOVER))
    RATE = (REP)[32]
    LASTURNOVER = TURNOVER
    DB = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='share_index')
    CURSOR = DB.cursor()
    SQL = "INSERT INTO sz300059(DATE,TIME,TIMESTAMP,INDEX_CODE,OPEN_PRICE,NOW_PRICE,HIGH_PRICE,LOW_PRICE,MEDIAN_PRICE,TURNOVER,AMOUNT,AVERAGE_PRICE,DIFFERENCE,RATE) \
            VALUES (%s,'%s',%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
            (NOW_DATE,NOW_TIME,TIMESTAMP,INDEX_CODE,OPEN_PRICE,NOW_PRICE,HIGH_PRICE,LOW_PRICE,MEDIAN_PRICE,TURNOVER,AMOUNT,AVERAGE_PRICE,DIFFERENCE,RATE)
    CURSOR.execute(SQL)
    DB.commit()
    DB.close()
    #print (i,NOW_DATE,NOW_TIME,TIMESTAMP,INDEX_CODE,OPEN_PRICE,NOW_PRICE,HIGH_PRICE,LOW_PRICE,MEDIAN_PRICE,TURNOVER,AMOUNT,AVERAGE_PRICE,RATE)
    time.sleep(10)
