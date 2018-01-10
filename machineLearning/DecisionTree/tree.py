#!usr/bin/python
# coding:utf-8
from math import log
import operator

# 计算数据集的香农商
def calcShannonEnt(dataset):
    numEntries = len(dataset)
    LabelCounts = {}
    for featVec in dataset:
        currentLabel = featVec[-1] # 获取当前类别
        # 计算类别频率
        if currentLabel not in LabelCounts.keys():
            LabelCounts[currentLabel] = 0
        LabelCounts[currentLabel] +=1
    # 信息熵计算
    shannonEnt = 0.0
    for key in LabelCounts:
        prob = float(LabelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

# 划分数据集 参数分别为：带划分的数据集、划分数据集的特征、需要返回的特征的值
def splitDataSet(dataSet, axis, value) :
    retDataSet = []
    for featVec in dataSet :
        if featVec[axis] == value :
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return  retDataSet

# 选择最好的分类特征
# dataSet需要是列表，且所有的列表元素具有相同的数据长度，最后一个元素是当前实例的类别标签
def chooseBestFeature(dataSet):
    numFeatures = len(dataSet[0]) -1 # 获取特征总数
    baseEntropy = calcShannonEnt(dataSet) #基本信息熵
    bestInfoGain = 0.0 #最好的信息熵
    bestFeature = -1 # 最好的分类特征
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet] #获取所有样本第i个特征值的集合
        uniqueVals = set(featList) #对集合进行去重，得到当前特征的唯一特征值
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i , value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob *calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy # 计算信息增益
        # 根据最大信息增益值，进行最好分类特征选取
        if(infoGain > bestInfoGain) :
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys() :
            classCount[vote] = 0
        classCount[vote]+=1
    # 字典对象存储了每个类标签出现的频率，使用operator操作键值排序字典，返回分类次数最多的分类名称
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, Labels) :
    classList = [ example[-1] for example in dataSet] # 获取数据集的类别
    # 如果全是一类，那么就直接返回当前类为节点
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 遍历所有的特征对象，返回分类次数最多的
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    # 选取影响最大的特征的下标
    bestFeature = chooseBestFeature(dataSet)
    # 获取影响最大的特征
    beatFeatLable = Labels[bestFeature]
    # 建立决策树
    myTree = {beatFeatLable : {}}
    # 已将影响最大的特征加入树，则在特征集中删除该特征
    del(Labels[bestFeature])
    # 获取此特征列，即此特征的特征值集合
    featValues = [example[bestFeature] for example in dataSet]
    # 对集合进行唯一性去重
    uniqueVals = set(featValues)
    # 根据此特征的有几个特征值建立几个子树
    for value in uniqueVals:
        subLables = Labels[:]
        myTree[beatFeatLable][value] = createTree(splitDataSet(dataSet, bestFeature, value), subLables)
    return myTree
# 进行分类
def classify(inputTree, featLables, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLables.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLables, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel
def storeTree(inputTree, fileName):
    import pickle
    fw = open(fileName,'w')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    import  pickle
    fr = open(filename, 'r')
    return pickle.load(fr)





