# x轴和y轴单位长度相等
b=plt.plot([11,12,13,41])
ax = plt.gca()
ax.set_aspect(1)
plt.show()


#3D散点图
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

x=np.array([[1.2,2.2,2.3],[2.1,2.2,3.1],[5,5.6,6.5],[1.8,3.2,3.9],[1.5,4.2,3.2]])
y=x-x.mean(axis=0)
z=np.cov(y,rowvar=0)
values,vectors=np.linalg.eig(z)
tmp=np.array(np.dot(x,vectors[:,[0,1]]))

fig=plt.figure()
# plt.scatter(tmp[:,0],tmp[:,1],c=['r','y','g','b','k'])
ax=Axes3D(fig)
ax.scatter(x[:,0],x[:,1],x[:,2],c=['r','y','g','b','k'])
ax = plt.gca()
ax.set_aspect(1)
plt.show()
