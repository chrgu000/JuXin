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
import joblib, warnings,pymysql,datetime,pdb

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
            for i in range(Lstocks):
#                print('%s:%d' %(stocks[i][0],i+1),end=' ',flush=True) #print(i, sep=' ', end=' ', flush=True)
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
                for i2 in range(15,Lt-45):
                    if func(opens[i2-15:i2+1],highs[i2-15:i2+1],lows[i2-15:i2+1],closes[i2-15:i2+1]):
                        if 1:#closes[i2+1]>=closes[i2]:
                            Re.append(closes[i2+45]/opens[i2+1]-1.003)
                            if fig>0:
                                figx=[5,49]
                                figy=[opens[i2+1],closes[i2+45]]
#                        else:#elif closes[i2+2]<=closes[i2+1]:
#                            Re.append(opens[i2+2]/opens[i2+1]-1.003)
#                            if fig>0:
#                                figx=[-5,-4]
#                                figy=[opens[i2+1],opens[i2+2]]
                        if fig>0:
                            fig=fig-1
                            plt.figure()
                            candleData=[]
                            for i3 in range(i2-4,i2+45):
                                tem=(date2num(dates[i3]),opens[i3],highs[i3],lows[i3],closes[i3])
                                candleData.append(tem)
                            ax=plt.subplot()
                            ax.xaxis_date()
                            plt.xticks(rotation=45)
                            plt.yticks()
                            plt.title(stocks[i][0]+str(round(Re[-1],3)))
                            plt.xlabel('Date')
                            plt.ylabel('Price')
                            mpf.candlestick_ohlc(ax,candleData,width=0.8,colorup='r',colordown='g')
                            plt.plot([candleData[figx[0]][0],candleData[figx[1]][0]],figy,color='b',linewidth='2')
                            plt.grid()      
            
            plt.figure(figsize=(15,8))
            plt.plot(np.cumsum(Re))
            plt.title(str(np.mean(Re)))
            
        
    
   



    







    




    



    







    



