import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tushare as ts

x=pd.read_csv('test.csv',index_col='datetime')
lows=x['low'].values
highs=x['high'].values
closes=x['close'].values

Ndays=len(closes)//48
Re=[]
holds=15
for i in range(Ndays):
    lowT=lows[i*48:(i+1)*48]
    highT=highs[i*48:(i+1)*48]
    closeT=closes[i*48:(i+1)*48]
    startBar=holds//5
    upline=max(highT[:startBar])
    downline=min(lowT[:startBar])
    for i2 in range(startBar,len(lowT)):
        if lowT[i2]<downline:
            Re.append(1-closeT[-1]/downline)
            break
        elif highT[i2]>upline:
            Re.append(closeT[-1]/upline-1)
            break
        if i2>len(lowT)-2:
            Re.append(0.0)

Re=np.array(Re)
plt.plot(Re.cumsum(),label='Strategy')
reRaw=closes[47::48]/closes[::48]-1
plt.plot(reRaw.cumsum(),label='HS300')
plt.plot([0,500],[0,0],c='r')
plt.grid()
plt.legend()
plt.show()









