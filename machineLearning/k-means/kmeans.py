#!usr/bin/python
# coding:utf-8
from numpy import *
import matplotlib.pyplot as plt
def loadDataSet(filename):
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    return dataMat
# 计算距离 欧式距离
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))

# 初始化质心 通过计算每一维数据的边界值，然后在边界值中随机选取位置
def randCent(dataSet, k):
    n = shape(dataSet)[1]
    # 初始化质心
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = minJ +rangeJ * random.rand(k,1)
    return centroids

def kmeans(dataSet, k, distMeas = distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    # 第一维存储距离点最近的质点下标，第二维存储最小距离
    clusterAssment = mat(zeros((m,2)))
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:], dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex:
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        # print centroids
        for cent in range(k) :
            pstInClust = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]
            centroids[cent,:] = mean(pstInClust, axis=0)
    return centroids, clusterAssment

def  biKmeans(dataSet, k , distMeas=distEclud):
    m = shape(dataSet)[0]
    # 第一维存储距离点最近的质点下标，第二维存储最小距离
    clusterAssment = mat(zeros((m,2)))
    # 计算整个数据集的质心
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    # 将第一个质心加入质心序列中
    cenList = [centroid0]
    # 计算d单个质心时的SSE值
    for j in range(m):
        clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
    # 当簇数目小于k时
    while(len(cenList) < k):
        lowestSSE = inf
        # 对于每一个质心
        for i in range(len(cenList)):
            # 获取当前质心的数据集
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A == i)[0],:]
            # 对当前数据集进行二分均值划分,第一个值为质心集合,第二个为[质心坐标，sse值]的集合
            centroidMat, spliClustAss = kmeans(ptsInCurrCluster, 2, distMeas)
            # 计算总的sse值
            sseSplit = sum(spliClustAss[:,1])
            # 计算其他簇的sse值的总和
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A != i)[0],1])
            print "当前簇的sse值 , 其他簇的sse值:", sseSplit, sseNotSplit
            # 如果当前簇划分后sse减小
            if (sseSplit + sseNotSplit) < lowestSSE:
                # 指定当前簇为最佳划分簇
                bestCenToSplit = i
                # 指定最佳划分质点
                bestNewCents = centroidMat
                # 获取最佳划分,[质心坐标，sse值]的集合
                bestClustAss = spliClustAss.copy()
                # 更新lowestSSE
                lowestSSE = sseNotSplit +  sseSplit
        # 对于划分后质心下标为1的质心，更新质心坐标为簇数目，因为二分簇划分只有下标为1和0；两个簇
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0], 0] = len(cenList)
        # 对于划分后质心下标为0的质心，更新质心坐标为最佳划分簇
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0], 0] = bestCenToSplit
        print "最优划分簇为：", bestCenToSplit
        print "最优簇sse值的长度为：",len(bestClustAss)
        # 保存当前的最佳划分质心，下标对应质心点
        cenList[bestCenToSplit] = bestNewCents.tolist()[0]
        # 加入另一个质心
        cenList.append(bestNewCents.tolist()[1])
        # 保存新的质心的sse值
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCenToSplit)[0],:] = bestClustAss
    return mat(cenList), clusterAssment



