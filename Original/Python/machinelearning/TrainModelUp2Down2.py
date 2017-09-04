# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:46:01 2017

@author: Administrator
"""

from hmmlearn.hmm import GaussianHMM
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from matplotlib.pylab import date2num
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import numpy as np
import pandas as pd
import pymysql,time,TrainModel

x1=time.clock()

firstTime=0; shuffleSample=0; #shuffle Matrix for sample points
ReSet=0
nameDB='Up2Down2' # should be set for create a new mode test;
TradeScan=0 # 1 means match tradescan exactly but waste much time for this procedure and 0 means approxcimate but very fast;

TM=TrainModel.TrainModel(nameDB)
if ReSet:
    conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
    cur=conn.cursor()
    cur.execute('drop database '+nameDB)
    conn.commit()
    cur.close()
    conn.close()
    firstTime=1
if firstTime:
    fig=10 # how many figures ploted to show the confirmed model;
    conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
    cur=conn.cursor()
    cur.execute('create database if not exists '+nameDB) # create database;        
    conn.select_db('pythonStocks')     
    Lstocks=cur.execute('select number from stocks') # select name from stocks: get stocks' name;
    Number=np.insert(np.cumsum(cur.fetchall()),0,0)
    cur.execute('select name from stocks') # select name from stocks: get stocks' name;
    stocks=cur.fetchall()
    cur.execute('select * from dataDay') #'select * from dataDay limit '
    dataAll=np.column_stack(cur.fetchall())
    Re=[]
    dateAll=[]
    Matrix=[]
    for i in range(Lstocks):
        print('%s:%d' %(stocks[i][0],i+1),end=' ',flush=True) #print(i, sep=' ', end=' ', flush=True)
        startT=Number[i]
        endT=Number[i+1]
        dates=dataAll[0][startT:endT]
        opens=dataAll[1][startT:endT]
        closes=dataAll[2][startT:endT]
        highs=dataAll[3][startT:endT]
        lows=dataAll[4][startT:endT]
        vols=dataAll[5][startT:endT]
        turns=dataAll[6][startT:endT]
        
        Lt=len(opens)
        if Lt<20:
            continue
    #        maN=np.zeros(Lt)
    #        ma10=np.zeros(Lt)
    #        for i2 in range(10,Lt):
    #            maN[i2]=np.mean(closes[i2-3:i2+1])
    #            ma10[i2]=np.mean(closes[i2-10:i2+1])
        for i2 in range(15,Lt-3):
            if lows[i2-3]<=min(lows[i2-5:i2+1]) and highs[i2-2]>highs[i2-3] and highs[i2-1]>highs[i2] and lows[i2-1]>lows[i2] and \
            highs[i2-3]>lows[i2-3] and highs[i2-2]>lows[i2-2]and highs[i2-1]>lows[i2-1]and highs[i2]>lows[i2] and closes[i2]/closes[i2-1]<1.095: #vols[i2-2:i2].min()>vols[[i2-3,i2]].max() and 
                if closes[i2+1]>closes[i2]:
                    Re.append(closes[i2+2]/closes[i2]-1)
                else:
                    Re.append(closes[i2+1]/closes[i2]-1)
                dateAll.append(dates[i2])
                max5near=max(closes[i2-4:i2+1]);max5far=max(closes[i2-9:i2-4]);
                min5near=min(closes[i2-4:i2+1]);min5far=min(closes[i2-9:i2-4]);
                max_7near=max(highs[i2-6:i2+1]);max_7far=max(highs[i2-13:i2-6]);
                min_7near=min(lows[i2-6:i2+1]);min_7far=min(lows[i2-13:i2-6]);
                if max5near>max5far and min5near>min5far:
                    ud5=1
                elif max5near<max5far and min5near<min5far:
                    ud5=-1
                else:
                    ud5=0
                if max_7near>max_7far and min_7near>min_7far:
                    ud_7=1
                elif max_7near<max_7far and min_7near<min_7far:
                    ud_7=-1
                else:
                    ud_7=0                                                       
                tem=[ opens[i2]/highs[i2-1],\
                     lows[i2]/highs[i2-1],\
                     min5near/min5far,\
                     closes[i2-4:i2].mean()/closes[i2-9:i2].mean(),\
                     max5near/max5far,\
                     highs[i2-4:i2].mean()/highs[i2-9:i2].mean(),\
                     lows[i2]/opens[i2-1],\
                     highs[i2]/highs[i2-1],\
                     lows[i2]/lows[i2-1],\
                     lows[i2]/closes[i2-1],\
                     (vols[i2]+vols[i2-1])/(vols[i2-3]+vols[i2-2]),\
                     vols[i2-1]/vols[i2-2],\
                     vols[i2]/vols[i2-2],\
                     closes[i2-4:i2].std()/closes[i2-9:i2].std(),\
                     highs[i2]/closes[i2-1],\
                     ud_7,\
                     opens[i2]/closes[i2-1],\
                     vols[i2-1]/vols[i2-3],\
                     highs[i2]/lows[i2-1],\
                     vols[i2]/vols[i2-3],\
                     closes[i2]/np.mean(opens[i2-4:i2]),\
                     pd.DataFrame([lows[i2-3],opens[i2-3],closes[i2-3],highs[i2-3]])[0].corr(pd.DataFrame([lows[i2],closes[i2],opens[i2],highs[i2]])[0]),\
                     vols[i2]/vols[i2-1],\
                     highs[i2-4:i2].std()/highs[i2-9:i2].std(),\
                     vols[i2-2]/vols[i2-3],\
                     np.std([ closes[i2],opens[i2],highs[i2],lows[i2] ])/np.std([closes[i2-1],opens[i2-1],highs[i2-1],lows[i2-1]]),\
                     closes[i2]/closes[i2-1],\
                     opens[i2]/lows[i2-1],\
                     highs[i2]/opens[i2-1] ]                
                Matrix.append(tem)
                if fig>0:
                    fig=fig-1
                    plt.figure()
                    candleData=[]
                    for i3 in range(i2-10,i2+3):
                        tem=(date2num(dates[i3]),opens[i3],highs[i3],lows[i3],closes[i3])
                        candleData.append(tem)
                    ax=plt.subplot()
                    ax.xaxis_date()
                    plt.xticks(rotation=45)
                    plt.yticks()
                    plt.title(stocks[i][0])
                    plt.xlabel('Date')
                    plt.ylabel('Price')
                    mpf.candlestick_ohlc(ax,candleData,width=0.8,colorup='r',colordown='g')
                    plt.grid()      
    
    conn.select_db(nameDB)
    Matrix=np.row_stack(Matrix)
    Matrix=np.column_stack((dateAll,Re,Matrix))
    cur.execute('create table indicators(date date,Re float,ind1 float,ind2 float,ind3 float,ind4 float,ind5 float,ind6 float,ind7 float,ind8 float,\
    ind9 float,ind10 float,ind11 float,ind12 float,ind13 float,ind14 float,ind15 float,ind16 float,ind17 float,ind18 float,ind19 float,ind20 float,ind21 float,ind22 float,\
    ind23 float,ind24 float,ind25 float,ind26 float,ind27 float,ind28 float,ind29 float)')
    cur.executemany('insert into indicators values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', Matrix.tolist()) 
    
    dateAll=Matrix[:,0]
    Re=Matrix[:,1]
    Matrix=Matrix[:,2:]
    dispersity,profitP=TM.hmmTestAll(Matrix,Re,0)  
    cur.execute('create table dispersity(dis float)')
    cur.executemany('insert into dispersity values(%s)',dispersity.tolist())
    cur.execute('create table profitP(flag0 float,flag1 float,flag2 float,flag3 float,flag4 float)')
    for i in range(len(profitP)):
        if len(profitP[i])<5:
            while 1:
                profitP[i].append(-1.0)
                if len(profitP[i])>4:
                    break
    cur.executemany('insert into profitP values(%s,%s,%s,%s,%s)',profitP)
    profitP=np.row_stack(profitP)
    conn.commit()
    cur.close()
    conn.close()
else:
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('select * from indicators')
    Matrix=np.row_stack(cur.fetchall())
    dateAll=Matrix[:,0]
    Re=Matrix[:,1]
    Matrix=Matrix[:,2:]
    if shuffleSample:
        dispersity,profitP=TM.hmmTestAll(Matrix,Re,0)  
        cur.execute('drop table dispersity')
        cur.execute('create table dispersity(dis float)')
        cur.executemany('insert into dispersity values(%s)',dispersity.tolist())
        cur.execute('drop table profitP')
        cur.execute('create table profitP(flag0 float,flag1 float,flag2 float,flag3 float,flag4 float)')
        for i in range(len(profitP)):
            if len(profitP[i])<5:
                while 1:
                    profitP[i].append(-1.0)
                    if len(profitP[i])>4:
                        break
        cur.executemany('insert into profitP values(%s,%s,%s,%s,%s)',profitP)
        profitP=np.row_stack(profitP)
        conn.commit()
        cur.close()
        conn.close()
    else:   
        cur.execute('select * from dispersity')
        dispersity=np.column_stack(cur.fetchall())[0]
        cur.execute('select * from profitP')
        profitP=np.row_stack(cur.fetchall())
        cur.close()
        conn.close()
        
dispersity=dispersity[:-1]
colSelect=np.array(list(range(len(dispersity))))[dispersity>0.35] # -1 delete the last one wich is not for single but for all;
flagNot=[]
for i in range(len(colSelect)):
    flagi=profitP[colSelect[i]]
    flagDi=[]
    for i2 in range(len(flagi)):
        if flagi[i2]<0.35: #profitP<0.4%
            flagDi.append(i2)
    if len(flagDi)>0:
        flagNot.append([colSelect[i],flagDi])
flagOk=[]
for i in range(len(colSelect)):
    flagi=profitP[colSelect[i]]
    flagDi=[]
    for i2 in range(len(flagi)):
        if flagi[i2]>0.6: #profitP>0.8%
            flagDi.append(i2)
    if len(flagDi)>0:
        flagOk.append([colSelect[i],flagDi])
if TradeScan:        
    ReSelectNot=[] #value is 0 or 1
    tem=np.ones(len(Matrix[0]))
    for i in range(len(Matrix)):
        ReSelectNot.append(TM.hmmTestCertainNot([tem.tolist(),Matrix[i].tolist()],flagNot)[-1])
    ReSelectOk=[] # value is 0 or 1 or 2 or ...
    for i in range(len(Matrix)):
        ReSelectOk.append( TM.hmmTestCertainOk([tem.tolist(),Matrix[i].tolist()],flagOk)[-1] )
    ReSelectNot=np.array(ReSelectNot)
    ReSelectOk=np.array(ReSelectOk)
else:    
    ReSelectNot=TM.hmmTestCertainNot(Matrix,flagNot)
    ReSelectOk=TM.hmmTestCertainOk(Matrix,flagOk)

if (sum(ReSelectNot)>0) * (sum(ReSelectOk))>0 :
    plt.figure(figsize=(15,8))
    TM.ReFig([Re[ReSelectNot>0],Re[ReSelectOk>0]],['SelectNot','SelectOk'])
elif sum(ReSelectNot)>0:
    plt.figure(figsize=(15,8))
    TM.ReFig([Re[ReSelectNot>0],],['SelectNot',])
else:
    plt.figure(figsize=(15,8))
    TM.ReFig([Re[ReSelectOk>0],],['SelectOk',]) # select how many flag is match by one Re

pointSelect=(ReSelectOk>0)*(ReSelectNot>0) # draw final select figure;
if sum(pointSelect)>0:
    plt.figure(figsize=(15,8))
    TM.ReFig([Re,Re[pointSelect]],['RawRe','SelectOkNot']) 
# sort all by time;
#    dateSort=dateAll[pointSelect]
#    ReSort=Re[pointSelect]
#    Lt=len(dateSort)
#    month=[]
#    day=[]
#    week=[]
#    weekday=[]    
#    for i2 in range(Lt):
#        month.append(dateSort[i2].strftime('%m'))
#        day.append(dateSort[i2].strftime('%d'))
#        week.append(dateSort[i2].strftime('%W'))
#        weekday.append(dateSort[i2].strftime('%w'))
#    TM.sortStatastic(weekday,ReSort,'selectNotOk--weekday')
#    TM.sortStatastic(month,ReSort,'selectNotOk--month')
#    TM.sortStatastic(day,ReSort,'selectNotOk--day')
#    TM.sortStatastic(week,ReSort,'selectNotOk--week')
    
    # sort according to xgboost;
    MatrixXGB=np.c_[dateAll[pointSelect],Matrix[pointSelect,:]];ReXGB=Re[pointSelect]
    x_train,x_test,y_train,y_test=train_test_split(MatrixXGB,ReXGB,test_size=0.4) #random_state=0,
    date_train=x_train[:,0];x_train=x_train[:,1:21];date_test=x_test[:,0];x_test=x_test[:,1:21]
    tem=int(len(x_test)/5)
    x_validation=x_test[:tem,:];x_test=x_test[tem:,:];y_validation=y_test[:tem];y_test=y_test[tem:];date_test=date_test[tem:]
    
    TM.xgbTrain(x_train,y_train,x_validation,y_validation)
    TM.gaussianNBtrain(x_train,y_train)
    plt.figure(figsize=(25,12))
    for i2 in range(2):
        if i2==0:
            x_=x_train
            y_=y_train
            labeli=['xgbTrain','gaussianTrain']
            date_=date_train
        else:
            x_=x_test
            y_=y_test
            labeli=['xgbTest','gaussianTest']
            date_=date_test
        
        y_pre=TM.xgbPredict(x_)
        y_pre1=y_pre
        flags=np.unique(y_pre)
        Rex=[];labelx=[]
        for i in range(len(flags)):
            tem=y_pre==flags[i]
            Rex.append(y_[tem].tolist())
            labelx.append(labeli[0]+str(flags[i]))
        plt.subplot(2,2,i2+1)
        TM.ReFig(Rex,labelx)   
        y_pre=TM.gaussianNBpredict(x_)
        flags=np.unique(y_pre)
        Rex=[];labelx=[]
        for i in range(len(flags)):
            tem=y_pre==flags[i]
            Rex.append(y_[tem].tolist())
            labelx.append(labeli[1]+str(flags[i]))
        plt.subplot(2,2,i2+3)
        TM.ReFig(Rex,labelx)  
    tem=y_pre1==2
    dateSort=date_test[tem] # sort by time;
    ReSort=y_test[tem]
    Lt=len(dateSort)
    month=[]
    day=[]
    week=[]
    weekday=[]    
    for i2 in range(Lt):
        month.append(dateSort[i2].strftime('%m'))
        day.append(dateSort[i2].strftime('%d'))
        week.append(dateSort[i2].strftime('%W'))
        weekday.append(dateSort[i2].strftime('%w'))
    TM.sortStatastic(weekday,ReSort,'selectNotOk--weekday')
    TM.sortStatastic(month,ReSort,'selectNotOk--month')
    TM.sortStatastic(day,ReSort,'selectNotOk--day')
    TM.sortStatastic(week,ReSort,'selectNotOk--week')      
       
#        wd=np.array([int(date_[i].strftime('%w')) for i in range(len(dateAll))]) #sort according to weekday but not nice;
#        for i in range(2):
#            tem=y_pre==i+1
#            TM.sortStatastic(wd[tem],y_[tem],'flag:'+str(i+1)+'--weekday')

# test this model by hands freely according to your free mind.
flagOk1=[ [0,[1]], ] ;flagOk2=[ [1, [0, 3]], [2, [1, 3, 4]] ]  
flagNot1=[ [0, [0, 2]] ] ;flagNot2=[ [2, [2]], [6, [1, 3]] ]  
ReOk1=TM.hmmTestCertainOk(Matrix,flagOk1)
ReOk2=TM.hmmTestCertainOk(Matrix,flagOk2)
ReNot1=TM.hmmTestCertainNot(Matrix,flagNot1)
ReNot2=TM.hmmTestCertainNot(Matrix,flagNot2)
plt.figure(figsize=(25,12))
plt.subplot(2,2,1)
TM.ReFig([Re[ReOk1>0],Re[ReOk2>0],Re[ReNot1>0],Re[ReNot2>0],],['SelectOk1','SelectOk2','SelectNot1','SelectNot2'])
plt.subplot(2,2,2)
TM.ReFig([Re[(ReOk1>0)*(ReOk2>0)],Re[(ReOk1>0)*(ReNot1>0)],Re[(ReOk1>0)*(ReNot2>0)],Re[(ReOk2>0)*(ReNot1>0)],Re[(ReOk2>0)*(ReNot2>0)],Re[(ReNot1>0)*(ReNot2>0)],],\
             ['Ok1-Ok2','Ok1-Not1','Ok1-Not2','Ok2-Not1','Ok2-Not2','Not1-Not2'])
plt.subplot(2,2,3)
TM.ReFig([Re[(ReOk1>0)*(ReOk2>0)*(ReNot1>0)],Re[(ReOk1>0)*(ReOk2>0)*(ReNot2>0)],Re[(ReOk1>0)*(ReNot1>0)*(ReNot2>0)],Re[(ReOk2>0)*(ReNot1>0)*(ReNot2>0)]],\
             ['Ok1-Ok2-Not1','Ok1-Ok2-Not2','Ok1-Not1-Not2','Ok2-Not1-Not2'])
plt.subplot(2,2,4)
TM.ReFig([Re[(ReOk1>0)*(ReOk2>0)*(ReNot1>0)*(ReNot2)>0]], ['Ok1-Ok2-Not1-Not2'])
    
x2=time.clock()
print('time elapse:%.1f minutes' %((x2-x1)/60))
    













    





    


