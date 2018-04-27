import numpy as np
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import pandas as pd
#from matplotlib.pylab import date2num
import matplotlib.patches as patches
import pickle,pdb,pymysql,datetime,time

dataDownLoad=0
TS=0 #use tushare or not
if dataDownLoad:
    if TS:
        tmp=ts.get_stock_basics()
        stocks=tmp.index.tolist()
        opens=[]
        highs=[]
        closes=[]
        lows=[]
        vols=[]
        dataAll=[]
        Stock=[]
        L=len(stocks)
        for i in range(L):
            print('download {}%'.format(round(i*100/L,2)))
            tmp=ts.get_k_data(code = stocks[i],autype='qfq',ktype='W',start = '2000-01-01',end='2018-04-25')
            if len(tmp):
                dataAll.append(tmp[['date','open','high','low','close','volume']].reset_index(drop=True))
                Stock.append(stocks[i])
    else:    
        conn = pymysql.connect(host ='localhost',user = 'caofa',passwd = 'caofa',charset='utf8')
        cur=conn.cursor()
        conn.select_db('pythonStocks') 
        if dataDownLoad:
            Lstocks=cur.execute('select number from stocks')
            Number=np.insert(np.cumsum(cur.fetchall()),0,0)
            cur.execute('select name from stocks')
            stocks=cur.fetchall()
            cur.execute('select * from dataDay')
            dataAll=np.c_[cur.fetchall()]
            Stock=[]
            dataWeek=[]
            for i in range(1,Lstocks):
                print('download {}%'.format(round(i*100/Lstocks,2)))
                datai=dataAll[:,Number[i-1]:Number[i]]
                date=datai[0]
                opens=datai[1]
                closes=datai[2]
                highs=datai[3]
                lows=datai[4]
                vols=datai[5]
                dateNum=[ time.mktime((i-datetime.timedelta(i.weekday())).timetuple()) for i in date]
                dateIndex=np.zeros(len(dateNum))
                dateIndex[0]=1
                for i2 in range(1,len(dateIndex)):
                    if dateNum[i2]>dateNum[i2-1]:
                        dateIndex[i2]=1
                wkTmp=np.where(dateIndex==1)[0]
                wkTmp=np.insert(wkTmp,len(wkTmp),len(dateNum))
                weekTmp=[]
                for i2 in range(len(wkTmp)-1):          
                    weekTmp.append([date[wkTmp[i2]],opens[wkTmp[i2]],closes[wkTmp[i2+1]-1],\
                                    max(highs[wkTmp[i2]:wkTmp[i2+1]]),min(lows[wkTmp[i2]:wkTmp[i2+1]]),sum(vols[wkTmp[i2]:wkTmp[i2+1]])])
                weekTmp.pop()
                if len(weekTmp)>5:
                    Stock.append(stocks[i][0])
                    tmp=np.c_[weekTmp]
                    dataWeek.append(pd.DataFrame({'date':tmp[:,0],'open':tmp[:,1],'close':tmp[:,2],'high':tmp[:,3],\
                                     'low':tmp[:,4],'volume':tmp[:,5]}))
        cur.close()
        conn.close() 
        
    dataWeek={'stocks':Stock,'dataAll':dataWeek}
    tmp=open('E:\\MySQLData\\dataWeek.pkl','wb')
    pickle.dump(dataWeek,tmp)
    tmp.close()   
else:
    tmp=open('E:\\MySQLData\\dataWeek.pkl','rb')
    dataWeek=pickle.load(tmp)
    tmp.close()
    stocks=dataWeek['stocks']
    dataAll=dataWeek['dataAll']
    L=len(stocks)
    fig=plt.figure(figsize=(12,8))
    tmp=ts.get_stock_basics()
    dicOut=tmp.outstanding
    i2Start=30
    for i in range(L):
        Ci='Complete {}%'.format(round(i*100/L,2))
        print(Ci)
    #    if dicOut[stocks[i]]>20:
    #        continue
        data=dataAll[i]
        L2=len(data)
        vols=data['volume'].values
        opens=data['open'].values
        closes=data['close'].values
        highs=data['high'].values
        lows=data['low'].values
        dates=data['date'].values
        figS=1
        for i2 in range(i2Start,L2-1):
            maxP=max(highs[i2-i2Start:i2])
            minP=min(lows[i2-i2Start:i2])
            tmpP=(maxP-minP)*0.45
            if closes[i2]<tmpP and sum(vols[i2-4:i2-1]-vols[i2-3:i2]>0)==3 and sum(closes[i2-4:i2-1]-closes[i2-3:i2]>0)==3 and \
            sum(opens[i2-3:i2]-closes[i2-3:i2]>0)==3 and \
            (closes[i2]>closes[i2-1] or vols[i2]>vols[i2-1] or opens[i2]<closes[i2]):                            
                if i2+10<L2:
                    endP=i2+10
                else:
                    endP=L2
                if i2-i2Start>0:
                    startP=i2-i2Start
                else:
                    startP=0
                date=dates[startP:endP]
                candleData=np.column_stack([list(range(len(date))),opens[startP:endP],highs[startP:endP],lows[startP:endP],closes[startP:endP]])
                ax=fig.add_axes([0.1,0.3,0.8,0.6])
                mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
                tmp=i2-4-startP
                ax.plot([tmp-0.5,tmp-0.5,tmp+3.5,tmp+3.5],[0,highs[tmp],highs[tmp],0],color='r')
                tmpL=len(date)
                xindex=list(range(0,tmpL,tmpL//5))
                ax.set_xticks(xindex)
                ax.grid()
                nameF=stocks[i]+'-'+str(figS)
                plt.title(nameF)
                figS+=1
                ax1=fig.add_axes([0.1,0.1,0.8,0.2])
                vol=vols[startP:endP]
                ax1.bar(range(len(date)),vol)
                ax1.plot([tmp-0.5,tmp-0.5,tmp+3.5,tmp+3.5],[0,vols[tmp],vols[tmp],0],color='r')
                ax1.set_xticks(xindex)
                ax1.set_xticklabels(date[xindex],rotation=45)
                ax1.grid()
                plt.savefig('E:\\缩量连跌图\\'+nameF+'.png')
                plt.clf()



























