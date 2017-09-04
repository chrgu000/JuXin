# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 13:16:21 2017

@author: Administrator
"""
from WindPy import *
import numpy as np
import pymysql

loadData=0
capital=10000000

conn=pymysql.connect('localhost','caofa','caofa')
cur=conn.cursor()
if loadData:
    w.start()
    data=w.wsi('I.DCE','open,close,high,low','2014-9-5','2017-9-2','BarSize=60')
    tem=data.Times
    dateMinute=np.array([tem[i].date() for i in range(len(tem))])
    dataMinute=np.column_stack(data.Data)
    data=w.wsd('I.DCE','open,close,high,low','2014-5-5','2017-9-2')
    tem=data.Times
    dateDay=np.array([tem[i].date() for i in range(len(tem))])
    dataDay=np.column_stack(data.Data)
    
    cur.execute('drop database if exists turtleTrade')
    cur.execute('create database turtleTrade')
    conn.select_db('turtleTrade')
    cur.execute('create table dataDay(date date,opens float,closes float,highs float,lows float)')
    dataDay=np.column_stack([dateDay,dataDay])
    cur.executemany('insert into dataDay values(%s,%s,%s,%s,%s)',dataDay.tolist())
    cur.execute('create table dataMinute(date date,opens float,closes float,highs float,lows float)')
    dataMinute=np.column_stack([dateMinute,dataMinute])
    cur.executemany('insert into dataMinute values(%s,%s,%s,%s,%s)',dataMinute.tolist())
    conn.commit()
    cur.close()
    conn.close()
else:
    conn.select_db('turtleTrade')
    cur.execute('select * from dataDay')
    dataDay=np.row_stack(cur.fetchall())
    cur.execute('select * from dataMinute')
    dataMinute=np.row_stack(cur.fetchall())
    cur.close()
    conn.close()
   
dateDay=dataDay[:,0]
openDay=dataDay[:,1]
closeDay=dataDay[:,2]
highDay=dataDay[:,3]
lowDay=dataDay[:,4]
dates=dataMinute[:,0]
opens=dataMinute[:,1]
closes=dataMinute[:,2]
highs=dataMinute[:,3]
lows=dataMinute[:,4]

up10=[]
down10=[]
up20=[]
down20=[]
up50=[]
down50=[]
for i in range((dateDay<dateMinute[0]).sum(),len(dateDay)):
    up10.append(max(highDay[i-10:i]))
    down10.append(min(downDay[i-10:i]))
    up20.append(max(highDay[i-20:i]))
    down20.append(min(downDay[i-20:i]))
    up50.append(max(highDay[i-55:i]))
    down50.append(min(downDay[i-55:i]))

hold=0 # 0 means hold none;1 means hold long; -1 means hold short;
stopLoss=0
openPrice=[]
ATR=0
capiDelta=[]
for i in range(len(dateMinute)):
    if hold==0:
        if highs[i]>



    





























