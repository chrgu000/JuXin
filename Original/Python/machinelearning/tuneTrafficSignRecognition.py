#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:16:37 2018

@author: austincao
"""

import os,shutil,cv2,time,json,pickle
import numpy as np
import tensorflow as tf

conv1SizeS=[5,3]
FCsizeS=[1024,512]
regularizationRateS=[0.00001,0.0001,0.001]

figSize=28 #square for input fig
channels=3 #RGB
#shutil.rmtree('/home/austin/Documents/ICar')

# prepare data from raw figures
dirExtract='/home/austincao/Documents/trafficSign/data/'

#forward propogation parameters
inputNode=figSize*figSize
outputNodes=182 # final output nodes
layer1Node=500

conv1Deep=32
#conv1Size=5
conv2Deep=64
conv2Size=5
#FCsize=512

# traing parameters
trainTimes=2000
BATCH=6000
#regularizationRate=0.00001
reTrain=1


for conv1Size in conv1SizeS:
    for FCsize in FCsizeS:
        for regularizationRate in regularizationRateS:
            t1=time.time()
            g=tf.Graph()
            with g.as_default():
                modelSavePath="/home/austincao/Documents/trafficSign/model/"+str(conv1Size)+'-'+str(FCsize)+'-'+str(regularizationRate)
                modelName="model.ckpt"
                if not os.path.exists(modelSavePath):
                    os.makedirs(modelSavePath)
                else:
                    shutil.rmtree(modelSavePath)
                    os.makedirs(modelSavePath)                    
                def forwardP(inputTensor,train,regularizer):
                    with tf.variable_scope('layer1-conv1',reuse=tf.AUTO_REUSE):
                        conv1Weights=tf.get_variable("weight",[conv1Size,conv1Size,channels,conv1Deep],\
                                            initializer=tf.truncated_normal_initializer(stddev=0.1))
                        conv1Biases=tf.get_variable("bias",[conv1Deep],initializer=tf.constant_initializer(0.0))
                        conv1=tf.nn.conv2d(inputTensor,conv1Weights,strides=[1,1,1,1],padding="SAME")
                        relu1=tf.nn.relu(tf.nn.bias_add(conv1,conv1Biases))
                    with tf.name_scope('layer2-pool'):
                        pool1=tf.nn.max_pool(relu1,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")
                    with tf.variable_scope("layer3-conv2",reuse=tf.AUTO_REUSE):
                        conv2Weights=tf.get_variable("weight",[conv2Size,conv2Size,conv1Deep,conv2Deep],\
                                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
                        conv2Biases=tf.get_variable("bias",[conv2Deep],initializer=tf.constant_initializer(0.0))
                        conv2=tf.nn.conv2d(pool1,conv2Weights,strides=[1,1,1,1],padding='SAME')
                        relu2=tf.nn.relu(tf.nn.bias_add(conv2,conv2Biases))
                    with tf.name_scope("layer4-pool"):
                        pool2=tf.nn.max_pool(relu2,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")
                    poolShape=pool2.get_shape().as_list()
                    nodes=poolShape[1]*poolShape[2]*poolShape[3]
                    reshaped=tf.reshape(pool2,[-1,nodes])
                    with tf.variable_scope("layer5-fc1",reuse=tf.AUTO_REUSE):
                        fc1Weights=tf.get_variable("weight",[nodes,FCsize],initializer=tf.truncated_normal_initializer(stddev=0.1))
                        if regularizer!=None:
                            tf.add_to_collection("losses",regularizer(fc1Weights))
                        fc1Biases=tf.get_variable('bias',[FCsize],initializer=tf.constant_initializer(0.0))
                        fc1=tf.nn.relu(tf.matmul(reshaped,fc1Weights)+fc1Biases)
                        if train:
                            fc1=tf.nn.dropout(fc1,0.5)
                    with tf.variable_scope("layer6-fc2",reuse=tf.AUTO_REUSE):
                        fc2Weights=tf.get_variable("weight",[FCsize,outputNodes],initializer=tf.truncated_normal_initializer(stddev=0.1))
                        fc2Biases=tf.get_variable("bias",[outputNodes],initializer=tf.constant_initializer(0.0))
                        if regularizer !=None:
                            tf.add_to_collection('loss',regularizer(fc2Weights))
                        logit=tf.matmul(fc1,fc2Weights)+fc2Biases
                    return logit

                def train(): #update Train() into trafficSignRecognition
                    x=tf.placeholder(tf.float32,[None,figSize,figSize,channels],name='x-input')
                    y=tf.placeholder(tf.int64,[None],name='y-input')
                    dataSets=tf.data.Dataset.from_tensor_slices((x,y))
                #    iterator=dataSets.shuffle(Nsamples).repeat().batch(BATCH).make_initializable_iterator()
                    iterator=dataSets.repeat().batch(BATCH).make_initializable_iterator()
                    (xBatch,yBatch)=iterator.get_next()
                    
                    regularizer=tf.contrib.layers.l2_regularizer(regularizationRate)
                    y_=forwardP(xBatch,False,regularizer)
                    globalStep=tf.Variable(0,trainable=False)
                    crossEntropyMean=tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y_,labels=yBatch))
                    loss=crossEntropyMean#+tf.add_n(tf.get_collection("losses"))
                    optimizer=tf.train.AdamOptimizer().minimize(loss,global_step=globalStep)
                    
                    y_vali=forwardP(x,False,None)
                    accuracyTrain=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y_vali,1),y),tf.float32))
                    
                    with tf.control_dependencies([optimizer]):
                        train_op=tf.no_op(name='train')
                    with tf.Session() as sess:
                        tf.global_variables_initializer().run()
                        infoDir=next(os.walk(dirExtract))
                        dirTmp=infoDir[0]
                        filesTmp=infoDir[2]
                        figs=[]
                        figLabels=[]
                #        for file in filesTmp:
                #            with open(os.path.join(dirTmp,file),'rb') as tmp:
                #                dataTmp=pickle.load(tmp)
                #            figs.extend(dataTmp['figs'])
                #            figLabels.extend(dataTmp['figLabels'])
                        with open(dirTmp+'resize/all.pkl','rb') as tmp:
                            dataTmp=pickle.load(tmp)
                        figTrain=dataTmp['figTrain']
                        labelTrain=dataTmp['labelTrain']
                        figVali=dataTmp['figVali']
                        labelVali=dataTmp['labelVali']
                               
                        sess.run(iterator.initializer,feed_dict={x:figTrain,y:labelTrain})
                        saver=tf.train.Saver()
                        ckpt=tf.train.get_checkpoint_state(modelSavePath)
                        if ckpt and ckpt.model_checkpoint_path and not reTrain:
                            saver.restore(sess,ckpt.model_checkpoint_path)
                        numberTrain=int(len(labelTrain)*trainTimes/BATCH)+1
                        records=[]
                        for i in range(numberTrain):
                            _,lossValue,step=sess.run([train_op,loss,globalStep])
                            if i%100==0 or numberTrain-i<2:
                                accuracyT=sess.run(accuracyTrain,feed_dict={x:figVali,y:labelVali})
                                records.append([lossValue,accuracyT])
                                print("after %d training steps, loss on training batch is %f, and accuracy is %f." \
                                      %(step,lossValue,accuracyT))
                                saver.save(sess,os.path.join(modelSavePath,modelName),global_step=globalStep)
                        with open(modelSavePath+'records.pkl') as tmp:
                            pickle.dump(records,tmp)
                        
                train()
                t2=time.time()
                print('consume time {} minutes.'.format(round((t2-t1)/60,2)))
