# -*-coding:utf-8 -*-
# import numpy as np
# import pdb
#
# x = np.array([[1, 0, 0,1,1],
#               [0, 0, 1,0,1],
#               [0, 1, 0,1,0],
#               [1, 0, 1,0,1],
#               [1,0,1,1,0]
#               ]).T
# y = np.array([[1, 0, 0, 0],[0,1,0,0],[0,0,0,1],[0,1,0,0],[0,0,0,1]]).T
# theta = np.random.randn(4,5)
# theta1=np.random.randn(10,10)
#
# for i in range(1000):
#     l1 = 1/(1+np.exp(-np.dot(theta, x)))
#     l1_error = l1-y
#     l1_delta = l1_error * (l1*(1-l1))
#     theta -= np.dot(l1_delta,x.T)
#
# print("the training result is:")
# print(l1)

# import numpy as np
# import pdb
#
# x=np.random.randn(5,5).T
# y = np.array([[1, 0, 0, 0],[0,1,0,0],[0,0,0,1],[0,1,0,0],[0,0,0,1]]).T
# theta1 = np.random.randn(10,5)
# theta2=np.random.randn(10,10)
# theta3=np.random.randn(4,10)
#
# for i in range(1000):
#     a1=x
#     a2 = 1/(1+np.exp(-np.dot(theta1, a1)))
#     a3= 1/(1+np.exp(-np.dot(theta2, a2)))
#     a4= 1/(1+np.exp(-np.dot(theta3, a3)))
#     delta4=a4-y
#     delta3=np.dot(theta3.T,delta4)*(a3*(1-a3))
#     delta2=np.dot(theta2.T,delta3)*(a2*(1-a2))
#     tmp=x.shape[0]
#     theta1 -= np.dot(delta2,a1.T)/tmp
#     theta2 -= np.dot(delta3,a2.T)/tmp
#     theta3 -= np.dot(delta4,a3.T)/tmp
#
# print("the training result is:")
# print(a4)

import numpy as np
import pdb

def NN(x,y,hiddenLayers,learnRatio):
    netWork=np.concatenate([[x.shape[0]],hiddenLayers,[y.shape[0]]])
    Lnet=len(netWork)
    theta=[]
    for i in range(Lnet-1):
        theta.append(np.random.randn(netWork[i+1],netWork[i]))

    for i in range(1000):
        a=[x]
        for i2 in range(1,Lnet):
            a.append(1 / (1 + np.exp(-np.dot(theta[i2-1], a[i2-1]))))

        delta=[a[-1]-y]
        for i2 in range(1,Lnet):
            delta.insert(0,np.dot(theta[-i2].T, delta[-i2]) * (a[-i2-1] * (1 - a[-i2-1])))
        for i2 in range(0,Lnet-1):
            theta[i2]-=learnRatio*np.dot(delta[i2+1],a[i2].T)/x.shape[0]

    print("the training result is:")
    print(a[-1])

x=np.random.randn(5,5)
y = np.array([[1, 0, 0, 0],[0,1,0,0],[0,0,0,1],[0,1,0,0],[0,0,0,1]]).T
NN(x,y,[10,20,12],learnRatio=0.1)




