import tushare as ts
import matplotlib.pyplot as plt
import numpy as np

stock='000001'
Id=False
data=ts.get_k_data(stock,ktype='D',autype='qfq',index=Id,start='2018-01-12')
closes=data['close'].values
opens=data['open'].values
highs=data['high'].values
lows=data['low'].values
dates=data['date'].values

plt.figure(figsize=(10,6))
ax=plt.subplot()
ax.plot(highs,'r',label='High')
ax.plot(lows,'g',label='Low')
ax.plot(closes,'k',label='Close')
L=len(closes)
xind=range(0,L,L//12)
ax.set_xticks(xind)
ax.set_xticklabels(dates[xind],rotation=60)
if Id:
    plt.title('index'+stock)
else:
    plt.title('stock'+stock)
plt.grid()
plt.legend()
plt.show()


























