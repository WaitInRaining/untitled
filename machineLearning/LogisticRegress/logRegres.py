#!usr/bin/python
#coding:utf8

import math
from numpy import *
def loadDataSet():
    dataMat = [];labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[-1]))
    return dataMat, labelMat

def sigmoid(inX):
    return 1.0 / (1 + exp(-inX)) # 不能使用math的e,因为是矩阵运算，所以使用numpy的e

def gradAscent(dataMat, classLabels):
    dataMatrix = mat(dataMat)  # 转换为矩阵
    labelMat =  mat(classLabels).transpose()# array(classLabels).T
    m,n = shape(dataMatrix) # 获取矩阵的行数、列数
    alpha = 0.001
    maxCycles = 500 #定义迭代次数
    weights = ones((n,1)) #初始化权重系数，n列1行
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        error = (labelMat - h)
        weights = weights + alpha * dataMatrix.T *error
    return weights
# 使用随机梯度上升,dataMatrix为数组型数据集

def stocGradAscent0(dataMatrix, classLables):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    maxCycles = 200
    for k in range(maxCycles):
        for i in range(m):
            h = sigmoid(sum(dataMatrix[i] * weights))
            error = classLables[i] - h
            weights = weights + alpha * error * dataMatrix[i]
    return weights

# 改进的随机梯度上升
"""
    在数值收敛后仍然会出现一些波动，产生的原因是存在一些不能正确分类的样本点。
    在每次迭代后会引发系数的剧烈改变，我们期望算法能避免来回波动，从而收敛到某一个值并加快收敛速度。
"""
def stocGradAscent1(dataMatrix, classLables, numIter = 150):
    m, n = shape(dataMatrix)
    weights = ones(n)
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            # 对alpha进行每次迭代调整，且随着迭代一直减小，但不会到0，这样是为了保证在多次迭代后新数据仍然具有一定的影响。
            # 如果要处理的问题是动态变化的，那么可以适当加大常数项，来确保新的值获得更大的回归系数
            aplha = 4 / (1.0 + i + j) + 0.01
            # 随机选取样本来更新回归系数，减少了周期性的波动
            randIndex = int(random.uniform(0,len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex] * weights))
            error = classLables[randIndex] - h
            weights = weights + aplha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX * weights))
    if prob  > 0.5:return  1.0
    else: return 0.0

def colicTest():
    frTrain = open('horseColicTraining.txt')
    frTest = open('horseColicTest.txt')
    trainingSet = []; trainingLables = []
    for line in frTrain.readlines():
        # strip()移除字符串头尾指定的字符
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLables.append(float(currLine[-1]))
    trainWeights = stocGradAscent1(array(trainingSet), trainingLables, 500)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights)) != int(currLine[-1]):
            errorCount += 1
    errorRate = (float(errorCount) / numTestVec)
    print "错误率为 %f" % errorRate
    return  errorRate
def muliTest():
    numTests = 10; errorSum = 0.0
    for k in range(numTests):
        errorSum += colicTest()
    print "经过 %d 次迭代后，平均错误率为: %f" % (numTests, errorSum / float(numTests))


def plotBestFit(dataMat, classLables, weight):
    import matplotlib.pyplot as plt
    # dataMat, classLables = loadDataSet()
    dataMatrix  = array(dataMat)
    n = shape(dataMatrix)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    # 对每一个点进行绘制
    for i in range(n):
        if int(classLables[i]) == 1:
            xcord1.append(dataMatrix[i, 1])
            ycord1.append(dataMatrix[i, 2])
        if int(classLables[i]) == 0:
            xcord2.append(dataMatrix[i, 1])
            ycord2.append(dataMatrix[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s = 30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s = 30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weight[0] - weight[1] * x)/ weight[2]
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()
