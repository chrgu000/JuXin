#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:05:57 2018

@author: austincao
"""

import os,shutil,cv2,time,json,pickle,pdb
import numpy as np
import tensorflow as tf

figSize=28 #square for input fig
channels=3 #RGB
#shutil.rmtree('/home/austin/Documents/ICar')

# prepare data from raw figures
dirImg='/home/austincao/Downloads/stinghua-tencent-data/'
dirNoneImg='/home/austincao/Downloads/stinghua-tencent-data-nosign_1/'
jsonFile='/home/austincao/Downloads/stinghua-tencent-data/annotations.json'
dirExtract='/home/austincao/Documents/trafficSign/data/'
numEachType=100
ratioTrain=0.9

#forward propogation parameters
inputNode=figSize*figSize
outputNodes=183 # final output nodes; and one of them stands for None
layer1Node=500

conv1Deep=32
conv1Size=3
conv2Deep=64
conv2Size=3
FCsize=512

# traing parameters
trainTimes=2000
BATCH=6000
regularizationRate=8.0
dropoutRatio=0.85
reTrain=1
showShape=1

modelSavePath="/home/austincao/Documents/trafficSign/model/test/"
modelName="model.ckpt"
if not os.path.exists(modelSavePath):
    os.makedirs(modelSavePath)
else:
    shutil.rmtree(modelSavePath)
    os.makedirs(modelSavePath)
def forwardP(inputTensor,train,regularizer):
    global showShape
    with tf.variable_scope('layer1-conv1',reuse=tf.AUTO_REUSE):
        conv1Weights=tf.get_variable("weight",[conv1Size,conv1Size,channels,conv1Deep],\
                            initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv1Biases=tf.get_variable("bias",[conv1Deep],initializer=tf.constant_initializer(0.0))
        conv1=tf.nn.conv2d(inputTensor,conv1Weights,strides=[1,1,1,1],padding="SAME")
#        lrn1=tf.nn.local_response_normalization(conv1, depth_radius = 2, alpha = 2e-05,
#                                              beta = 0.75, bias = 1.0, name = 'LRN')
        relu1=tf.nn.tanh(tf.nn.bias_add(conv1,conv1Biases))
    with tf.name_scope('layer2-pool'):
        pool1=tf.nn.max_pool(relu1,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")
    with tf.variable_scope("layer3-conv2",reuse=tf.AUTO_REUSE):
        conv2Weights=tf.get_variable("weight",[conv2Size,conv2Size,conv1Deep,conv2Deep],\
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv2Biases=tf.get_variable("bias",[conv2Deep],initializer=tf.constant_initializer(0.0))
        conv2=tf.nn.conv2d(pool1,conv2Weights,strides=[1,1,1,1],padding='SAME')
#        lrn2=tf.nn.local_response_normalization(conv2, depth_radius = 2, alpha = 2e-05,
#                                              beta = 0.75, bias = 1.0, name = 'LRN')
        relu2=tf.nn.tanh(tf.nn.bias_add(conv2,conv2Biases))   #modify activate function;
    with tf.name_scope("layer4-pool"):
        pool2=tf.nn.max_pool(relu2,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")
    if showShape:
        print('Relu1 Shape',end='')
        print(relu1.get_shape())
        print('Pool1 Shape',end='')
        print(pool1.get_shape())
        print('Relu2 Shape',end='')
        print(relu2.get_shape())
        print('Pool2 Shape',end='')
        print(pool2.get_shape())
        showShape=0
        
    poolShape=pool2.get_shape().as_list()
    nodes=poolShape[1]*poolShape[2]*poolShape[3]
    reshaped=tf.reshape(pool2,[-1,nodes])
    with tf.variable_scope("layer5-fc1",reuse=tf.AUTO_REUSE):
        fc1Weights=tf.get_variable("weight",[nodes,FCsize],initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer!=None:
            tf.add_to_collection("losses",regularizer(fc1Weights))
        fc1Biases=tf.get_variable('bias',[FCsize],initializer=tf.constant_initializer(0.0))
        fc1=tf.nn.tanh(tf.matmul(reshaped,fc1Weights)+fc1Biases)
        if train:
            fc1=tf.nn.dropout(fc1,dropoutRatio,name='dropout1')
            
#    with tf.variable_scope("layer6-fc2",reuse=tf.AUTO_REUSE):
#        fc2Weights=tf.get_variable("weight",[FCsize,FCsize2],initializer=tf.truncated_normal_initializer(stddev=0.1))
#        fc2Biases=tf.get_variable("bias",[FCsize2],initializer=tf.constant_initializer(0.0))
#        if regularizer !=None:
#            tf.add_to_collection('loss',regularizer(fc2Weights))
#        fc2=tf.matmul(fc1,fc2Weights)+fc2Biases
    with tf.variable_scope("layer7-fc3",reuse=tf.AUTO_REUSE):
        fc3Weights=tf.get_variable("weight",[FCsize,outputNodes],initializer=tf.truncated_normal_initializer(stddev=0.1))
        fc3Biases=tf.get_variable("bias",[outputNodes],initializer=tf.constant_initializer(0.0))
        if regularizer !=None:
            tf.add_to_collection('loss',regularizer(fc3Weights))
        logit=tf.matmul(fc1,fc3Weights)+fc3Biases
    return logit
    

def train(): #update Train() into trafficSignRecognition
    x=tf.placeholder(tf.float32,[None,figSize,figSize,channels],name='x-input')
    y=tf.placeholder(tf.int64,[None],name='y-input')
    
    regularizer=tf.contrib.layers.l2_regularizer(regularizationRate)
    y_=forwardP(x,True,regularizer)
#    y_=forwardP(xBatch,False,None)
    globalStep=tf.Variable(0,trainable=False)
    crossEntropyMean=tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y_,labels=y))
    loss=crossEntropyMean+tf.add_n(tf.get_collection("losses"))
    optimizer=tf.train.AdamOptimizer().minimize(loss,global_step=globalStep)
    accuracyTrain=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y_,1),y),tf.float32))
    
    y_vali=forwardP(x,False,None)
    accuracyVali=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y_vali,1),y),tf.float32))
    
    with tf.control_dependencies([optimizer]):
        train_op=tf.no_op(name='train')
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        infoDir=next(os.walk(dirExtract))
        dirTmp=infoDir[0]

        with open(dirTmp+'resize/all.pkl','rb') as tmp:
            dataTmp=pickle.load(tmp)
        figTrain=dataTmp['figTrain']
        labelTrain=dataTmp['labelTrain']
        figVali=dataTmp['figVali']
        labelVali=dataTmp['labelVali']
        Ltrain=len(labelTrain)

        saver=tf.train.Saver()
        ckpt=tf.train.get_checkpoint_state(modelSavePath)
        if ckpt and ckpt.model_checkpoint_path and not reTrain:
            saver.restore(sess,ckpt.model_checkpoint_path)
        numberTrain=int(len(labelTrain)*trainTimes/BATCH)+1
        records=[]
        t0=time.time()
        for i in range(numberTrain):
            tmp=np.random.choice(Ltrain,BATCH,replace=False)
            _,lossValue,step=sess.run([train_op,loss,globalStep],feed_dict={x:figTrain[tmp],y:labelTrain[tmp]})
            if i%50==0 or numberTrain-i<2:
                accuracyT=sess.run(accuracyTrain,feed_dict={x:figTrain,y:labelTrain})
                accuracyV=sess.run(accuracyVali,feed_dict={x:figVali,y:labelVali})
                records.append([lossValue,accuracyV])
                print("after %d training steps, loss on training batch is %f, and accuracies of Train and Validation are %f and %f." \
                      %(step,lossValue,accuracyT,accuracyV))
                saver.save(sess,os.path.join(modelSavePath,modelName),global_step=globalStep)
                if i!=0:
                    t1=time.time()
                    print('each train loop needs %.2f seconds.' %((t1-t0)/i))
                
        with open(modelSavePath+'records.pkl','wb') as tmp:
            pickle.dump(records,tmp)

def evaluate(figs,figLabels):
    with tf.Graph().as_default() as g:
        x=tf.placeholder(tf.float32,[None,figSize,figSize,channels],name="x-input")
        y=tf.placeholder(tf.int64,[None],name="y-input")
        y_=forwardP(x,False,None)
        accuracy=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(y_,1),y),tf.float32))
        with tf.Session() as sess:
            ckpt=tf.train.get_checkpoint_state(modelSavePath)
            if ckpt and ckpt.model_checkpoint_path:
                saver=tf.train.Saver()
                saver.restore(sess,ckpt.model_checkpoint_path)
                globalStep=ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                accuracyScore=sess.run(accuracy,feed_dict={x:figs,y:figLabels})
                print("After %s training steps, validation accuracy=%f"%(globalStep,accuracyScore))
            else:
                print("No checkpoint file found")
        

def getSamples():# resized into 28*28
    if os.path.exists(dirExtract):
        shutil.rmtree(dirExtract) 
    os.makedirs(dirExtract+'randomFigs/')
    os.makedirs(dirExtract+'standardFigs/')
    
    # create labelCount dictionary;
    with open(jsonFile) as tmp:
        hp=json.load(tmp)
    boxImgs=hp["imgs"]
    types=hp["types"]
    nameImg=list(boxImgs.keys())
    
    labelsCount={} # initiating for counting labels;
    for label in types:
        labelsCount[label]=0
    L=len(nameImg) #collect all types;
    for i in range(L):
        boxImg=boxImgs[nameImg[i]]
        for bI in boxImg['objects']:
            labelsCount[bI['category']]+=1
    Tmp=labelsCount.copy() #delete the type which is not gotten;
    for di in Tmp:
        if labelsCount[di]==0:
            del labelsCount[di]
    with open(dirExtract+'labelsCount.pkl','wb') as tmp:
        pickle.dump(labelsCount,tmp)
    # cut samples
    figs=[]
    figLabels=[]
    
    with open(jsonFile) as tmp:
        hp=json.load(tmp)
    boxImgs=hp["imgs"]
    types=hp["types"]
    nameImg=list(boxImgs.keys())
    L=len(nameImg)
    t1=time.time()
    labelRecord=[]
    for i in range(L):
        boxImg=boxImgs[nameImg[i]]
        for bI in boxImg['objects']:
            imgMat=cv2.imread(dirImg+boxImg['path'])
            bbox=bI['bbox']
            yT=bbox["ymax"]-bbox["ymin"]
            xT=bbox["xmax"]-bbox["xmin"]
            bI_cate=bI['category']
            if bI_cate not in labelRecord:
                labelRecord.append(bI_cate)
                standardImg=imgMat[int(bbox['ymin']):int(bbox['ymax']),\
                                   int(bbox['xmin']):int(bbox['xmax']),:]
                cv2.imwrite(dirExtract+'standardFigs/'+bI_cate+'-'+\
                            str(labelsCount[bI_cate])+'.png',standardImg)
                
            timesTmp=numEachType/labelsCount[bI_cate]
            if timesTmp<1:
                if np.random.rand()<=timesTmp:
                    timesCut=1
                else:
                    continue
            else:
                timesCut=int(np.round(timesTmp))
            for i2 in range(timesCut):
                lRatio=np.random.rand(4)*0.5
                xShape,yShape,_=imgMat.shape
                x1=int(max(0,bbox['xmin']-xT*lRatio[0]))
                x2=int(min(imgMat.shape[1],bbox['xmax']+xT*lRatio[1]))
                y1=int(max(0,bbox['ymin']-yT*lRatio[2]))
                y2=int(min(imgMat.shape[0],bbox['ymax']+yT*lRatio[3]))
                positive=imgMat[y1:y2,x1:x2,:]
    #            positive=cv2.resize(positive,(figSize,figSize),interpolation=cv2.INTER_CUBIC)
                figs.append(positive.tolist())
                figLabels.append(bI_cate)
        if not i%100 and i:
            if boxImg['objects']:
                cv2.imwrite(dirExtract+'randomFigs/'+figLabels[-1]+'-'+boxImg['path'].split('/')[-1],positive)
            t2=time.time()
            print('Complete {} %, and need {} minutes more.'.format(round(i/L*100,2),round((t2-t1)/60*((L-i-1)/(i+1)),2)))
        if  L-i<2:
            dirTmp,_,files=next(os.walk(dirNoneImg))
            for i2 in range(numEachType*2):
                imgMat=cv2.imread(dirTmp+'/'+files[i2])
                y_,x_,_=imgMat.shape
                while 1:
                    rand2=np.random.rand(2)*0.5
                    y0=rand2[0]*100
                    x0=rand2[1]*100
                    ymax=y0+40*(rand2[0]+1)
                    xmax=x0+40*(rand2[1]+1)
                    if  ymax < y_-2 and  xmax < x_-2:
                        positive=imgMat[int(y0):int(ymax),int(x0):int(xmax),:]
                        figs.append(positive.tolist())
                        figLabels.append('None')
                        break
            pklData={'figs':figs,'figLabels':figLabels}
            with open(dirExtract+'train'+str(i//1000)+'_'+str(len(figLabels))+'.pkl','wb') as tmp:
                pickle.dump(pklData,tmp)
        elif not i%1000 and i:
            pklData={'figs':figs,'figLabels':figLabels}
            with open(dirExtract+'train'+str(i//1000)+'_'+str(len(figLabels))+'.pkl','wb') as tmp:
                pickle.dump(pklData,tmp)
            figs=[]
            figLabels=[]
    reSize()

def reSize():
    pathFigTmp=dirExtract+'resize/'
    if os.path.exists(pathFigTmp):
        shutil.rmtree(pathFigTmp) 
    os.makedirs(pathFigTmp+'figures')    
    tmp=os.walk(dirExtract)
    dirTmp,_,files=next(tmp)
    Nfig=1
    figAll=[]
    labelAll=[]
    for file in files:
        print(file)
        wholeFile=os.path.join(dirTmp,file)
        with open(wholeFile,'rb') as tmp:
            pklData=pickle.load(tmp)
        figs=pklData['figs']
        figLabels=pklData['figLabels']
        figTmp=[]
        for i in range(len(figLabels)):
            dataNew=cv2.resize(np.array(figs[i],dtype=np.uint8),(figSize,figSize),interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(dirTmp+'/resize/figures/'+str(Nfig)+figLabels[i]+'.png',dataNew)
            Nfig+=1 
#            figTmp.append(dataNew.tolist())
            figAll.append(dataNew.tolist())
            labelAll.append(figLabels[i])
            
#        pklData['figs']=figTmp
#        with open(dirTmp+'/tmp/'+file,'wb') as tmp:
#            pickle.dump(pklData,tmp)

#    labelAll=[i for i in set(labelAll)]
#    dictLabel={}
#    for i in range(len(labelAll)):
#        dictLabel[labelAll[i]]=i
#    print('the number of all labels is {}.'.format(len(dictLabel)))
    laTmp=[i for i in set(labelAll)]
    dictLabel={}
    for i in range(len(laTmp)):
        dictLabel[laTmp[i]]=i
    print('the number of all labels is {}.'.format(len(dictLabel))) 
    with open(dirExtract+'dictLabel.pkl','wb') as tmp:
        pickle.dump(dictLabel,tmp)
        
    labelAll=[dictLabel[i] for i in labelAll] 
    Ltmp=len(labelAll)
    tmp=np.random.choice(Ltmp,Ltmp,replace=False)
    figAll=np.array(figAll)
    labelAll=np.array(labelAll)
    figTrain=[]
    labelTrain=[]
    figVali=[]
    labelVali=[]
    noneValue=dictLabel['None']
    tmp=labelAll==noneValue
    figTmp=figAll[tmp][:numEachType]
    splitPoint=int(numEachType*ratioTrain)
    figTrain.extend(figTmp[:splitPoint].tolist())
    figVali.extend(figTmp[splitPoint:].tolist())
    labelTrain.extend([noneValue]*splitPoint)
    labelVali.extend([noneValue]*(numEachType-splitPoint))    
    del dictLabel['None']
    numS=int(numEachType/2) # how many samples should be selected for each type
    for (key,value) in dictLabel.items():
        indexTmp=labelAll==value
        Lstmp=sum(indexTmp)
        if Lstmp<numS:
            selectTmp=Lstmp
        else:
            selectTmp=numS
        figTmp=figAll[indexTmp][:selectTmp]
        splitPoint=int(selectTmp*ratioTrain)
        figTrain.extend(figTmp[:splitPoint].tolist())
        figVali.extend(figTmp[splitPoint:].tolist())
        labelTrain.extend([value]*splitPoint)
        labelVali.extend([value]*(selectTmp-splitPoint))   
    figTrain=np.array(figTrain)
    figVali=np.array(figVali)
    labelTrain=np.array(labelTrain)
    labelVali=np.array(labelVali)
    Ltmp=len(labelTrain)
    tmp=np.random.choice(Ltmp,Ltmp,replace=False)
    figTrain=figTrain[tmp]
    labelTrain=labelTrain[tmp]
    Ltmp=len(labelVali)
    tmp=np.random.choice(Ltmp,Ltmp,replace=False)
    figVali=figVali[tmp]
    labelVali=labelVali[tmp]
    
    pklData={'figTrain':figTrain,'labelTrain':labelTrain,'figVali':figVali,'labelVali':labelVali}
    with open(dirTmp+'/resize/all.pkl','wb') as tmp:
        pickle.dump(pklData,tmp)
    
#    tmp=os.walk(dirExtract+'tmp/')
#    dirTmp,_,files=next(tmp)
#    for file in files:
#        print(file)
#        wholeFile=os.path.join(dirTmp,file)
#        with open(wholeFile,'rb') as tmp:
#            pklData=pickle.load(tmp)
#        figLabels=pklData['figLabels']
#        labelTmp=[dictLabel[i] for i in figLabels]
#        pklData['figLabels']=labelTmp
#        with open(wholeFile,'wb') as tmp:
#            pickle.dump(pklData,tmp)
    
#getSamples()
#reSize()
train()
#evaluate(figs,figLabels)











