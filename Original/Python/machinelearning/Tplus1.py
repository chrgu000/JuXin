# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 09:14:08 2017

@author: Administrator
"""

from pylab import *
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import tushare as ts
import numpy as np
  
mpl.rcParams['font.sans-serif']=['SimHei']  
mpl.rcParams['axes.unicode_minus']=False  
  
stock='000004'  
data=ts.get_k_data(stock,ktype='D',autype='qfq',index=False,start='2010-09-12',end='2017-12-11')  
closes=np.array(data['close'])  
opens=np.array(data['open'])  

diff=1-opens[2:]/closes[1:-1]#-0.0013  
#tmp=[ True if  abs(closes[i]/closes[i-1]-1)>=0.094 else False for i in range(1,len(closes)-1)]  
#diff[tmp]=0  
#tmp=[ True if  closes[i]/closes[i-1]-1>=0.0 else False for i in range(1,len(closes)-1)]  
#diff[tmp]=0  
tem=(closes[1:-1]/closes[:-2]>=1.0) + (1-closes[1:-1]/closes[:-2]>=0.094)
diff[tem]=0.0

#diff=[]  
#for i in range(2,len(closes)):  
#    if closes[i-1]<closes[i-2] and 1-closes[i-1]/closes[i-2]<0.094 :
#        diff.append(1-opens[i]/closes[i-1]) 
#    else:
#        diff.append(0.0)
#diff=np.array(diff)  
  
plt.figure(figsize=(10,6))  
ax=plt.subplot()  
ax.plot(diff.cumsum(),label='价差套利')  
diff1=closes[1:]/closes[:-1]-1  
ax.plot(diff1.cumsum(),label='正常走势')  
dates=data['date']  
xindex=list(map(int,np.linspace(0,len(dates)-1,6)))  
ax.set_xticks(xindex)  
ax.set_xticklabels(dates[dates.index[xindex]],rotation=30)  
plt.legend(prop={'size':10})  
plt.title(stock)  
plt.grid()  