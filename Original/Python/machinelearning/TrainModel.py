# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 11:12:35 2017

@author: Administrator
"""

from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb
import joblib, warnings,pymysql,time

warnings.filterwarnings("ignore")

class TrainModel():
    def __init__(self,*args): #nameDB,firstTime,shufflePoints,ReGetPoints,TradeScan
        self.nameDB=args[0]
        self.saveData='D:\\Trade\\Original\\joblib\\'+args[0]
        if len(args)>1:        
            self.firstTime=args[1] 
            self.shufflePoints=args[2]  #shuffle Matrix for sample points
            self.ReGetPoints=args[3] 
            self.TradeScan=args[4]  # 1 means match tradescan exactly but waste much time for this procedure and 0 means approxcimate but very fast;
            self.dispersityX=args[5]
            self.profitNot=args[6]
            self.profitOk=args[7]
        else:
            self.kmean=joblib.load(self.saveData+'ratioOpen_kmean')
        
    def __call__(self,func):
        if self.ReGetPoints:
            conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
            cur=conn.cursor()
            cur.execute('drop database '+self.nameDB)
            conn.commit()
            cur.close()
            conn.close()
            self.firstTime=1
        if self.firstTime:
            fig=5 # how many figures ploted to show the confirmed model;
            conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
            cur=conn.cursor()
            cur.execute('drop database if exists '+self.nameDB) # create database;   
            cur.execute('create database '+self.nameDB) # create database;        
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
            labelMarket=[]
            ratioOpen=[]
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
        #        for i2 in range(15,16):
                    if func(opens[i2-15:i2+1],highs[i2-15:i2+1],lows[i2-15:i2+1],closes[i2-15:i2+1]):
                        if closes[i2+1]>=closes[i2]:
                            Re.append(closes[i2+2]/opens[i2+1]-1.003)
#                            Re.append(opens[i2+2]/opens[i2+1]-1)
                            if fig>0:
                                figx=[-5,-4]
                                figy=[opens[i2+1],closes[i2+2]]
                        else:#elif closes[i2+2]<=closes[i2+1]:
                            Re.append(opens[i2+2]/opens[i2+1]-1.003)
#                            Re.append(closes[i2+2]/opens[i2+1]-1)
                            if fig>0:
                                figx=[-5,-4]
                                figy=[opens[i2+1],opens[i2+2]]
                                
#                        if min(lows[i2+1:i2+3])>=lows[i2]:
#                            Re.append(closes[i2+2]/opens[i2+1]-1.003)
##                            Re.append(opens[i2+2]/opens[i2+1]-1)
#                            if fig>0:
#                                figx=[-5,-4]
#                                figy=[opens[i2+1],closes[i2+2]]
#                        else:#elif closes[i2+2]<=closes[i2+1]:
#                            Re.append(opens[i2+2]/opens[i2+1]-1.003)
##                            Re.append(closes[i2+2]/opens[i2+1]-1)
#                            if fig>0:
#                                figx=[-5,-4]
#                                figy=[opens[i2+1],opens[i2+2]]
                        
                        
#                        elif closes[i2+3]<=closes[i2+2] :
#                            Re.append(closes[i2+3]/closes[i2]-1)
##                            Re.append(closes[i2+2]/opens[i2+1]-1)
#                            if fig>0:
#                                figx=[-6,-3]
#                                figy=[closes[i2],closes[i2+3]]
#                        elif closes[i2+4]<=closes[i2+3] :
#                            Re.append(closes[i2+4]/closes[i2]-1)
##                            Re.append(closes[i2+2]/opens[i2+1]-1)
#                            if fig>0:
#                                figx=[-6,-2]
#                                figy=[closes[i2],closes[i2+4]]
#                        else:
#                            Re.append(closes[i2+5]/closes[i2]-1)
##                            Re.append(closes[i2+2]/opens[i2+1]-1)
#                            if fig>0:
#                                figx=[-6,-1]
#                                figy=[closes[i2],closes[i2+5]]
                                
                            
                        dateAll.append(dates[i2+1])
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
                             (highs[i2]-lows[i2])/(highs[i2-1]-lows[i2-1]),\
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
                        if np.isnan(tem).sum():
                            Re.pop()
                            dateAll.pop()
                            continue
                        labelMarket.append(int(stocks[i][0][0]))
                        ratioOpen.append(opens[i2+1]/closes[i2]-1)
                        Matrix.append(tem)
                        if fig>0:
                            fig=fig-1
                            plt.figure()
                            candleData=[]
                            for i3 in range(i2-10,i2+6):
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
                            plt.plot([candleData[figx[0]][0],candleData[figx[1]][0]],figy,color='b',linewidth='2')
                            plt.grid()      
            
            conn.select_db(self.nameDB)
            Matrix=np.row_stack(Matrix)
            Matrix=np.column_stack((dateAll,Re,labelMarket,ratioOpen,Matrix))
            cur.execute('create table indicators(date date,Re float,ind1 float,ind2 float,ind3 float,ind4 float,ind5 float,ind6 float,ind7 float,ind8 float,\
            ind9 float,ind10 float,ind11 float,ind12 float,ind13 float,ind14 float,ind15 float,ind16 float,ind17 float,ind18 float,ind19 float,ind20 float,ind21 float,ind22 float,\
            ind23 float,ind24 float,ind25 float,ind26 float,ind27 float,ind28 float,ind29 float,ind30 float,ind31 float,ind32 float)')
            cur.executemany('insert into indicators values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', Matrix.tolist()) 
            
            dateAll=Matrix[:,0]
            Re=Matrix[:,1]
            labelMarket=Matrix[:,2]
            ratioOpen=Matrix[:,3]
            Matrix=Matrix[:,4:]
            dispersity,profitP=self.kmeanTestAll(Matrix,Re,0)  
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
            
        else:
            conn=pymysql.connect('localhost','caofa','caofa',self.nameDB)
            cur=conn.cursor()
            cur.execute('select * from indicators')
            Matrix=np.row_stack(cur.fetchall())
            dateAll=Matrix[:,0]
            Re=Matrix[:,1]
            labelMarket=Matrix[:,2]
            ratioOpen=Matrix[:,3]
            Matrix=Matrix[:,4:]
            if self.shufflePoints:
                dispersity,profitP=self.kmeanTestAll(Matrix,Re,0)  
                cur.execute('drop table if exists dispersity')
                cur.execute('create table dispersity(dis float)')
                cur.executemany('insert into dispersity values(%s)',dispersity.tolist())
                cur.execute('drop table if exists profitP')
                cur.execute('create table profitP(flag0 float,flag1 float,flag2 float,flag3 float,flag4 float)')
                for i in range(len(profitP)):
                    if len(profitP[i])<5:
                        while 1:
                            profitP[i].append(-1.0)
                            if len(profitP[i])>4:
                                break
                cur.executemany('insert into profitP values(%s,%s,%s,%s,%s)',profitP)
                profitP=np.row_stack(profitP)
                
            else:   
                cur.execute('select * from dispersity')
                dispersity=np.column_stack(cur.fetchall())[0]
                cur.execute('select * from profitP')
                profitP=np.row_stack(cur.fetchall())

                
        dispersity=dispersity[:-1]
        colSelect=np.array(list(range(len(dispersity))))[dispersity>self.dispersityX] # -1 delete the last one wich is not for single but for all;
        tem=input('please select which colume(1,2,3 like this) for OkNot:')
        if len(tem)>0:
            colSelect=np.array(list(map(int,tem.split(','))))
        colXGB=np.array(list(range(len(dispersity))))[dispersity>0.2]
        tem=input('please select which colume(1,2,3 like this) for XGB:')
        if len(tem)>0:
            colXGB=np.array(list(map(int,tem.split(','))))
        
        cur.execute('drop table if exists colOkNOt') # for tradeScan
        cur.execute('create table colOkNOt(dis tinyint)')
        cur.executemany('insert into colOkNot values(%s)',colSelect.tolist())
        cur.execute('drop table if exists colXGB') # for tradeScan
        cur.execute('create table colXGB(dis tinyint)')
        cur.executemany('insert into colXGB values(%s)',colXGB.tolist())
        conn.commit()
        cur.close()
        conn.close()
            
        flagNot=[]
        for i in range(len(colSelect)):
            flagi=profitP[colSelect[i]]
            flagDi=[]
            for i2 in range(len(flagi)):
                if flagi[i2]<self.profitNot: #profitP<0.4%
                    flagDi.append(i2)
            if len(flagDi)>0:
                flagNot.append([colSelect[i],flagDi])
        flagOk=[]
        for i in range(len(colSelect)):
            flagi=profitP[colSelect[i]]
            flagDi=[]
            for i2 in range(len(flagi)):
                if flagi[i2]>self.profitOk: #profitP>0.8%
                    flagDi.append(i2)
            if len(flagDi)>0:
                flagOk.append([colSelect[i],flagDi])
        if self.TradeScan:        
            ReSelectNot=[] #value is 0 or 1
            tem=np.ones(len(Matrix[0]))
            for i in range(len(Matrix)):
                ReSelectNot.append(self.kmeanTestCertainNot([tem.tolist(),Matrix[i].tolist()],flagNot)[-1])
            ReSelectOk=[] # value is 0 or 1 or 2 or ...
            for i in range(len(Matrix)):
                ReSelectOk.append( self.kmeanTestCertainOk([tem.tolist(),Matrix[i].tolist()],flagOk)[-1] )
            ReSelectNot=np.array(ReSelectNot)
            ReSelectOk=np.array(ReSelectOk)
        else:    
            ReSelectNot=self.kmeanTestCertainNot(Matrix,flagNot)
            ReSelectOk=self.kmeanTestCertainOk(Matrix,flagOk)
        
        if (sum(ReSelectNot)) * (sum(ReSelectOk))>0 :
            plt.figure(figsize=(15,8))
            self.ReFig([Re[ReSelectNot>0],Re[ReSelectOk>0]],['SelectNot','SelectOk'])
        elif sum(ReSelectNot)>0:
            plt.figure(figsize=(15,8))
            self.ReFig([Re[ReSelectNot>0],],['SelectNot',])
        elif sum(ReSelectOk)>0:
            plt.figure(figsize=(15,8))
            self.ReFig([Re[ReSelectOk>0],],['SelectOk',]) # select how many flag is match by one Re
        
        pointSelect=(ReSelectOk>0)*(ReSelectNot>0) # draw final select figure;
        if sum(pointSelect)>0:
            plt.figure(figsize=(15,8))
            self.ReFig([Re,Re[pointSelect]],['RawRe','SelectOkNot']) 
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
        #    self.sortStatastic(weekday,ReSort,'selectNotOk--weekday')
        #    self.sortStatastic(month,ReSort,'selectNotOk--month')
        #    self.sortStatastic(day,ReSort,'selectNotOk--day')
        #    self.sortStatastic(week,ReSort,'selectNotOk--week')
            
            # sort according to xgboost;
            MatrixXGB=np.c_[dateAll[pointSelect],labelMarket[pointSelect],ratioOpen[pointSelect],Matrix[pointSelect,:]];ReXGB=Re[pointSelect]
            X_train,X_test,y_train,y_test=train_test_split(MatrixXGB,ReXGB,test_size=0.5) #random_state=0,
                    
            date_train=X_train[:,0];labelMarket_train=X_train[:,1];ratioOpen_train=X_train[:,2];x_train=X_train[:,colXGB+3];
            date_test=X_test[:,0];labelMarket_test=X_test[:,1];ratioOpen_test=X_test[:,2];x_test=X_test[:,3:]
            tem=int(len(x_test)/10)
            x_validation=x_test[:tem,:][:,colXGB];x_test=x_test[tem:,:];y_validation=y_test[:tem];y_test=y_test[tem:];date_test=date_test[tem:]
            labelMarket_test=labelMarket_test[tem:];ratioOpen_test=ratioOpen_test[tem:]
            
            self.xgbTrain(x_train,y_train,x_validation,y_validation)
            self.gaussianNBtrain(x_train,y_train)
            plt.figure(figsize=(25,24))
            for i2 in range(2):
                if i2==0:
                    x_=X_train[:,3:]
                    y_=y_train
                    labeli=['xgbTrain','gaussianTrain','labelMarket','ratioOpen']
                    date_=date_train
                    labelMarket_=labelMarket_train
                    ratioOpen_=ratioOpen_train
                else:
                    x_=x_test
                    y_=y_test
                    labeli=['xgbTest','gaussianTest','labelMarket','ratioOpen']
                    date_=date_test
                    labelMarket_=labelMarket_test
                    ratioOpen_=ratioOpen_test
                
                y_pre=self.xgbPredict(x_)
                y_pre1=y_pre
                flags=np.unique(y_pre)
                Rex=[];labelx=[]
                for i in range(len(flags)):
                    tem=y_pre==flags[i]
                    Rex.append(y_[tem].tolist())
                    labelx.append(labeli[0]+str(flags[i]))
                plt.subplot(4,2,i2+1)
                self.ReFig(Rex,labelx)  
                
                tem=y_pre1==1
                y_pre=labelMarket_[tem]
                y_tem=y_[tem]
                flags=np.unique(y_pre)
                Rex=[];labelx=[]
                for i in range(len(flags)):
                    tem=y_pre==flags[i]
                    Rex.append(y_tem[tem].tolist())
                    labelx.append(labeli[2]+str(flags[i]))
                plt.subplot(4,2,i2+3)
                self.ReFig(Rex,labelx)  
                
                tem=y_pre1==1
                y_pre=ratioOpen_[tem]
                y_tem=y_[tem]
                if i2==0:
                    kmean=KMeans(n_clusters=5).fit(np.row_stack(y_pre))
                    joblib.dump(kmean,self.saveData+'ratioOpen_kmean')
                    y_pre=kmean.labels_
                else:
                    kmean=joblib.load(self.saveData+'ratioOpen_kmean')
                    y_pre=kmean.predict(np.row_stack(y_pre))
                flags=np.unique(y_pre)
                Rex=[];labelx=[]
                for i in range(len(flags)):
                    tem=y_pre==flags[i]
                    Rex.append(y_tem[tem].tolist())
                    labelx.append(labeli[3]+str(flags[i]))
                plt.subplot(4,2,i2+5)
                self.ReFig(Rex,labelx)    
                
                y_pre=self.gaussianNBpredict(x_)
                flags=np.unique(y_pre)
                Rex=[];labelx=[]
                for i in range(len(flags)):
                    tem=y_pre==flags[i]
                    Rex.append(y_[tem].tolist())
                    labelx.append(labeli[1]+str(flags[i]))
                plt.subplot(4,2,i2+7)
                self.ReFig(Rex,labelx)  
            tem=y_pre1==1
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
            self.sortStatastic(weekday,ReSort,'selectNotOk--weekday')
            self.sortStatastic(month,ReSort,'selectNotOk--month')
            self.sortStatastic(day,ReSort,'selectNotOk--day')
            self.sortStatastic(week,ReSort,'selectNotOk--week')           
        return flagNot,flagOk,Matrix,Re
    
    def kmeanTestAll(self,Xraw,Reraw,figStart): # figStart: how many figs to show 0 means show all and Xcol mean show one (in all)
        Xshape=Xraw.shape
        Xrow=Xshape[0]
        Xcol=Xshape[1]
        if figStart!=Xcol:
            Xraw,X0,Reraw,y0=train_test_split(Xraw,np.array(Reraw),test_size=0.0) #random_state=1
        dispersity=[] # hold dispesity of each column but last one not for some one column but all;
        profitP=[] # hold each type's profit/per of each indicator column
        if figStart!=0:
            colStart=Xcol        
        else:
            colStart=0
        for lp in range(colStart,Xcol+1):
            if lp<Xcol:
                X=Xraw[:,lp]
                figTitle=str(lp)
            else:
                X=Xraw
                figTitle='All'
            trainSample=30000
            if Xrow<trainSample:
                Xtrain=X[:Xrow//2]
                Xtest=X[Xrow//2:]
                Retrain=Reraw[:Xrow//2]
                Retest=Reraw[Xrow//2:]
            else:
                Xtrain=X[:trainSample]
                Xtest=X[trainSample:]    
                Retrain=Reraw[:trainSample]  
                Retest=Reraw[trainSample:]
            if figStart!=0:
                Xtest=X
                Retest=Reraw
                figTitle=str(figStart)

            kmean=KMeans(n_clusters=5).fit(np.row_stack(Xtrain))
            joblib.dump(kmean,self.saveData+figTitle+'_kmean')

            records=[] # hold two recordi
            for i in range(2):
                if i==0:
                    Xtem=Xtrain
                    Retem=Retrain
                else:
                    Xtem=Xtest
                    Retem=Retest
                    
                flag=kmean.predict(np.row_stack(Xtem))
                plt.figure(figsize=(15,8))
                xi=[]
                yi=[]
                recordi=[] # record number of total orders, IR,winratio,ratioWL,profitP
                for i2 in range(kmean.n_clusters):
                    state=(flag==i2)
                    ReT=Retem[state]
                    ReTcs=ReT.cumsum()
                    LT=len(ReT)
                    if LT<2:
                        continue
                    maxDraw=0
                    maxDrawi=0
                    maxDrawValue=0
                    i2High=0
                    for i3 in range(LT):
                        if ReTcs[i3]>i2High:
                            i2High=ReTcs[i3]
                        drawT=i2High-ReTcs[i3]
                        if maxDraw<drawT:
                            maxDraw=drawT
                            maxDrawi=i3
                            maxDrawValue=ReTcs[i3]
                    xi.append(maxDrawi)
                    yi.append(maxDrawValue)  
                    recordi.append([LT,np.mean(ReT)/np.std(ReT),ReTcs[-1]/LT*100])
                    try:
                        plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
                             %(i2,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
                    except:
                        plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%s);maxDraw:%.2f%%;profitP:%.4f%%;'\
                             %(i2,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),'error',maxDraw*100,ReTcs[-1]/LT*100))
                records.append(recordi)
                plt.plot(xi,yi,'r*')
                plt.title(figTitle,fontsize=16)
                
                if i==1:
                    if lp<Xcol:
                        tem=np.sort(Xtem)
                        pointsTem=tem[[list(map(int,np.linspace(0,len(tem),6)))[1:-1]]]
                        tem=np.array([np.mean(Retem[Xtem<=pointsTem[0]]),np.mean(Retem[(Xtem>pointsTem[0]) * (Xtem<=pointsTem[1])]),np.mean(Retem[(Xtem>pointsTem[1])*(Xtem<=pointsTem[2])]),\
                            np.mean(Retem[(Xtem>pointsTem[2])*(Xtem<=pointsTem[3])]),np.mean(Retem[Xtem>pointsTem[3]])])
                        tem=(tem/max(tem)).std()
                    else:
                        tem=0                    
                    rec1=np.row_stack(records[0])
                    rec2=np.row_stack(records[1])
                    profitP.append(rec2[:,2].tolist())
                    dispersity.append(tem)
                    if tem>0.2:
                        plt.xlabel( 'indicator column %d, correlative of train and test: %.10f, dispesity:%.10f'\
                               %(lp,pd.DataFrame(rec1[:,1])[0].corr(pd.DataFrame(rec2[:,1])[0]), tem ),color='r')
                    else:
                        plt.xlabel( 'indicator column %d, correlative of train and test: %.10f, dispesity:%.10f'\
                               %(lp,pd.DataFrame(rec1[:,1])[0].corr(pd.DataFrame(rec2[:,1])[0]), tem ),color='gray')                        
        #        plt.legend(loc='upper',bbox_to_anchor=(0.0,1.0),ncol=1,fancybox=True,shadow=True)
                plt.legend(loc='upper left')
                plt.grid(1)
                
        if figStart==Xcol:
            return flag,profitP
        else:
            dispersity=np.array(dispersity)
            return dispersity,profitP
        
    def kmeanSortFigure(self,Matrix,Re):
        cols=Matrix.shape[1]
        records=[] # hold two recordi
        for i in range(cols):
            figTitle='kmean sort according to Column: '+str(i)
            Xtem=Matrix[:,i]
            kmean=joblib.load(self.saveData+str(i)+'_kmean')                
            flag=kmean.predict(np.row_stack(Xtem))
            plt.figure(figsize=(15,8))
            xi=[]
            yi=[]
            recordi=[] # record number of total orders, IR,winratio,ratioWL,profitP
            for i2 in range(kmean.n_clusters):
                state=(flag==i2)
                ReT=Re[state]
                ReTcs=ReT.cumsum()
                LT=len(ReT)
                if LT<2:
                    continue
                maxDraw=0
                maxDrawi=0
                maxDrawValue=0
                i2High=0
                for i3 in range(LT):
                    if ReTcs[i3]>i2High:
                        i2High=ReTcs[i3]
                    drawT=i2High-ReTcs[i3]
                    if maxDraw<drawT:
                        maxDraw=drawT
                        maxDrawi=i3
                        maxDrawValue=ReTcs[i3]
                xi.append(maxDrawi)
                yi.append(maxDrawValue)  
                recordi.append([LT,np.mean(ReT)/np.std(ReT),ReTcs[-1]/LT*100])
                try:
                    plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
                         %(i2,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/-np.mean(ReT[ReT<0]),maxDraw*100,ReTcs[-1]/LT*100))  
                except:
                    plt.plot(range(LT),ReTcs,label='latent_state %d;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%s);maxDraw:%.2f%%;profitP:%.4f%%;'\
                         %(i2,LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),'error',maxDraw*100,ReTcs[-1]/LT*100))
            records.append(recordi)
            dispTem=np.sort(Xtem)
            pointsTem=dispTem[[list(map(int,np.linspace(0,len(dispTem),6)))[1:-1]]]
            dispTem=np.array([np.mean(Re[Xtem<=pointsTem[0]]),np.mean(Re[(Xtem>pointsTem[0]) * (Xtem<=pointsTem[1])]),np.mean(Re[(Xtem>pointsTem[1])*(Xtem<=pointsTem[2])]),\
                np.mean(Re[(Xtem>pointsTem[2])*(Xtem<=pointsTem[3])]),np.mean(Re[Xtem>pointsTem[3]])])
            dispTem=(dispTem/max(dispTem)).std()
            if dispTem>0.2:
                plt.xlabel( 'indicator column %d, dispesity:%.10f'  %(i,dispTem ),color='r')
            else:
                plt.xlabel( 'indicator column %d, dispesity:%.10f'  %(i,dispTem ),color='gray')           
            plt.plot(xi,yi,'r*')
            plt.title(figTitle,fontsize=16)
            plt.legend(loc='upper left')
            plt.grid(1)
       
    def kmeanTestCertainNot(self,Matrix,flagSelect):
        X=np.row_stack(Matrix)  
        Nind=[]
        flagNot=[]
        for i in range(len(flagSelect)):
            Nind.append(flagSelect[i][0])
            flagNot.append(flagSelect[i][1])            
        ReSelect=np.ones(len(X))
        for i2 in range(len(Nind)):    
            kmean=joblib.load(self.saveData+str(Nind[i2])+'_kmean')
            flagTem=kmean.predict(np.row_stack(X[:,Nind[i2]]))
            for i in range(len(flagNot[i2])):
                    ReSelect=ReSelect*(flagTem!=flagNot[i2][i])       
        return ReSelect
    
    def kmeanTestCertainOk(self,Matrix,flagSelect):
        X=np.row_stack(Matrix)  
        Nind=[]
        flagOk=[]
        for i in range(len(flagSelect)):
            Nind.append(flagSelect[i][0])
            flagOk.append(flagSelect[i][1])            
        ReSelect=np.zeros(len(X))
        for i2 in range(len(Nind)):    
            kmean=joblib.load(self.saveData+str(Nind[i2])+'_kmean')
            flagTem=kmean.predict(np.row_stack(X[:,Nind[i2]]))
            for i in range(len(flagOk[i2])):
                    ReSelect=ReSelect+(flagTem==flagOk[i2][i])    
        return ReSelect
        
    def averageSort(self,Matrix,Re):
        Lt=Matrix.shape[1]
        pointValues=[] # each one divides each column into equal 5 piece of data;
        for i in range(Lt):
            x=Matrix[:,i]
            xS=x.copy()
            xS.sort()
            tem=len(x)/5
            p1=xS[int(tem)]
            p2=xS[int(tem*2)]
            p3=xS[int(tem*3)]
            p4=xS[int(tem*4)]
            pointValues.append([p1,p2,p3,p4])
            r1=Re[x<p1]
            r2=Re[(x<p2)*(x>=p1)]
            r3=Re[(x<p3)*(x>=p2)]
            r4=Re[(x<p4)*(x>=p3)]
            r5=Re[(x>=p4)]
            plt.figure()
            re=[]
            title=[]
            if len(r1)>0:
                re.append(r1)
                title.append(str(i)+'--r1')
            if len(r2)>0:
                re.append(r2)
                title.append(str(i)+'--r2')
            if len(r3)>0:
                re.append(r3)
                title.append(str(i)+'--r3')
            if len(r4)>0:
                re.append(r4)
                title.append(str(i)+'--r4')
            if len(r5)>0:
                re.append(r5)
                title.append(str(i)+'--r5')
            self.ReFig(re,title)
        return pointValues
    
    def xgbTrain(self,x_train,y_train,x_test,y_test):
        x_train=x_train.copy()
        x_test=x_test.copy()
        y_train=y_train.copy()
        y_test=y_test.copy()        
        y_train[y_train>=0.001]=1
        y_train[y_train<=0.001]=0
        y_test[y_test>=0.001]=1
        y_test[y_test<0.001]=0
        
        data_train=xgb.DMatrix(data=x_train,label=y_train)
        data_test=xgb.DMatrix(data=x_test,label=y_test)
        watch_list={(data_test,'eval'),(data_train,'train')}
        param={'max_depth':3,'eta':0.03,'early_stopping_rounds':3,'silent':1,'objective':'multi:softmax','num_class':2}
        XGB=xgb.train(param,data_train,num_boost_round=5000,evals=watch_list) #modeify 20000
        joblib.dump(XGB,self.saveData+'_xgb')
    
    def xgbPredict(self,x_):
        conn = pymysql.connect('localhost','caofa','caofa',self.nameDB)
        cur=conn.cursor()
        cur.execute('select * from colXGB') # select name from sto
        colXGB=np.r_[cur.fetchall()]
        data_=xgb.DMatrix(data=x_[:,colXGB])
        cur.close()
        conn.close()
        XGB=joblib.load(self.saveData+'_xgb')
        return XGB.predict(data_)
        
    def gaussianNBtrain(self,x_,y_):
        y_train=y_.copy()
        y_train[y_train>=0.001]=1
        y_train[y_train<0.001]=0      
        gauNB=GaussianNB().fit(x_.tolist(),y_train.tolist())
        joblib.dump(gauNB,self.saveData+'_gauNB')
        
    def gaussianNBpredict(self,x_):
        gauNB=joblib.load(self.saveData+'_gauNB')
        conn = pymysql.connect('localhost','caofa','caofa',self.nameDB)
        cur=conn.cursor()
        cur.execute('select * from colXGB') # select name from sto
        colXGB=np.r_[cur.fetchall()]
        cur.close()
        conn.close()  
        return gauNB.predict(x_[:,colXGB])        
    
    def ReFig(self,Re,figTitle):
        for i in range(len(figTitle)):
            Rei=np.array(Re[i])
            figTitlei=figTitle[i]
            Recs=Rei.cumsum()
            LT=len(Rei)
            maxDraw=0
            maxDrawi=0
            maxDrawValue=0
            i2High=0
            for i2 in range(LT):
                if Recs[i2]>i2High:
                    i2High=Recs[i2]
                drawT=i2High-Recs[i2]
                if maxDraw<drawT:
                    maxDraw=drawT
                    maxDrawi=i2
                    maxDrawValue=Recs[i2]
            try:
                plt.plot(range(LT),Recs,label='%s ---- orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.4f%%;'\
                     %(figTitlei,LT,np.mean(Rei)/np.std(Rei),sum(Rei>0)/float(LT),np.mean(Rei[Rei>0])/-np.mean(Rei[Rei<0]),maxDraw*100,Recs[-1]/LT*100))  
            except Exception as tem:
                plt.plot(range(LT),Recs)
                print(tem)
            plt.plot(maxDrawi,maxDrawValue,'r*')
            plt.legend(loc='upper left',framealpha=0.3)
            plt.grid(1) 
        plt.title(' VS '.join(figTitle))

    def sortStatastic(self,sorts,Re,Title):
        sorts=np.array(sorts)
        sortsU=np.unique(sorts)
        plt.figure(figsize=(15,8))
        ax=plt.subplot(1,1,1)
        xi=[]
        yi=[]
        profitP=[]
        for i in range(len(sortsU)):
            state=(sorts==sortsU[i])
            ReT=Re[state]
            ReTcs=ReT.cumsum()
            LT=len(ReT)
            if LT<2:
                continue
            maxDraw=0
            maxDrawi=0
            maxDrawValue=0
            i2High=0
            for i2 in range(LT):
                if ReTcs[i2]>i2High:
                    i2High=ReTcs[i2]
                drawT=i2High-ReTcs[i2]
                if maxDraw<drawT:
                    maxDraw=drawT
                    maxDrawi=i2
                    maxDrawValue=ReTcs[i2]
            xi.append(maxDrawi)
            yi.append(maxDrawValue)  
            profitP.append(ReTcs[-1]/LT*100)
            try:
                ax.plot(range(LT),ReTcs,label='latent_state %s;orders:%d;IR:%.4f;winratio(ratioWL):%.2f%%(%.2f);maxDraw:%.2f%%;profitP:%.2f%%;'\
                        %(sortsU[i],LT,np.mean(ReT)/np.std(ReT),sum(ReT>0)/float(LT),np.mean(ReT[ReT>0])/(-np.mean(ReT[ReT<0])),maxDraw*100,ReTcs[-1]/LT*100))  
            except:
                ax.plot([0,i*100],[0,-1],label='latent_state %s: too less points or some other error!' %sortsU[i])
#                ax.text(i*100,-0.8,'test',fontsize=20,horizontalalignment='center',verticalalignment='center')
                    
        ax.plot(xi,yi,'r*')
        handles, labels = ax.get_legend_handles_labels()
        tem=np.argsort(profitP)[::-1]
        ax.legend(np.array(handles)[tem],np.array(labels)[tem],loc='upper left', bbox_to_anchor=(1.0, 1.0), ncol=1, fancybox=True, shadow=True)
        plt.title(Title)
        plt.grid(1)
    

    



    







    




    



    







    



