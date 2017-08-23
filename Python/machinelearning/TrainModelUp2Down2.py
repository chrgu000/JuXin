# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:46:01 2017

@author: Administrator
"""

from hmmlearn.hmm import GaussianHMM
from seqlearn.perceptron import StructuredPerceptron
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from matplotlib.colors import ListedColormap
from matplotlib.pylab import date2num
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import numpy as np
import pandas as pd
import scipy.io as sio
import joblib, pymysql,time

import TrainModel

x1=time.clock()
nameDB='Up2Down2'
TM=TrainModel.TrainModel(nameDB)

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
                                   
            tem=[ max5near/max5far,min5near/min5far,vols[i2]/vols[i2-2],ud_7,\
                 pd.DataFrame([lows[i2-3],opens[i2-3],closes[i2-3],highs[i2-3]])[0].corr(pd.DataFrame([lows[i2],closes[i2],opens[i2],highs[i2]])[0]),\
                vols[i2]/vols[i2-3],vols[i2]/vols[i2-1],vols[i2-1]/vols[i2-3],\
                vols[i2-1]/vols[i2-2],vols[i2-2]/vols[i2-3],(vols[i2]+vols[i2-1])/(vols[i2-3]+vols[i2-2]),\
                highs[i2]/highs[i2-1],highs[i2]/opens[i2-1],highs[i2]/lows[i2-1],highs[i2]/closes[i2-1],\
                lows[i2]/highs[i2-1],lows[i2]/opens[i2-1],lows[i2]/lows[i2-1],lows[i2]/closes[i2-1],\
                opens[i2]/highs[i2-1],opens[i2]/opens[i2-1],opens[i2]/lows[i2-1],opens[i2]/closes[i2-1],\
                closes[i2]/closes[i2-1],closes[i2-4:i2].mean()/closes[i2-9:i2].mean(),highs[i2-4:i2].mean()/highs[i2-9:i2].mean(),\
                closes[i2-4:i2].std()/closes[i2-9:i2].std(),highs[i2-4:i2].std()/highs[i2-9:i2].std(),\
                np.std([ closes[i2],opens[i2],highs[i2],lows[i2] ])/np.std([closes[i2-1],opens[i2-1],highs[i2-1],lows[i2-1]])]
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

colSelect=np.array(list(range(len(dispersity))))[dispersity[:-1]>0.35] # -1 delete the last one wich is not for single but for all;
flagDelete=[]
for i in range(len(colSelect)):
    flagi=profitP[colSelect[i]]
    flagDi=[]
    for i2 in range(len(flagi)):
        if flagi[i2]<0.4: #profitP<0.4%
            flagDi.append(i2)
    if len(flagDi)>0:
        flagDelete.append([colSelect[i],flagDi])
flag=TM.hmmTestCertain(Matrix,Re,flagDelete)

tem=dispersity[:-1]>0.35
TM.hmmTestAll(Matrix[:,tem][flag,:],Re[flag],0) 
            
    








cur.close()
conn.close()


tem=np.array(dispersity[:-1]) # delete the last one which is not for single indicator but for all indicators;
indSelected=np.array(range(len(tem)))[tem>0.3]
hmmTestAll(Matrix[:,indSelected],Re,0) 
print(profitP)



    

sw0=1 # get dataset for the model and test all for the first time;
sw1=0 # test selected figures;
sw2=0 # show one figure with one line after delete some bad type (should be done by hand)
sw3=0 # show one figure with different line of hmm sort according to sw2's selected and then show many features according to different date/time;
sw3_1=0 # show many figures and each one is sorted according to different date/time; 
sw4=0 # train by seq   
sw5=0 # PCA

if sw0:   
    
    
selectInd=[0,6,7,9,10,13,14,15,16,17,18,21,23,24,]
#selectInd=range(0,25)
if sw1+sw2+sw3+sw4:  
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)     
    cur=conn.cursor()
    cur.execute('select * from indicators')
    Matrix=np.row_stack(cur.fetchall())
    dateAll=Matrix[:,0]
    Re=Matrix[:,1]
    Matrix=Matrix[:,2:]
    if sw4:
        Matrix=Matrix[:,selectInd]
    else:
        Matrix=Matrix[:,selectInd]
    
#    tem=sio.loadmat(saveData)
#    Matrix=tem['Matrix'] 
#    Rall=tem['Rall']
#    dateAll=tem['dateAll']
#    tem=[]
#    Re=Rall[:,1] #0:return1; 1:return2     

if sw1:    
#    pca=PCA(n_components=12)
#    Matrix=pca.fit_transform(Matrix[:,[0,4,7,8,9,12,13,14,15,16,18,21,26,27,28,29]])
    hmmTestAll(Matrix,Re,0)    
if sw2:    
    flagSelected=[ [0,[1,3]],[3,[1,2]],[4,[2]],[6,[0,2]],[7,[1,2]],[8,[2]],[9,[2]],[10,[3,4]],]
    flag=hmmTestCertain(Matrix,Re,flagSelected)  # flag is 1 or 0;
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('drop table if exists indSelected')
    cur.execute('create table if not exists indSelected(flag tinyint)')
    cur.executemany('insert into indSelected values(%s)', flag.tolist()) 
    conn.commit()
    cur.close()
    conn.close()
if sw3:
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('select * from indSelected')
    indSelected=np.column_stack(cur.fetchall())[0]>0
    Matrix=Matrix[indSelected,:] 
    Re=Re[indSelected]
    dateAll=dateAll[indSelected]
#    pca=PCA(n_components=4)
#    Matrix=pca.fit_transform(Matrix)
    flag=hmmTestAll(Matrix,Re,Matrix.shape[1])
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('drop table if exists flag')
    cur.execute('create table if not exists flag(flag tinyint)')
    cur.executemany('insert into flag values(%s)', flag.tolist()) 
    conn.commit()
    cur.close()
    conn.close()
    
    flagU=np.unique(flag)
    for i in range(len(flagU)):
        tem=flag==flagU[i]
        datei=dateAll[tem]
        Rei=Re[tem]
        Lt=len(datei)
        month=[]
        day=[]
        week=[]
        weekday=[]    
        for i2 in range(Lt):
            month.append(datei[i2].strftime('%m'))
            day.append(datei[i2].strftime('%d'))
            week.append(datei[i2].strftime('%W'))
            weekday.append(datei[i2].strftime('%w'))
        sortStatastic(weekday,Rei,'flag:'+str(flagU[i])+'--weekday')
        sortStatastic(month,Rei,'flag:'+str(flagU[i])+'--month')
        sortStatastic(day,Rei,'flag:'+str(flagU[i])+'--day')
        sortStatastic(week,Rei,'flag:'+str(flagU[i])+'--week')

if sw3_1:
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('select * from indicators')
    Matrix=np.row_stack(cur.fetchall())
    dateAll=Matrix[:,0]
    Re=Matrix[:,1]
    Matrix=Matrix[:,2:] 
    
#    Matrix=Matrix[:,selectInd] # select according to sw2; if comments, select according to raw data;
#    cur.execute('select * from indSelected')
#    indSelected=np.column_stack(cur.fetchall())[0]>0
#    Matrix=Matrix[indSelected,:] 
#    Re=Re[indSelected]
#    dateAll=dateAll[indSelected]

    Lt=len(dateAll)
    month=[]
    day=[]
    week=[]
    weekday=[]    
    for i in range(Lt):
        month.append(dateAll[i].strftime('%m'))
        day.append(dateAll[i].strftime('%d'))
        week.append(dateAll[i].strftime('%W'))
        weekday.append(dateAll[i].strftime('%w'))
    sortStatastic(weekday,Re,'weekday')
    sortStatastic(month,Re,'month')
    sortStatastic(day,Re,'day')
    sortStatastic(week,Re,'week')
    cur.close()
    conn.close()
    
if sw4:
    conn=pymysql.connect('localhost','caofa','caofa',nameDB)
    cur=conn.cursor()
    cur.execute('select * from indSelected')
    indSelected=np.column_stack(cur.fetchall())[0]>0
    Matrix=Matrix[indSelected,:] 
    Re=Re[indSelected]
    dateAll=dateAll[indSelected]

    seqTrain(Matrix,Re,'seqTrain')
    for i in range(Matrix.shape[1]):
        seqTrain(Matrix[:,i],Re,'seqTrain'+'---column'+str(i))

#    cur.execute('select * from flag')
#    flag=np.column_stack(cur.fetchall())[0]
#    flagU=np.unique(flag)
##    flagU=[2] #2,4,1    
#    for i in range(len(flagU)):
#        indTem=flag==flagU[i]
#    
##        for i2 in range(Matrix.shape[1]):
##            X=Matrix[indTem,i2]
##            y=Re[indTem]
##            seqTrain(X,y,'flag:'+str(flagU[i])+'---indicator:'+str(i2))
#        X=Matrix[indTem]
#        y=Re[indTem]
#        seqTrain(X,y,'flag:'+str(flagU[i])+'---indicator:All')    

    cur.close()
    conn.close()
if sw5:
    tem=sio.loadmat(fileName+'Selected')
    flag_sw3=tem['flag_sw3'][0]
    Matrix=tem['Matrix']
    Re=tem['Re'][0]
    dateAll=tem['dateAll']
    PCAtest(Matrix,Re)

x2=time.clock()
print(x2-x1)

    



    



