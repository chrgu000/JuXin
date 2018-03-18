

import pandas as pd
from sklearn import preprocessing
import pdb

def NN(x,y,hiddenLayers,learnRatio):
    netWork=np.concatenate([[x.shape[0]],hiddenLayers,[y.shape[0]]])
    Lnet=len(netWork)
    theta=[]
    for i in range(Lnet-1):
        theta.append(np.random.randn(netWork[i+1],netWork[i]))

    for i in range(10000):
        a=[x]
        for i2 in range(1,Lnet):
            a.append(1 / (1 + np.exp(-np.dot(theta[i2-1], a[i2-1]))))

        delta=[a[-1]-y]
        for i2 in range(1,Lnet):
            delta.insert(0,np.dot(theta[-i2].T, delta[-i2]) * (a[-i2-1] * (1 - a[-i2-1])))
        for i2 in range(0,Lnet-1):
            theta[i2]-=learnRatio*np.dot(delta[i2+1],a[i2].T)/x.shape[0]

    print("the training result is:")
    tmp1=np.argmax(y,axis=0)
    tmp2=np.argmax(a[-1],axis=0)
    print(sum(tmp1==tmp2)/y.shape[1])

data=pd.read_csv('C:\\Users\\Administrator\\Desktop\\iris.txt',sep=',',header=None)
x=data.iloc[:,:4].values
x=preprocessing.minmax_scale(x)
x=x.T
y=data.iloc[:,4].values
# pdb.set_trace()
# NN(x,y,[10,20,12],learnRatio=0.1)
# print(data)
Y=[]
for i in y:
    if i=='Iris-setosa':
        Y.append([1,0,0])
    elif i=='Iris-versicolor':
        Y.append([0,1,0])
    else:
        Y.append([0,0,1])
Y=np.array(Y).T
NN(x,Y,[8,8],learnRatio=0.3)
















