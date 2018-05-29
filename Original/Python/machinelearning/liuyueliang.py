import os,shutil,pdb
import numpy as np
import pandas as pd
import matplotlib.finance as mpf
import matplotlib.pyplot as plt


data_dir='e:/future_data/'
data_files=os.listdir(data_dir)
#data_files=[data_files[4]]
for i0 in data_files:
    print(i0)
    fileTmp=data_dir+i0
    futureName=i0[:-5]
    fileFig='e:/stockSelect/'+futureName+'/'
    if futureName=='CUL':
        minTick=10
    elif futureName=='CFL' or futureName=='RUL' or futureName=='ZNL':
        minTick=5
    elif futureName=='ML' or futureName=='SRL' or futureName=='RBL':
        minTick=1
    elif futureName=='JL':
        minTick=0.5

    Fig=0
    try:
        shutil.rmtree(fileFig)
    except:
        pass
    os.mkdir(fileFig)
    
    def drawFig(Fig):
        fig=plt.figure(figsize=(10,6))
        ax=fig.add_axes([0.1,0.3,0.8,0.6])
        for i3 in range(len(recordBar)-1):
            if hold*(recordP[i3]-recordP[-1])>0:
                colorTmp='gray'
            else:
                colorTmp='gold'
            ax.plot([recordBar[i3]-allStarts[i],recordBar[-1]-allStarts[i]],[recordP[i3],recordP[-1]],color=colorTmp,linewidth=3.0)
        ax.plot(data.ma5[allStarts[i]:endTmp].values,linestyle='--')
        ax.plot(data.ma10[allStarts[i]:endTmp].values,linestyle='--')
        ax.plot(data.ma20[allStarts[i]:endTmp].values,linestyle='--')
        candleData=np.c_[range(endTmp-allStarts[i]),data[['open','high','low','close']].loc[allStarts[i]:endTmp-1]]
        mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
        ax.grid()
        if hold>0:
            plt.title('Profit: '+str(((stopP-minTick)/openP-1.0)/3))
        else:
            plt.title('Profit: '+str((1.0-(stopP+minTick)/openP)/3))
        ax1=fig.add_axes([0.1,0.1,0.8,0.2])
        ax1.bar(range(endTmp-allStarts[i]),data.vol[allStarts[i]:endTmp])
        ax1.plot(data.volMa1[allStarts[i]:endTmp].values)
        ax1.plot(data.volMa2[allStarts[i]:endTmp].values)
        ax1.grid() 
        plt.savefig(fileFig+str(Fig)+'.png')
        plt.clf()
    
    kind=pd.read_csv(fileTmp,sep='\t',encoding='gb2312',nrows=0).columns[0]
    data=pd.read_csv(fileTmp,sep='\t',encoding='gb2312',skiprows=2)
    data.columns=['time','open','high','low','close','vol','ma5','ma10',\
                  'ma20','ma60','volV','volMa1','volMa2','macdDIF','MACD.DEA','macd2','unName']
    data=data.drop([data.shape[0]-1])
    allStarts=[]
    L=data.shape[0]
    for i in range(L):
        if data.time[i][-5:]=='21:01':
            allStarts.append(i)
    allStarts=np.array(allStarts)
    Ldays=len(allStarts)
    profit=[]
    holds=[]
    for i in range(Ldays-21):
        if allStarts[i]<80:
            continue
        try:
            endTmp=allStarts[i+1]
        except:
            endTmp=L
        hold=0
        openP=0
        recordP=[]
        recordBar=[]
        stopP=0
        for i2 in range(allStarts[i]+2,endTmp):
            dataNow=data.loc[i2]
            dataPast=data.loc[i2-1]
            openLong=dataNow.ma5>dataNow.ma10>dataNow.ma20 and \
                not (dataPast.ma5>dataPast.ma10>dataPast.ma20) and \
                float(dataNow.ma5)>float(dataPast.ma5) and float(dataNow.ma10)>float(dataPast.ma10) and \
                float(dataNow.ma20)>float(dataPast.ma20) and \
                dataNow.vol>2.1*float(dataNow.volMa2) and sum(data.loc[i2-10:i2].high>data.loc[i2-10:i2].low)>10 and \
                data.close[allStarts[i-20:i]-1].mean()<data.close[allStarts[i-10:i]-1].mean()<data.close[allStarts[i-5:i]-1].mean()
            openShort=dataNow.ma5<dataNow.ma10<dataNow.ma20 and \
                not (dataPast.ma5<dataPast.ma10<dataPast.ma20) and \
                float(dataNow.ma5)<float(dataPast.ma5) and float(dataNow.ma10)<float(dataPast.ma10) and \
                float(dataNow.ma20)<float(dataPast.ma20) and \
                dataNow.vol>2.1*float(dataNow.volMa2) and sum(data.loc[i2-10:i2].high>data.loc[i2-10:i2].low)>10 and \
                data.close[allStarts[i-20:i]-1].mean()>data.close[allStarts[i-10:i]-1].mean()>data.close[allStarts[i-5:i]-1].mean()
            if hold==0:
                if openLong:
                    hold=1
                    openP=dataNow.close
                    recordBar.append(i2)
                    recordP.append(openP)
                    stopP=dataNow.low-2*minTick
                    R=dataNow.high-dataNow.low
                if openShort:
                    hold=-1
                    openP=dataNow.close
                    recordBar.append(i2)
                    recordP.append(openP)
                    stopP=dataNow.high+2*minTick
                    R=dataNow.high-dataNow.low
                    
            else:
                if hold>0:
                    if dataNow.low<=stopP:
                        profit.append(hold*((stopP-minTick)/openP-1.0))
                        holds.append(hold)
                        recordP.append(stopP)
                        recordBar.append(i2)
                        drawFig(Fig)
                        Fig+=1
                        recordP=[]
                        recordBar=[]
                        hold=0
                    elif openShort:
                        profit.append(hold*((dataNow.close-minTick)/openP-1.0))
                        holds.append(hold)
                        recordP.append(stopP)
                        recordBar.append(i2)
                        drawFig(Fig)
                        Fig+=1
                        recordP=[]
                        recordBar=[]
                        
                        hold=-1 # open new short
                        openP=dataNow.close
                        recordBar.append(i2)
                        recordP.append(openP)
                        stopP=dataNow.high+2*minTick
                        R=dataNow.high-dataNow.low
                    elif hold==1:
                        if dataNow.high-openP>R:
                            stopP=openP
                        if dataNow.high-openP>2*R:
                            hold=hold+1
                            recordP.append(dataNow.close)
                            recordBar.append(i2)
                            openP=(openP+dataNow.close)/2
                            stopP=openP
                    elif hold==2:
                        if dataNow.high-recordP[0]>4*R:
                            hold=hold+1
                            stopP=recordP[1]
                            openP=openP*2/3+dataNow.close/3
                            recordP.append(dataNow.close)
                            recordBar.append(i2)
                else:
                    if dataNow.high>=stopP:
                        profit.append(hold*(1.0-(stopP+minTick)/openP))
                        holds.append(hold)
                        recordP.append(stopP)
                        recordBar.append(i2)
                        drawFig(Fig)
                        Fig+=1
                        recordP=[]
                        recordBar=[]
                        hold=0
                    elif openLong:
                        profit.append(hold*(1.0-(dataNow.close+minTick)/openP))
                        holds.append(hold)
                        recordP.append(stopP)
                        recordBar.append(i2)
                        drawFig(Fig)
                        Fig+=1
                        recordP=[]
                        recordBar=[]
                        
                        hold=1 #open new long
                        openP=dataNow.close
                        recordBar.append(i2)
                        recordP.append(openP)
                        stopP=dataNow.low-2*minTick
                        R=dataNow.high-dataNow.low
                    elif hold==-1:
                        if openP-dataNow.low>R:
                            stopP=openP
                        if openP-dataNow.low>2*R:
                            hold=hold-1
                            recordP.append(dataNow.close)
                            recordBar.append(i2)
                            openP=(openP+dataNow.close)/2
                            stopP=openP
                    elif hold==-2:
                        if recordP[0]-dataNow.low>4*R:
                            hold=hold-1
                            stopP=recordP[1]
                            openP=openP*2/3+dataNow.close/3
                            recordP.append(dataNow.close)
                            recordBar.append(i2)               
            if i2==endTmp-1 :
                if  hold >0:
                    profit.append(hold*((dataNow.close-minTick)/openP-1.0))
                    stopP=dataNow.close
                    holds.append(hold)
                    recordP.append(dataNow.close)
                    recordBar.append(i2)
                    drawFig(Fig)
                    Fig+=1
                    hold=0
                elif hold<0:
                    profit.append(hold*(1.0-(dataNow.close+minTick)/openP))
                    stopP=dataNow.close
                    holds.append(hold)
                    recordP.append(dataNow.close)
                    recordBar.append(i2)
                    drawFig(Fig)
                    Fig+=1
                    hold=0
    
    plt.figure(figsize=(10,6))
    profit=np.array(profit)/3
    maxDown=0-profit[0]
    for i in range(1,len(profit)):
        tmp=max(profit[:i])-profit[i]
        if tmp>maxDown:
            maxDown=tmp
    winRatio=sum(profit>0)/sum(profit<0)
    plt.plot(profit.cumsum())
    plt.title('maxDown:'+str(round(maxDown*100,2))+'%;'+'win/loss: '+str(round(winRatio,2)))
    plt.grid()
    plt.savefig(fileFig+'result.png')
    plt.clf()
#            if hold<0 and data.loc[i2].high>=stopP:
#                hold=0
#                profit.append(1.0-stopP/openP)
            
                
        
        
        
        
























