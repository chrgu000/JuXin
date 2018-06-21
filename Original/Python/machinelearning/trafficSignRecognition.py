import os,cv2,time,pickle,pdb
import numpy as np
import tensorflow as tf

figSize=28 #square for input fig
channels=3 #RGB

#forward propogation parameters
inputNode=figSize*figSize
outputNodes=50 # final output nodes
layer1Node=500

conv1Deep=32
conv1Size=5
conv2Deep=64
conv2Size=5
FCsize=512

# traing parameters
learningRateBase=0.001
learningRateDecay=0.99
regularizationRate=0.0001
trainingSteps=3
movingAverageDecay=0.99

modelSavePath="e:\\ICar"
modelName="model.ckpt"

def forwardP(inputTensor,train,regularizer):
    with tf.variable_scope('layer1-conv1'):
        conv1Weights=tf.get_variable("weight",[conv1Size,conv1Size,channels,conv1Deep],\
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv1Biases=tf.get_variable("bias",[conv1Deep],initializer=tf.constant_initializer(0.0))
        conv1=tf.nn.conv2d(inputTensor,conv1Weights,strides=[1,1,1,1],padding="SAME")
        relu1=tf.nn.relu(tf.nn.bias_add(conv1,conv1Biases))
    with tf.name_scope('layer2-pool'):
        pool1=tf.nn.max_pool(relu1,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")
    with tf.variable_scope("layer3-conv2"):
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
    with tf.variable_scope("layer5-fc1"):
        fc1Weights=tf.get_variable("weight",[nodes,FCsize],initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer!=None:
            tf.add_to_collection("losses",regularizer(fc1Weights))
        fc1Biases=tf.get_variable('bias',[FCsize],initializer=tf.constant_initializer(0.0))
        fc1=tf.nn.relu(tf.matmul(reshaped,fc1Weights)+fc1Biases)
        if train:
            fc1=tf.nn.dropout(fc1,0.5)
    with tf.variable_scope("layer6-fc2"):
        fc2Weights=tf.get_variable("weight",[FCsize,outputNodes],initializer=tf.truncated_normal_initializer(stddev=0.1))
        fc2Biases=tf.get_variable("bias",[outputNodes],initializer=tf.constant_initializer(0.0))
        if regularizer !=None:
            tf.add_to_collection('loss',regularizer(fc2Weights))
        logit=tf.matmul(fc1,fc2Weights)+fc2Biases
    return logit
    

def train(figs,figLabels):
    x=tf.placeholder(tf.float32,[None,figSize,figSize,channels],name='x-input')
    yRaw=tf.placeholder(tf.int32,[None],name='y-input')
    tmp=tf.concat([tf.expand_dims(tf.range(len(figLabels)),1),tf.expand_dims(yRaw,1)],1)
    y_=tf.cast(tf.sparse_to_dense(tmp,[len(figLabels),43],1.0,0.0),tf.float32)
        
    regularizer=tf.contrib.layers.l2_regularizer(regularizationRate)
    y=forwardP(x,True,regularizer)
    globalStep=tf.Variable(0,trainable=False)
    
    variableAverage=tf.train.ExponentialMovingAverage(movingAverageDecay,globalStep)
    variableAverageOp=variableAverage.apply(tf.trainable_variables())
    crossEntropy=tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y,labels=tf.argmax(y_,1))
    crossEntropyMean=tf.reduce_mean(crossEntropy)
    loss=crossEntropyMean+tf.add_n(tf.get_collection("losses"))
    learningRate=tf.train.exponential_decay(learningRateBase,globalStep,5,learningRateDecay,staircase=True)
    trainStep=tf.train.GradientDescentOptimizer(learningRate).minimize(loss,global_step=globalStep)
    with tf.control_dependencies([trainStep,variableAverageOp]):
        train_op=tf.no_op(name='train')
    saver=tf.train.Saver()
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        for i in range(trainingSteps):
            xs,ys=figs,figLabels
            _,lossValue,step=sess.run([train_op,loss,globalStep],feed_dict={
                    x:xs,yRaw:ys})
    
            print("after %d training steps, loss on training batch is %f." %(step,lossValue))############################
            saver.save(sess,os.path.join(modelSavePath,modelName),global_step=globalStep)##########
            
            if 1%100==0:
                print("after %d training steps, loss on training batch is %f." %(step,lossValue))
                saver.save(sess,os.path.join(modelSavePath,modelName),global_step=globalStep)

def evaluate(figs,figLabels):
    with tf.Graph().as_default() as g:
        x=tf.placeholder(tf.float32,[None,figSize,figSize,channels],name="x-input")
        y_=tf.placeholder(tf.float32,[None,outputNodes],name="y-input")
        validateFeed={x:figs,y_:figLabels}
        y=forwardP(x,False,None)
        
        correct_prediction=tf.equal(tf.arg_max(y,1),tf.arg_max(y_,1))
        accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
        variableAverages=tf.train.ExponentialMovingAverage(movingAverageDecay)
        variable2Restore=variableAverages.variables_to_restore()
        saver=tf.train.Saver(variable2Restore)
        
        while True:
            with tf.Session() as sess:
                ckpt=tf.train.get_checkpoint_state(modelSavePath)
                if ckpt and ckpt.model_checkpoint_path:
                    saver.restore(sess,ckpt.model_checkpoint_path)
                    globalStep=ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                    accuracyScore=sess.run(accuracy,feed_dict=validateFeed)
                    print("After %s training steps, validation accuracy=%f"%(globalStep,accuracyScore))
                else:
                    print("No checkpoint file found")
                    return
            time.sleep(10)

def getSamples():
    try:
        with open('E:/trafficSignRecognition.pkl','rb') as fileTem:
            pklData=pickle.load(fileTem)
        figs=pklData['figs']
        figLabels=pklData['figLabels']
    except:            
        saveDir="E:/TrainIJCNN2013/"
        files=os.walk(saveDir)
        subDirs=next(files)[1]
        figs=[]
        figLabels=[]
        figSize=28
        for Dir in subDirs:
            files=os.listdir(saveDir+Dir)
            files=[saveDir+Dir+'/'+file for file in files]
            for file in files:           
                figs.append(cv2.resize(cv2.imread(file),(figSize,figSize)).tolist())
                figLabels.append(int(Dir))
                Ltmp=len(figs)
                cv2.imwrite('e:/tmp/'+str(Ltmp)+'.png',np.array(figs[-1]))
        pklData={"figs":figs,"figLabels":figLabels}
        with open('E:/trafficSignRecognition.pkl','wb') as fileTem:
            pickle.dump(pklData,fileTem)
    
    return (figs,figLabels)

(figs,figLabels)=getSamples()
#figs=np.array(figs)
#figLabels=np.array(figLabels)
#indexS=np.random.choice(len(figLabels),20,replace=False)
#figs=figs[indexS]
#figLabels=figLabels[indexS]
train(figs,figLabels)






































































