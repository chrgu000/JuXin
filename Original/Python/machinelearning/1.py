import numpy as np

# x=np.random.randn(6,5).T
# y=np.array([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0],[1,0,0,0]]).T
#
# theta1=np.random.randn(10,5)
# theta2=np.random.randn(10,10)
# theta3=np.random.randn(4,10)
#
# for i in range(1000):
#     a1=x
#     a2=1/(1+np.exp(-np.dot(theta1,a1)))
#     a3=1/(1+np.exp(-np.dot(theta2,a2)))
#     a4=1/(1+np.exp(-np.dot(theta3,a3)))
#
#     delta4=a4-y
#     delta3=np.dot(theta3.T,delta4)*a3*(1-a3)
#     delta2=np.dot(theta2.T,delta3)*a2*(1-a2)
#
#     tmp=x.shape[1]
#     theta1-=np.dot(delta2,a1.T)/tmp
#     theta2-=np.dot(delta3,a2.T)/tmp
#     theta3-=np.dot(delta4,a3.T)/tmp
#
# print(a4)

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












