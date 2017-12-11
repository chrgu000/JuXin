from pylab import *  
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import tushare as ts
import numpy as np
import datetime

#data=ts.get_k_data('600000',ktype='D',autype='qfq',start='2017-10-12',end='2017-12-11')
#candleData=data[['open','high','low','close']]
#candleData=np.column_stack([list(range(candleData.shape[0])),candleData])
#
#plt.figure(figsize=(12,8))
#ax=plt.subplot()
#mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
#ax.grid()




data=ts.get_k_data('600000',ktype='D',autype='qfq',start='2017-10-12',end='2017-12-11')
prices=data[['open','high','low','close']]
dates=data['date']
dates=[datetime.datetime.strptime(x, '%Y-%m-%d').date() for x in dates]
candleData=np.column_stack([dates,prices])
plt.figure(figsize=(12,8))
ax=plt.subplot()
mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
ax.grid()

































































