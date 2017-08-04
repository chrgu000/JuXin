# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 11:36:27 2017

@author: Administrator
"""

#import pymysql
#
#conn=pymysql.connect('localhost','caofa','caofa') # connect to database;
#cur=conn.cursor() # 
#cur.execute('create database if not exists python') # create database;
#conn.select_db('python') 
#cur.execute('create table test(id int,info varchar(20))')
#value=[1,'hi rollen']
#cur.execute('insert into test values(%s,%s)',value)
#values=[]
#for i in range(20):
#    values.append((i,'hi rollen'+str(i)))         
#cur.executemany('insert into test values(%s,%s)',values) 
#cur.execute('update test set info="I am rollen" where id=3')
#conn.commit()
#cur.close()
#conn.close()
#
#conn=pymysql.connect('localhost','caofa','caofa','python')
#cur=conn.cursor()
##conn.select_db('python')
#count=cur.execute('select * from test')
#print('there has %s rows record' % count)
#result=cur.fetchone()
#print (result)
#print ('ID: %s info %s' % result) 
#results=cur.fetchmany(5)
#for r in results:
#    print (r)
#print('=='*10)
#cur.scroll(0,mode='absolute')
#results=cur.fetchall()
#for r in results:
#    print( r[1])
#conn.commit()
#cur.close()
#conn.close()
#conn = pymysql.Connect(host='localhost', user='caofa', passwd='caofa', db='python',charset='utf8') 
##charset是要跟你数据库的编码一样，如果是数据库是gb2312 ,则写charset='gb2312'。
# 
##下面贴一下常用的函数：
##然后,这个连接对象也提供了对事务操作的支持,标准的方法
##commit() 提交
##rollback() 回滚
##cursor用来执行命令的方法:
##callproc(self, procname, args):用来执行存储过程,接收的参数为存储过程名和参数列表,返回值为受影响的行数
##execute(self, query, args):执行单条sql语句,接收的参数为sql语句本身和使用的参数列表,返回值为受影响的行数
##executemany(self, query, args):执行单挑sql语句,但是重复执行参数列表里的参数,返回值为受影响的行数
##nextset(self):移动到下一个结果集
##cursor用来接收返回值的方法:
##fetchall(self):接收全部的返回结果行.
##fetchmany(self, size=None):接收size条返回结果行.如果size的值大于返回的结果行的数量,则会返回cursor.arraysize条数据.
##fetchone(self):返回一条结果行.
##scroll(self, value, mode='relative'):移动指针到某一行.如果mode='relative',则表示从当前所在行移动value条,如果 mode='absolute',则表示从结果集的第一行移动value条.
from WindPy import *
import numpy as np
import pymysql,datetime

sw1=0 # load stocks' data from wind and save it into MySQL database--pythonStocks;
sw2=0 # load new stocks' data and add them into sw1;
sw3=0 # load stocks minutes' data from wind and save it into MySQL database--pythonStocksMinutes;
sw4=0 # load new stocks minutes' data and add them into sw3;
sw5=1 # load Futures minutes' data from wind and save it into MySQL database--pythonFuturesMinutes;

today=datetime.date.today()
yesterday=today-timedelta(days=1)
w.start()
if sw1+sw2+sw3+sw4:
    tem=w.wset('sectorconstituent','a001010100000000')
    stocks=tem.Data[1]
if sw5+sw6:
    tem=w.wset('sectorconstituent','a001010100000000')
    futures=tem.Data[1]

def loadStocks(stocks,yesterday):
    Lt=len(stocks)
    dates=w.tdays('ED-3000TD',yesterday).Data[0]
    opens=[]
    closes=[]
    highs=[]
    lows=[]
    vols=[]
    turns=[]
    for i in range(0,Lt,400):
        if i+400>Lt:
            iend=Lt
        else:
            iend=i+400
        while 1:
            tem=w.wsd(stocks[i:iend],'open','ED-3000TD',yesterday,'Fill=Previous','PriceAdj=F').Data
            if len(tem)>1:
                opens.extend(tem)
                break
        while 1:
            tem=w.wsd(stocks[i:iend],'close','ED-3000TD',yesterday,'Fill=Previous','PriceAdj=F').Data
            if len(tem)>1:
                closes.extend(tem)
                break
        while 1:
            tem=w.wsd(stocks[i:iend],'high','ED-3000TD',yesterday,'Fill=Previous','PriceAdj=F').Data
            if len(tem)>1:
                highs.extend(tem)
                break
        while 1:
            tem=w.wsd(stocks[i:iend],'low','ED-3000TD',yesterday,'Fill=Previous','PriceAdj=F').Data
            if len(tem)>1:
                lows.extend(tem)
                break
        while 1:
            tem=w.wsd(stocks[i:iend],'volume','ED-3000TD',yesterday,'PriceAdj=F').Data
            if len(tem)>1:
                vols.extend(tem)
                break
        while 1:
            tem=w.wsd(stocks[i:iend],'free_turn','ED-3000TD',yesterday,'PriceAdj=F').Data
            if len(tem)>1:
                turns.extend(tem)
                break
    
    conn=pymysql.connect('localhost','caofa','caofa')
    cur=conn.cursor()
    cur.execute('create database if not exists pythonStocks')
    conn.select_db('pythonStocks')
    cur.execute('create table if not exists stocks(name varchar(9))')
    cur.executemany('insert into stocks values(%s)', stocks) 
    for i in range(Lt):
        print(i)
        tem=np.isnan(opens[i]).sum()
        Matrix=[dates[tem:],opens[i][tem:],closes[i][tem:],highs[i][tem:],lows[i][tem:],vols[i][tem:],turns[i][tem:]]
        cur.execute('create table if not exists '+stocks[i][:6]+stocks[i][7:]+'(date date,open float,close float,high float,low float,vol bigint,turn float)')
        cur.executemany('insert into '+stocks[i][:6]+stocks[i][7:]+' values(%s,%s,%s,%s,%s,%s,%s)', np.column_stack(Matrix).tolist()) 
    conn.commit()
    cur.close()
    conn.close()

def addStocks(stocks,yesterday):
    Lt=len(stocks)
    conn=pymysql.connect('localhost','caofa','caofa','pythonStocks')
    cur=conn.cursor()
    tem=cur.execute('select * from 000001SZ')
    cur.scroll(tem-1,'absolute')
    dateStart=cur.fetchone()[0]+datetime.timedelta(days=1)    
    cur.execute('select * from stocks')
    stocksRaw=set([i[0] for i in cur.fetchall()])
    stocks=set(stocks)
    stocksAdd=list(stocks-stocksRaw)
    stocksRaw=list(stocksRaw & stocks) # get their both;
    
    dates=w.tdays(dateStart,yesterday).Data[0]
    if len(dates)<1:
        print('already latest datebase, no need to update again!')
        cur.close()
        conn.close()
        return
    opens=w.wsd(stocksAdd,'open',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
    closes=w.wsd(stocksAdd,'close',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
    highs=w.wsd(stocksAdd,'high',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
    lows=w.wsd(stocksAdd,'low',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
    vols=w.wsd(stocksAdd,'volume',dateStart,yesterday,'PriceAdj=F').Data
    turns=w.wsd(stocksAdd,'free_turn',dateStart,yesterday,'PriceAdj=F').Data
    Lt=len(stocksAdd)
    for i in range(Lt):
        print('add stock-%s %d/%d;' %(stocksAdd[i],i+1,Lt))
        try:
            tem=np.isnan(opens[i]).sum() #for none value pandas.isnull can treate it;
        except:
            continue                
        Matrix=[dates[tem:],opens[i][tem:],closes[i][tem:],highs[i][tem:],lows[i][tem:],vols[i][tem:],turns[i][tem:]]
        cur.execute('create table if not exists '+stocksAdd[i][:6]+stocksAdd[i][7:]+'(date date,open float,close float,high float,low float,vol bigint,turn float)')
        cur.executemany('insert into '+stocksAdd[i][:6]+stocksAdd[i][7:]+' values(%s,%s,%s,%s,%s,%s,%s)', np.column_stack(Matrix).tolist()) 
    cur.executemany('insert into stocks values(%s)', stocksAdd)
    
    opens=[]
    closes=[]
    highs=[]
    lows=[]
    vols=[]
    turns=[]
    Lt=len(stocksRaw)
    for i in range(0,Lt,400):
        if i+400>Lt:
            iend=Lt
        else:
            iend=i+400
        while 1:
            tem=w.wsd(stocksRaw[i:iend],'open',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
            if type(tem[0][0])==float:
                if len(tem)>1:
                    opens.extend(tem)
                else:
                    opens.extend(tem[0])
                break
        while 1:
            tem=w.wsd(stocksRaw[i:iend],'close',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
            if type(tem[0][0])==float:
                if len(tem)>1:
                    closes.extend(tem)
                else:
                    closes.extend(tem[0])
                break
        while 1:
            tem=w.wsd(stocksRaw[i:iend],'high',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
            if type(tem[0][0])==float:
                if len(tem)>1:
                    highs.extend(tem)
                else:
                    highs.extend(tem[0])
                break
        while 1:
            tem=w.wsd(stocksRaw[i:iend],'low',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
            if type(tem[0][0])==float:
                if len(tem)>1:
                    lows.extend(tem)
                else:
                    lows.extend(tem[0])
                break
        while 1:
            tem=w.wsd(stocksRaw[i:iend],'volume',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
            if type(tem[0][0])==float:
                if len(tem)>1:
                    vols.extend(tem)
                else:
                    vols.extend(tem[0])
                break
        while 1:
            tem=w.wsd(stocksRaw[i:iend],'free_turn',dateStart,yesterday,'Fill=Previous','PriceAdj=F').Data
            if type(tem[0][0])==float:
                if len(tem)>1:
                    turns.extend(tem)
                else:
                    turns.extend(tem[0])
                break
    for i in range(Lt):
        print('update stock %d/%d;' %(i+1,Lt))
        if len(dates)==1:
            temCheck=opens[i]
            if type(temCheck)==float:
                if str(temCheck)[0].isdigit():
                    Matrix=np.column_stack([dates[0],opens[i],closes[i],highs[i],lows[i],vols[i],turns[i]]).tolist()
                else:
                    tem=cur.execute('select * from '+stocksRaw[i][:6]+stocksRaw[i][7:])
                    cur.scroll(tem-1,'absolute')
                    tem=cur.fetchone()
                    Matrix=[list(tem)]
                    Matrix[0][0]=yesterday
                    Matrix[0][5]=0
                    Matrix[0][6]=0.0
            else:
                print('the day is not trading day; no need to update database!')
                cur.close()
                conn.close()
                return           
        else:
            temChar=str(opens[i][0])[0]
            if temChar.isdigit():
                Matrix=np.column_stack([dates,opens[i],closes[i],highs[i],lows[i],vols[i],turns[i]]).tolist()
            elif temChar.lower()=='n':
                tem=cur.execute('select * from '+stocksRaw[i][:6]+stocksRaw[i][7:])
                cur.scroll(tem-1,'absolute')
                tem=cur.fetchone()
                Matrix=np.tile(tem,[len(dates),1])
                Matrix[:,0]=dates
                Matrix[:,5]=0
                Matrix[:,6]=0.0
                Matrix=Matrix.tolist()                
            else:
                cur.close()
                conn.close()
                return
        cur.executemany('insert into '+stocksRaw[i][:6]+stocksRaw[i][7:]+' values(%s,%s,%s,%s,%s,%s,%s)', Matrix) 
    conn.commit()
    cur.close()
    conn.close()

def loadStocksMinutes(stocks,today):
    conn=pymysql.connect('localhost','caofa','caofa')
    cur=conn.cursor()
    cur.execute('create database if not exists pythonStocksMinutes')
    conn.select_db('pythonStocksMinutes')
    cur.execute('create table if not exists stocks(name varchar(9))') # 还没有写入
    cur.executemany('insert into stocks values(%s)', stocks) 
    
    Lt=len(stocks)
    for i in range(Lt):
        print('load stock-%s:%d/%d' %(stocks[i],i+1,Lt))
        while 1:
            tem=w.wsi(stocks[i],'open,close,high,low,volume',today-timedelta(days=3*370),today,'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
            if len(tem.Data)>1:
                break
        Matrix=[tem.Times]
        Matrix.extend(tem.Data)
        cur.execute('create table if not exists '+stocks[i][:6]+stocks[i][7:]+'(time datetime,open float,close float,high float,low float,vol int)')
        cur.executemany('insert into '+stocks[i][:6]+stocks[i][7:]+' values(%s,%s,%s,%s,%s,%s)', np.column_stack(Matrix).tolist()) 
    conn.commit()
    cur.close()
    conn.close()
    
def addStocksMinutes(stocks,today):
    conn=pymysql.connect('localhost','caofa','caofa','pythonStocksMinutes')
    cur=conn.cursor()
    tem=cur.execute('select * from 000001SZ')
    cur.scroll(tem-1,'absolute')
    dateStart=cur.fetchone()[0]+datetime.timedelta(minutes=10)    
    
    cur.execute('select * from stocks')
    stocksRaw=set([i[0] for i in cur.fetchall()])
    stocks=set(stocks)
    stocksAdd=list(stocks-stocksRaw)
    stocksRaw=list(stocksRaw & stocks) # get their both;
    
    Lt=len(stocksAdd)
    for i in range(Lt):
        print('add stock-%s:%d/%d' %(stocksAdd[i],i+1,Lt))
        while 1:
            tem=w.wsi(stocksAdd[i],'open,close,high,low,volume',dateStart,today,'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
            if len(tem.Data)>1:
                break
        Matrix=[tem.Times]
        Matrix.extend(tem.Data)
        cur.execute('create table if not exists '+stocksAdd[i][:6]+stocksAdd[i][7:]+'(time datetime,open float,close float,high float,low float,vol int)')
        cur.executemany('insert into '+stocksAdd[i][:6]+stocksAdd[i][7:]+' values(%s,%s,%s,%s,%s,%s)', np.column_stack(Matrix).tolist()) 
    cur.executemany('insert into stocks values(%s)', stocksAdd)
    
    Lt=len(stocksRaw)
    for i in range(Lt):
        print('update stock-%s:%d/%d' %(stocksRaw[i],i+1,Lt))
        tem=w.wsi(stocksRaw[i],'open,close,high,low,volume',dateStart,today,'periodstart=09:30:00;periodend=15:01:00;Fill=Previous;PriceAdj=F')
            if len(tem.Data)>1:
                break
        Matrix=[tem.Times]
        Matrix.extend(tem.Data)
        cur.executemany('insert into '+stocksRaw[i][:6]+stocksRaw[i][7:]+' values(%s,%s,%s,%s,%s,%s)', np.column_stack(Matrix).tolist()) 
    conn.commit()
    cur.close()
    conn.close()    

if sw1:
    loadStocks(stocks,yesterday)
if sw2:
    addStocks(stocks,yesterday)
if sw3: #take up more disk space;
    x1=datetime.datetime.now()
    t1=time.clock()
    loadStocksMinutes(stocks,today)
    x2=datetime.datetime.now()
    print((x2-x1).minutes)
if sw4:
    addStocksMinutes(stocks,today)
if sw5:
    loadFuturesMinutes(futures,today)
    
    
        

    
    
    
    
    
    





































































