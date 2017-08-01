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

today=datetime.date.today()
yesterday=today-timedelta(days=1)
w.start()
tem=w.wset('sectorconstituent','a001010100000000')
stocks=tem.Data[1]
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
        tem=w.wsd(stocks[i:iend],'volume','ED-3000TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        if len(tem)>1:
            vols.extend(tem)
            break
    while 1:
        tem=w.wsd(stocks[i:iend],'free_turn','ED-3000TD',yesterday,'Fill=Previous','PriceAdj=F').Data
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
    
    





































































