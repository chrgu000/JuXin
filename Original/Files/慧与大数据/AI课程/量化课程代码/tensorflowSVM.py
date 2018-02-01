import numpy as np
import pandas as pd
import tensorflow as tf

# get samples and their labels
iris = pd.read_csv('C:\\Users\\Administrator\\Desktop\\iris.txt',header=None)
x=iris.iloc[:,:4].values.T
y=iris.iloc[:,4].values
y = np.array([[1 if i=='Iris-setosa' else -1 for i in y]])

# use Gaussian Kernal to transform
xGaussian=[]
x=x.T
for i in range(x.shape[0]):
    xGaussian.append(np.exp(-np.sum((x[i]-x)**2,axis=-1)/3))
x=np.array(xGaussian).T

# define placeholder for samples
Lx=x.shape[0]
xHolder = tf.placeholder(shape=[Lx, None], dtype=tf.float32)
yHolder = tf.placeholder(shape=[1, None], dtype=tf.float32)

# define variables for thetas
w = tf.Variable(tf.random_normal(shape=[1,Lx]))
b = tf.Variable(tf.random_normal(shape=[1]))

# get one part of Loss caused by thetas
lossTheta = tf.reduce_sum(tf.square(w))
# get one part of Loss caused by wrong labels
lossLabels = tf.reduce_mean(tf.maximum(0., tf.subtract(1., tf.multiply(yHolder,tf.add(tf.matmul(w,xHolder), b)))))
# Loss together
loss = tf.add(lossLabels, tf.multiply(0.01, lossTheta))

# create optimizer
opt = tf.train.GradientDescentOptimizer(0.01)
train = opt.minimize(loss)

# train
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
for i in range(1000):
    sess.run(train, feed_dict={xHolder: x, yHolder: y})

# predict
w=np.array(sess.run(w))
b = sess.run(b)

y_predict=np.dot(w,x)+b
y_predict=y_predict.flatten()>=0
print('the predict accuracy:{}%'.format((y_predict==(y>0)).sum()/len(y[0])*100))














































