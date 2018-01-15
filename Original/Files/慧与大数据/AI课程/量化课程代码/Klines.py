import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
import numpy as np
import datetime

data=ts.get_k_data('600519',ktype='D',autype='qfq',start='2017-09-17',end='')
prices=data[['open','high','low','close']]
dates=data['date']
#dates=[date2num(datetime.datetime.strptime(x,'%Y-%m-%d')) for x in dates ]
candleData=np.column_stack([list(range(len(dates))),prices])
fig=plt.figure(figsize=(12,8))
ax=fig.add_axes([0.1,0.3,0.8,0.6])
mpf.candlestick_ohlc(ax,candleData,width=0.5,colorup='r',colordown='g')
dates=dates.values
L=len(dates)
closes=data['close']
ma5=[];ma10=[]
for i in range(4,L):
    ma5.append(closes[i-4:i+1].mean())
    if i>=9:
        ma10.append(closes[i-9:i+1].mean())
ax.plot(range(4,L),ma5)
ax.plot(range(9,L),ma10)
xindex=list(range(0,L,L//12))
ax.set_xticks(xindex)
ax.grid()
ax1=fig.add_axes([0.1,0.1,0.8,0.2])
ax1.bar(range(L),data['volume'])
ax1.set_xticks(xindex)
ax1.set_xticklabels(dates[xindex],rotation=45)
ax1.grid()
plt.show()



