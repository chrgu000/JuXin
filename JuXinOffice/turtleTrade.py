# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 13:16:21 2017

@author: Administrator
"""
from WindPy import *
from matplotlib.pylab import date2num
from pylab import *  
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import numpy as np
import pymysql,datetime
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


ordersLimit=4
capital=10000000
fig=5 # how many figures to be shown

loadData=0
minTick=0.5
contractMulti=100
nameFuture='I.DCE'
#minTick=1
#contractMulti=10
#nameFuture='RB.SHF'

yesterday=(datetime.date.today()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
conn=pymysql.connect('localhost','caofa','caofa')
cur=conn.cursor()
if loadData:
    w.start()
    data=w.wsi(nameFuture,'open,close,high,low','2014-9-5',yesterday,'BarSize=15')
    dateMinute=np.array(data.Times)
    dataMinute=np.column_stack(data.Data)
    data=w.wsd(nameFuture,'open,close,high,low','2014-5-5',yesterday)
    tem=data.Times
    dateDay=np.array([tem[i].date() for i in range(len(tem))])
    dataDay=np.column_stack(data.Data)
    
    cur.execute('drop database if exists turtleTrade')
    cur.execute('create database turtleTrade')
    conn.select_db('turtleTrade')
    cur.execute('create table dataDay(date date,opens float,closes float,highs float,lows float)')
    dataDay=np.column_stack([dateDay,dataDay])
    cur.executemany('insert into dataDay values(%s,%s,%s,%s,%s)',dataDay.tolist())
    cur.execute('create table dataMinute(date datetime,opens float,closes float,highs float,lows float)')
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
times=dataMinute[:,0]
dates=np.array([times[i].date() for i in range(len(times))])
opens=dataMinute[:,1]
closes=dataMinute[:,2]
highs=dataMinute[:,3]
lows=dataMinute[:,4]

up10=[]
down10=[]
up20=[]
down20=[]
up55=[]
down55=[]

for i in range(len(dates)):
    tem=(dateDay<dates[i]).sum()    
    up10.append(highDay[tem-10:tem].max())
    down10.append(lowDay[tem-10:tem].min())
    up20.append(highDay[tem-20:tem].max())
    down20.append(lowDay[tem-20:tem].min())
    up55.append(highDay[tem-55:tem].max())
    down55.append(lowDay[tem-55:tem].min())

hold=0 # 0 means hold none;1 means hold long; -1 means hold short;
stopLoss=0
openPrice=[]
openi=[] #  open bar number
ATR=0
capiDelta=[]
capiDeltai=[]
winR=0
lossR=0

for i in range(len(dates)):
    holdCheck=hold
    if hold==0: # no orders
        upOpen=up20[i]
        downOpen=down20[i]
#        if len(capiDelta)==0:
#            upOpen=up20[i]
#            downOpen=down20[i]
#        elif capiDelta[-1]>=0 or 1:
#            upOpen=up20[i]
#            downOpen=down20[i]
#        else:
#            upOpen=up55[i]
#            downOpen=down55[i]    
        if highs[i]>upOpen: # open first long order
            hold=1
            openi.append(i)
            if upOpen>opens[i]:
                tem=upOpen
            else:
                tem=opens[i]
            openPrice.append(tem+minTick)
            tem=(dateDay<dates[i]).sum()-1
            ATR=max([highDay[tem]-lowDay[tem],abs(highDay[tem]-closeDay[tem-1]),abs(lowDay[tem]-closeDay[tem-1])])
            hands=capital//(100*contractMulti*ATR)
            stopLoss=openPrice[-1]-2*ATR
        elif lows[i]<downOpen: # open first short order
            hold=-1
            openi.append(i)
            if downOpen>opens[i]:
                tem=opens[i]
            else:
                tem=downOpen
            openPrice.append(tem-minTick)
            tem=(dateDay<dates[i]).sum()-1
            ATR=max([highDay[tem]-lowDay[tem],abs(highDay[tem]-closeDay[tem-1]),abs(lowDay[tem]-closeDay[tem-1])])
            hands=capital//(100*contractMulti*ATR)
            stopLoss=openPrice[-1]+2*ATR
    elif hold==1: # hold long orders
        stop1=lows[i]<stopLoss;stop2=lows[i]<down10[i]
        if highs[i]-openPrice[-1]>ATR/2 and len(openPrice)<ordersLimit : # long another one
            if openPrice[-1]+ATR/2 >opens[i]:
                tem=openPrice[-1]+ATR/2
            else:
                tem=opens[i]
            openPrice.append(tem+minTick)
            openi.append(i)
            stopLoss=openPrice[-1]-2*ATR
        elif stop1 + stop2: # close orders
            hold=0
            capiDeltai.append(dates[i])
            if stop1 * stop2:
                stop12=max(down10[i],stopLoss)
            elif stop1:
                stop12=stopLoss
            else:
                stop12=down10[i]
            tem=0
            for i2 in range(len(openPrice)):
                tem1=(stop12-openPrice[i2])*contractMulti*hands
                tem=tem+tem1
                if tem1>0:
                    winR=winR+1
                else:
                    lossR=lossR+1
            capiDelta.append(tem)
    else: # hold short orders
        stop1=highs[i]>stopLoss;stop2=highs[i]>up10[i]
        if openPrice[-1]-lows[i]>ATR/2 and len(openPrice)<ordersLimit: # short another one
            if openPrice[-1]-ATR/2 >opens[i]:
                tem=opens[i]
            else:
                tem=openPrice[-1]-ATR/2
            openPrice.append(tem-minTick)
            openi.append(i)
            stopLoss=openPrice[-1]+2*ATR
        elif stop1 + stop2: # close orders
            hold=0
            capiDeltai.append(dates[i])
            if stop1 * stop2:
                stop12=min(up10[i],stopLoss)
            elif stop1:
                stop12=stopLoss
            else:
                stop12=up10[i]
            tem=0
            for i2 in range(len(openPrice)):
                tem1=(openPrice[i2]-stop12)*contractMulti*hands
                tem=tem+tem1
                if tem1>0:
                    winR=winR+1
                else:
                    lossR=lossR+1
            capiDelta.append(tem)
    if i==len(dateMinute)-1 and hold!=0:
        tem=0
        for i2 in range(len(openPrice)):
            tem=tem+(openPrice[i2]-closes[i])*contractMulti*hands*hold
            capiDelta.append(tem)
    if holdCheck!=0 and hold==0:
        if fig>0:
            fig=fig-1
            plt.figure(figsize=(30,8))
            candleData=[]
            datenum=[]
            u10=[]
            d10=[]
            u20=[]
            d20=[]
            startK=openi[0]-5
            if startK<0:
                startK=0
            for i2 in range(i-openi[0]+10):
                tem=date2num(times[startK+i2])
                datenum.append(tem)
                tem=(tem,opens[startK+i2],highs[startK+i2],lows[startK+i2],closes[startK+i2])
                candleData.append(tem)
                u10.append(up10[startK+i2])
                d10.append(down10[startK+i2])
                u20.append(up20[startK+i2])
                d20.append(down20[startK+i2])
            ax=plt.subplot()
            ax.xaxis_date()
            plt.xticks(rotation=45)
            plt.yticks()
            plt.xlabel('Date')
            plt.ylabel('Price')
            mpf.candlestick_ohlc(ax,candleData,width=0.1,colorup='r',colordown='g')
            plt.grid()
            plt.plot(datenum,u10,color='y',linewidth='1')
            plt.plot(datenum,d10,color='y',linewidth='1')
            plt.plot(datenum,u20,color='r',linewidth='1')
            plt.plot(datenum,d20,color='r',linewidth='1')         
            for i2 in range(len(openPrice)):
                x_=[date2num(times[openi[i2]]),date2num(times[i])]
                y_=[openPrice[i2],stop12]
                plt.plot(x_,y_,color='b',linewidth='2')     
                
        openPrice=[]
        openi=[]
        
    
        
    
capiDeltai.insert(0,dateDay[0])
capiDelta.insert(0,capital)
tem=np.cumsum(capiDelta)
Re=[tem[0]]
for i in range(1,len(dateDay)):    
    Re.append(tem[(np.array(capiDeltai)< dateDay[i]).sum()-1])

RePerYear=pow(Re[-1]/Re[0],1/3)-1
backMaxPer=0
backMax=0
for i in range(1,len(Re)):
    tem=max(Re[:i])
    if tem-Re[i]>backMax:
        backMax=tem-Re[i]
    tem=(tem-Re[i])/tem
    if tem>backMaxPer:
        backMaxPer=tem
winRatio=winR/(winR+lossR)

fig=plt.figure(figsize=(12,8))
plt.title(nameFuture+':'+'年化收益 %.2f%%;总获利 %.1f;最大损失 %.1f;最大回撤率 %.2f%%;胜率 %.3f%%' %(RePerYear,Re[-1]-Re[0],backMax,backMaxPer,winRatio*100),size=15)
ax1=fig.add_subplot(1,1,1)
line1,=ax1.plot(closeDay,color='g')
plt.grid()
plt.xticks(rotation=60,size=12)
ax1.set_ylabel(nameFuture+'走势图',size=12)
ax2=ax1.twinx()
line2,=ax2.plot(Re,color='r')
ax2.set_ylabel('策略资金曲线',size=12)
tem=list(map(int,np.linspace(0,len(dateDay),12)))
tem[-1]=tem[-1]-1
ax2.set_xticks(tem)
tem=np.array([i.strftime('%Y-%m-%d') for i in dateDay])[tem]
ax2.set_xticklabels(tem,rotation=60)
ax1.yaxis.label.set_color(line1.get_color())  
ax2.yaxis.label.set_color(line2.get_color()) 
ax1.tick_params(axis='y', colors=line1.get_color())  
ax2.tick_params(axis='y', colors=line2.get_color())  






    





























