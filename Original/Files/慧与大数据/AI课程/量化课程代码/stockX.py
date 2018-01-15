import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import numpy as np
import pdb

stock='000001'
data=ts.get_k_data(stock,ktype='D',autype='qfq',start='2010-01-01',end='2018-01-01')
closes=np.array(data['close'])
opens=np.array(data['open'])

#对以下for循环的矩阵运算
#diff=1-opens[2:]/closes[1:-1]
#tem=(closes[1:-1]/closes[:-2]>=1.094 )|(1-closes[1:-1]/closes[:-2]>=0.094)
#diff[tem]=0.0
diff=[]
for i in range(2,len(closes)):
    if closes[i-1]/closes[i-2]<1.094 and 1-closes[i-1]/closes[i-2]<0.094: #and closes[i-1]/closes[i-2]>1:
        diff.append(1-opens[i]/closes[i-1])
    #else:
        #diff.append(0.0)
#print(np.mean(diff))
diff=np.array(diff)

plt.figure(figsize=(10,6))
ax=plt.subplot()
ax.plot(diff.cumsum(),label='Strategy')
diff1=closes[1:]/closes[0]-1
ax.plot(diff1,label='Common')
dates=data['date'].values
L=len(dates)
xindex=list(range(0,L,L//12))
ax.set_xticks(xindex)
ax.set_xticklabels(dates[xindex],rotation=30)
plt.title(stock)
plt.grid()
plt.legend()
plt.show()









