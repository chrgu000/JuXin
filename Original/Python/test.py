# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 14:49:18 2017

@author: Administrator
"""
'''
from mlab.releases import latest_release as matlab
#matlab.plot([2,3,4,5,8],'-o')
matlab.path(matlab.path(),r'D:\Trading')
matlab.path(matlab.path(),r'E:\Trading')
matlab.pyWDM('600000.sh',1)
'''

'''
import scipy.io as scio
dataFile='C:\Users\Administrator\Desktop\Beta.mat'

data=scio.loadmat(dataFile)
xx=data['betaValue']
print xx
'''
'''
import tushare as ts
import scipy.io as scio

data=ts.get_hs300s()
hs300code=data['code'].tolist()
hs300weight=data['weight'].tolist()
scio.savemat('d:\Trading\hs300.mat',{'hs300code':hs300code,'hs300weight':hs300weight})
'''
'''
def test(indata):
    print "hello"
    for k in range(0,len(indata.Fields)):
        if(indata.Fields[k] == "RT_LAST"):
            lastvalue = str(indata.Data[k][0])
            print (lastvalue)
          
from WindPy import *            
w.start()
live_data=w.wsq("000001.SH,000001.SZ","rt_last",func=test.test)
'''

#import time
#import datetime
##while True:
##    print 'dsfs'
##    time.sleep(2)  
#
#'''
#from WindPy import *            
#w.start()
#data=w.wsd("000001.SH","high")
#print data
#'''
#
#x1 = datetime.datetime.strptime('2017-03-01', "%Y-%m-%d").date()
#x2=datetime.date.today()
#x3=(x2-x1).days
#
#print x3
#def features(sequence, i):
#    yield "word=" + sequence[i].lower()
#    if sequence[i].isupper():
#        yield "Uppercase"
#
#from seqlearn.datasets import load_conll
#
##x_t,y_t,length=load_conll('C:\Users\Administrator\Desktop\test.txt',features)


# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 08:59:37 2017

@author: caofa
"""
from WindPy import *
import numpy as np
import pickle,datetime,joblib


tradeFlag=raw_input('Please confirm trading or not [y/n]?')
tradeFlag=tradeFlag.lower()=='y'    
w.start()
Tem=w.tlogon('0000', '0', 'W115294100301', '*********', 'SHSZ')
logId=Tem.Data[0][0]
today=datetime.date.today()
try:
    fileTem=open('test','rb')
    dataTem=pickle.load(fileTem)
    fileTem.close()
    Date=dataTem['Date']
    Open=dataTem['Open']
    Close=dataTem['Close']
    High=dataTem['High']
    Low=dataTem['Low']
    Vol=dataTem['Vol']
    stocks=dataTem['stocks']
    lastTradeDay=dataTem['lastTradeDay']
    assets=dataTem['assets']
    holdDays=dataTem['holdDays']   
    dateStart=dataTem['dateStart']
    dataTem=w.tquery('Position', 'LogonId='+str(logId))
    holdStocks=dataTem.Data[0]
    holdShares=dataTem.Data[3]
    
except:
    dataTem=w.wset('SectorConstituent')
    stocks=dataTem.Data[1]
    yesterday=today-datetime.timedelta(days=1)
    lastTradeDay=[yesterday]
    assets=[w.tquery('Capital', 'LogonId='+str(logId)).Data[5]]
    holdDays={}    
    dateStart={}
    while 1:
        dataTem=w.wsd(stocks,'open','ED-20TD',yesterday,'Fill=Previous','PriceAdj=F')
        Date=dataTem.Times
        Open=dataTem.Data
        Close=w.wsd(stocks,'close','ED-20TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        High=w.wsd(stocks,'high','ED-20TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        Low=w.wsd(stocks,'low','ED-20TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        Vol=w.wsd(stocks,'volume','ED-20TD',yesterday,'Fill=Previous','PriceAdj=F').Data
        if np.all([len(Open)-1,len(Close)-1,len(High)-1,len(Low)-1,len(Vol)-1]):
            break

#Date.append(today)
#Open.append(w.wsq(stocks,'rt_open').Data[0])
#Close.append(w.wsq(stocks,'rt_latest').Data[0])
#High.append(w.wsq(stocks,'rt_high').Data[0])
#Low.append(w.wsq(stocks,'rt_low').Data[0])
#Vol.append(w.wsq(stocks,'rt_vol').Data[0])

#dataPKL={'Date':Date,'Open':Open,'Close':Close,'High':High,'Low':Low,'Vol':Vol}
#fileTem=open('test','wb')
#pickle.dump(dataPKL,fileTem)
#fileTem.close()

Lstocks=len(stocks)
stocksi=[] # name of stocks;
handsi=[]  # hands of trading this time;
modeli=[]  # model belonged to;
holdi=[]   # days to hold;
moneyi=[]  # money to trade;
profiti=[] # expected profit of this trading;
indicators=[] 
for i in range(Lstocks):
    openi=Open[i]
    closei=Close[i]
    highi=High[i]
    lowi=Low[i]
    
    Lnan=sum(np.isnan(openi))
    if Lnan>10:
        continue
    else:
        openi=openi[Lnan+1:]
        closei=closei[Lnan+1:]
        lowi=lowi[Lnan+1:]
        highi=highi[Lnan+1:]
    if closei[-1]/closei[-2]>=1.095:
        continue
    
    # model 1: spring, model number 1
    hmmSpring=joblib.load('D:\Trading\Python\machinelearning\HMMTest')
    if closei[-2]<lowi[-2]+(highi[-2]-lowi[-2])*0.25 and highi[-1]>lowi[-1]*1.000001 and 0.025<=closei[-1]/closei[-2]-1<0.055 and lowi[-1]/lowi[-2]-1>=0.01: 
        flagi=hmmSpring.predict([ np.std([closei[-1],openi[-1],lowi[-1],highi[-1]])/np.std([closei[-2],openi[-2],lowi[-2],highi[-2]])-1,\
                                 np.mean(closei[-4:])/np.mean(closei[-11:])-1,highi[-1]/highi[-2]-1,closei[-1]/lowi[-2]-1,closei[-1]/highi[-2]-1])
        if flagi==0:
            profiti.append(1.34)
        elif flagi==1:
            profiti.append(3.41)
        elif flagi==3:
            profiti.append(1.44)
        else:
            continue       
        print i
        stocksi.append(stocks[i])
        handsi.append(np.ceil(100/closei[-1])*100)
        modeli.append(1)   # model number:1;
        holdi.append(2)    # hold 2 days;
        moneyi.append(handsi[-1]*closei[-1])
    
indTem=np.argsort(-np.array(profiti))
profiti=np.array(profiti)[indTem]
stocksi=np.array(stocksi)[indTem]
handsi=np.array(handsi)[indTem]
modeli=np.array(modeli)[indTem]
holdi=np.array(holdi)[indTem]
moneyi=np.array(moneyi)[indTem]
dataTem=w.tquery('Capital', 'LogonId='+str(logId))
availableFun=dataTem.Data[1]
assetNow=dataTem.Data[5]
moneyCS=np.cumsum(moneyi)
Tem=sum(moneyCS>availableFun)
if Tem>0:
    profiti=profiti[:-Tem]
    stocksi=stocksi[:-Tem]
    handsi=handsi[:-Tem]
    modeli=modeli[:-Tem]
    holdi=holdi[:-Tem]
    moneyi=moneyi[:-Tem]

Ltrade=len(profiti)
for i in range(Ltrade):
    print 'Buy %s: %d shares;use capital:%.f Yuan;profitPerOrder:%.2f,ModelNumber:%d;' %(stocks[i],handsi[i],moneyi[i],profiti[i],moneyi[i]),
    if tradeFlag:
        w.torder(stocks[i], 'Buy', '0', handsi[i], 'OrderType=B5TC;'+'LogonID='+str(logId))
        print 'send trade command!'
    else:
        print 'not really trade!'
w.tlogout(str(logId))




        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
































