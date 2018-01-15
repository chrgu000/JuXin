import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.decomposition import PCA

objectTrade='000001'
def GetXY(startDate,endDate): #获取交易数据及其收益；
    data=ts.get_k_data(objectTrade,start=startDate,end=endDate,index=True)
    closes=np.array(data['close'])
    vols=np.array(data['volume'])
    opens=np.array(data['open'])
    highs=np.array(data['high'])
    lows=np.array(data['low'])

    tmp=closes[:-2]
    openNew=opens[1:-1]/tmp
    closeNew=closes[1:-1]/tmp
    highNew=highs[1:-1]/tmp
    lowNew=lows[1:-1]/tmp
    ReY=closes[2:]/closes[1:-1]-1
    X=np.column_stack([openNew,closeNew,highNew,lowNew])
    return X,ReY

def Fig(labels,labelsU,ReY): #对不同分类作图
    Rlist=[];titles=[]
    for i in range(len(labelsU)):
        tem=labels==labelsU[i]
        Rlist.append(ReY[tem])
        titles.append('Label:'+str(labelsU[i]))
    plt.figure(figsize=(15,8))
    for i in range(len(titles)):
        plt.plot(Rlist[i].cumsum(),label=titles[i])
    plt.title(objectTrade)
    plt.legend()
    plt.grid()
    plt.show()

X,ReY=GetXY('2000-01-01','2012-01-01')
scaler=preprocessing.StandardScaler() #数据标准化，等同于Z-score
X=scaler.fit_transform(X)
pca=PCA(2)
X=pca.fit_transform(X)
clf=MLPClassifier(solver='adam',max_iter=2000,hidden_layer_sizes=(10,5),activation='tanh')
tmp=np.ones(len(ReY))
tmp[ReY>0.005]=2
tmp[ReY<-0.005]=0
#print((tmp==0).sum())
#print((tmp==1).sum())
#print((tmp==2).sum())
kk=clf.fit(X,tmp)

labels=clf.predict(X)
labelsU=np.unique(labels)
Fig(labels,labelsU,ReY)

X,ReY=GetXY('2012-01-01','2017-12-01')
X=scaler.transform(X)
X=pca.transform(X)
labels=clf.predict(X)
Fig(labels,labelsU,ReY)




