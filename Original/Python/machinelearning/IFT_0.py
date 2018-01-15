import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tushare as ts

try:
    x=pd.read_csv('IFT_0.csv',index_col='datetime')
except:
    #x=ts.get_k_data('000300', ktype='5',index=True, start='2016-01-01', end='2018-01-11')
    cons = ts.get_apis()
    x=ts.bar('000300',conn=cons,freq='5min',asset='INDEX',start_date='2016-01-01',end_date='2018-01-11')
    x.to_csv('IFT_0.csv')

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
plt.legend()
plt.show()
