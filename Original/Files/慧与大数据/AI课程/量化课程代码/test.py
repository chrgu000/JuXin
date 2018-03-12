import numpy as np

def getEnt(dataSet): # 计算熵值
    L=len(dataSet)
    labels=dataSet[:,-1]
    Ent=0
    for label in np.unique(labels):
        prob=sum(labels==label)/L
        Ent-=prob*np.log(prob)
    return Ent

def splitDataSet(dataSet,axis,value): # 按某个特征分类后的数据
    newData=dataSet[dataSet[:,axis]==value]
    return np.column_stack([newData[:,:axis],newData[:,axis+1:]])

def chooseBestFeatureToSplit(dataSet):  # 选择最优的分类特征
    numFeatures = len(dataSet[0])-1
    baseEntropy = getEnt(dataSet)  # 原始的熵
    bestInfoGain = 0
    bestFeature = -1
    for i in range(numFeatures):
        feature=dataSet[:,i]
        Li=len(feature)
        newEnt=0
        for valueF in np.unique(feature):
            prob=sum(feature==valueF)/Li
            subDataSet = splitDataSet(dataSet, i, valueF)
            newEnt+=prob*getEnt(subDataSet)
        infoGain = baseEntropy - newEnt  # 原始熵与按特征分类后的熵的差值
        if (infoGain > bestInfoGain):  # 若按某特征划分后，熵值减少的最大，则次特征为最优分类特征
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):    #按分类后类别数量排序，比如：最后分类为2男1女，则判定为男；
    classU=np.unique(classList)
    classNum=0
    classMax=''
    for classi in classU:
        tem=sum(classList==classi)
        if tem>classNum:
            classNum=tem
            classMax=classi
    return classMax

def createTree(dataSet,features):
    classList=dataSet[:,-1]  # 类别：男或女
    if len(np.unique(classList))==1:
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    bestFeat=chooseBestFeatureToSplit(dataSet) #选择最优特征
    bestFeatLabel=features[bestFeat]
    myTree={bestFeatLabel:{}} #分类结果以字典形式保存
    del(features[bestFeat])
    for value in np.unique(dataSet[:,bestFeat]):
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),features)
    return myTree

dataSet = np.array([['长发', '粗声', '男'],
           ['短发', '粗声', '男'],
           ['短发', '粗声', '男'],
           ['长发', '细声', '女'],
           ['短发', '细声', '女'],
           ['短发', '粗声', '女'],
           ['长发', '粗声', '女'],
           ['长发', '粗声', '女']])
features = ['头发','声音']
decisionTree=createTree(dataSet, features)
print(decisionTree)







