import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import requests
sess=tf.Session()

housing_url='https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.data'
housing_header = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
cols_used = ['CRIM', 'INDUS', 'NOX', 'RM', 'AGE', 'DIS', 'TAX', 'PTRATIO', 'B', 'LSTAT']
num_features=len(cols_used)
housing_file=requests.get(housing_url)
housing_data=[[float(x) for x in y.split(' ') if len(x)>=1] \
               for y in housing_file.text.split('\n') if len(y)>=1]

y_vals=np.transpose([np.array([y[13] for y in housing_data])])
x_vals=np.array([[x for i,x in enumerate(y) if housing_header[i] \
                  in cols_used] for y in housing_data])

train_indices=np.random.choice(len(x_vals),round(len(x_vals)*0.8),replace=False)
test_indices=np.array(list(set(range(len(x_vals)))-set(train_indices)))
x_vals_train=x_vals[train_indices]
x_vals_test=x_vals[test_indices]
y_vals_train=y_vals[train_indices]
y_vals_test=y_vals[test_indices]
k=4
batch_size=len(x_vals_test)
x_data_train=tf.placeholder(shape=[None,num_features],dtype=tf.float32)
x_data_test=tf.placeholder(shape=[None,num_features],dtype=tf.float32)
y_target_train=tf.placeholder(shape=[None,1],dtype=tf.float32)
y_target_test=tf.placeholder(shape=[None,1],dtype=tf.float32)

distance=tf.reduce_sum(tf.abs(tf.subtract(x_data_train,\
                tf.expand_dims(x_data_test,1))),reduction_indices=2)
top_k_xvals,top_k_indices=tf.nn.top_k(tf.negative(distance),k=k)
x_sums=tf.expand_dims(tf.reduce_sum(top_k_xvals,1),1)
x_sums_repeated=






























