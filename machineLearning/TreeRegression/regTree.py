#/usr/bin/python
#!coding=utf8

from numpy import *
def loadDataSet(filename):
    f = open(filename)
    dataMat = []
    for line in f.readlines():
       curLine = line.strip().split('\t');
       fltLine = map(float, curLine) #将每一行映射成浮点数
       dataMat.append(fltLine)
    return dataMat
# 数据集，待分割特征，分割特征的值
def binSplitDataSet(dataSet, feature, value):
    # 获取该特征>Value的子集
    mat0 = dataSet[nonzero(dataSet[:,feature] > value)[0], :][0]
    # 获取该特征<=Value的子集
    mat1 = dataSet[nonzero(dataSet[:,feature] <= value)[0], :][0]
    return mat0, mat1
# 建立叶节点的函数
def regLeaf(dataSet):
    return mean(dataSet[:,-1])
# 误差估计的函数
def regErr(dataSet):
    return var(dataSet[:,-1]) * shape(dataSet)[0]
# 获取最好的二元划分
def chooseBestSplit(dataSet, leafType = regLeaf,errType = regErr, ops = (1,4)):
    tolS = ops[0];tolN = ops[1]
    # 如果只有一个不重复的样本
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1:
        return  None, leafType(dataSet)
    m,n = shape(dataSet)
    # 获取最大误差
    S = errType(dataSet)
    bestS = inf; bestIndex = 0; bestValue = 0
    # 对于每一个特征
    for featIndex in range(n-1):
        # 对于每一个特征的所有特征值
        for splitVal in set(dataSet[:,featIndex]):
            # 以当前值进行二分，mat0是大于当前值的样本集，mat1是小于等于当前值的样本集
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            # 如果划分后的两个样本集的数量小于某个值则进行下一次迭代
            if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): continue
            # 获取划分后的误差值
            newS = errType(mat0) + errType(mat1)
            # 如果误差值更小，记录特征索引，记录特征值，
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    # 如果误差值变化不大，则返回原始误差值
    if (S -bestS) < tolS:
        return None, leafType(dataSet)
    # 获取最好特征值的二分数据集
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    # 如果划分后的两个样本集的数量小于某个值则返回原始原始误差值
    if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):
        return None, leafType(dataSet)
    return bestIndex, bestValue



# 创建树。数据集，建立叶节点的函数，进行误差值计算的函数,ops为构建树所需的其他参数的数组
def createTree(dataSet, leafType = regLeaf, errType = regErr, ops=(1,4)):
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops)
    if feat == None: return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = createTree(lSet, leafType, errType, ops)
    retTree['right'] = createTree(rSet, leafType, errType, ops)
    return retTree


