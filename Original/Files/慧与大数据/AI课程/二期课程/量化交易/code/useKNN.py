from sklearn.neighbors import KNeighborsClassifier
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import pdb

objectTrade='000001'
def Get_XY(startDate,endDate): #获取交易数据及其收益
    data=ts.get_k_data(objectTrade,start=startDate,end=endDate,index=True)
    closes=np.array(data['close'])
    vols=np.array(data['volume'])
    opens=np.array(data['open'])
    highs=np.array(data['high'])
    lows=np.array(data['low'])

    ReX=[];ReY=[]
    for i in range(1,len(closes)-1):
        tmp=closes[i-1]
        ReX.append([opens[i]/tmp,closes[i]/tmp,highs[i]/tmp,lows[i]/tmp])
        ReY.append(closes[i+1]/closes[i]-1)

    X=np.array(ReX)
    ReY=np.array(ReY)
    return X,ReY

'''
    tmp=closes[:-2]
    openNew=opens[1:-1]/tmp
    closeNew=closes[1:-1]/tmp
    highNew=highs[1:-1]/tmp
    lowNew=lows[1:-1]/tmp   
    ReY=closes[2:]/closes[1:-1]-1
    X=np.column_stack([openNew,closeNew,highNew,lowNew])
    return X,ReY'''

def Fig(labels,labelsU,ReY): #针对不同分类，作图显示其走势差异
    Rlist=[];titles=[];
    for i in range(len(labelsU)):
        tem=labels==labelsU[i]
        ReTem=ReY[tem]
        Rlist.append(ReTem)
        titles.append('Label:'+str(labelsU[i]))
    plt.figure(figsize=(15,8))
    for i in range(len(titles)):
        plt.plot(Rlist[i].cumsum(),label=titles[i])
    plt.title('SZIndex:'+objectTrade+'; year:'+str(years))
    plt.legend()
    plt.grid()
    plt.show()

years=2014
X,ReY=Get_XY(str(years-3)+'-01-01',str(years)+'-01-01')

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(X,ReY>0)

X,ReY=Get_XY(str(years)+'-01-01',str(years)+'-12-01')
labels=knn.predict(X)
labelsU=np.unique(labels)
Fig(labels,labelsU,ReY)









