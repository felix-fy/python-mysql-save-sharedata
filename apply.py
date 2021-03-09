#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import time, datetime
import urllib.request
import pymysql
import tensorflow

def MysqlOpen (SQL):
    DB = pymysql.connect(host='127.0.0.1',user='root',password='123456',db='share_index')
    CURSOR = DB.cursor()
    CURSOR.execute(SQL)
    DB.commit()
    BUSS_DATE = CURSOR.fetchone()
    DB.close()
    return BUSS_DATE
  
def JudgeDate ():
    global NOW_TIMES
    NOW_TIMES = datetime.datetime.now()
    global NOW_DATE
    NOW_DATE = NOW_TIMES.strftime('%Y%m%d')
    global NOW_TIME
    NOW_TIME = NOW_TIMES.strftime('%H:%M:%S')
    NOW_TIME_HUER = int(NOW_TIMES.strftime('%H'))
    NOW_TIME_MIN = int(NOW_TIMES.strftime('%M'))
    SQL = "SELECT * FROM xxx WHERE %s' % (NOW_DATE))"
    BUSS_DATE = MysqlOpen (SQL) 
    if BUSS_DATE is not None:
        JudgeTime ()
    else:
        NOW_TIME_SEC = datetime.timedelta(hours=NOW_TIME_HUER,minutes=NOW_TIME_MIN).seconds
        COUNT_SEC = datetime.timedelta(hours=23,minutes=59).seconds+datetime.timedelta(hours=9,minutes=31).seconds
        RESIDUE_TIME = COUNT_SEC-NOW_TIME_SEC
        time.sleep(RESIDUE_TIME)
        JudgeDate ()
        
 def JudgeTime ():
    NOW_TIME_HUER = int(NOW_TIMES.strftime('%H'))
    NOW_TIME_MIN = int(NOW_TIMES.strftime('%M'))
    NOW_TIME_SEC = datetime.timedelta(hours=NOW_TIME_HUER,minutes=NOW_TIME_MIN).seconds
    if 9 <= NOW_TIME_HUER < 15:
        WriteIndex ()
    elif NOW_TIME_HUER < 9:
        COUNT_SEC = datetime.timedelta(hours=9,minutes=31).seconds
        RESIDUE_TIME = COUNT_SEC-NOW_TIME_SEC
        time.sleep(RESIDUE_TIME)
        WriteIndex ()
    else:
        COUNT_SEC = datetime.timedelta(hours=23,minutes=59).seconds+datetime.timedelta(hours=9,minutes=31).seconds
        RESIDUE_TIME = COUNT_SEC-NOW_TIME_SEC
        time.sleep(RESIDUE_TIME)
        JudgeDate ()
        
 def WriteIndex ():
    TIMESTAMP = int(time.mktime(NOW_TIMES.timetuple()))
    INDEX_CODE = 'sz300059'
    URL = ('http://hq.sinajs.cn/list=%s' % (INDEX_CODE))
    REP = urllib.request.urlopen(URL)
    RES_DATA = str(REP.read())
    REP = RES_DATA.split(",",9)
    OPEN_PRICE = (REP)[1]
    NOW_PRICE = (REP)[3]
    HIGH_PRICE = (REP)[4]
    LOW_PRICE = (REP)[5]
    TURNOVER = (REP)[8]
    SQL = "INSERT INTO sz300059(DATE,TIME,TIMESTAMP,INDEX_CODE,OPEN_PRICE,NOW_PRICE,HIGH_PRICE,LOW_PRICE,TURNOVER) VALUES (%s,'%s',%s,'%s',%s,%s,%s,%s,%s)" % (NOW_DATE,NOW_TIME,TIMESTAMP,INDEX_CODE,OPEN_PRICE,NOW_PRICE,HIGH_PRICE,LOW_PRICE,TURNOVER)
    DD = MysqlOpen (SQL)
    print (DD)
    print (TIMESTAMP,INDEX_CODE,OPEN_PRICE,NOW_PRICE,HIGH_PRICE,LOW_PRICE,TURNOVER)
    time.sleep(2)
    JudgeTime ()
