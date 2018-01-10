#!usr/bin/python
#coding=utf8

from numpy import *

def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split("\t"))-1
    dataMat = []; labels = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labels.append(float(curLine[-1]))
    return dataMat, labels

def standRegres(xArr, yArr):
    xMat = mat(xArr); yMat = mat(yArr).T
    xTx = xMat.T * xMat
    if linalg.det(xTx) == 0.0:
        print "当前矩阵不可逆"
        return
    ws = xTx.I * (xMat.T*yMat)
    return ws

# 使用高斯核对附近的点赋予更高的权重
# 第一个参数是测试点，第二个是数据集，第三个是结果集，第四个是高斯核参数，为1时为线性
def lwlr(testPoint, xArr, yArr, k = 1.0):
    xMat = mat(xArr); yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye(m))
    for j in range(m):
        diffMat = testPoint - xMat[j,:]
        weights[j,j] = exp(diffMat * diffMat.T / (-2.0*k**2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0:
        print "矩阵不可逆！"
    ws = xTx.I * (xMat.T * (weights * yMat))
    return  testPoint*ws

def lwlrTest(testArr, xArr, yArr, k =1.0):
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i], xArr, yArr, k)
    return yHat

# 计算均方误差
def ressError(yArr, yHatArr):
    return ((yArr-yHatArr)**2).sum()

# 岭回归计算回归系数
def  ridgeRegress(xMat, yMat, lam = 0.2):
    xTx = xMat.T * xMat
    demon = xTx + eye(shape(xMat)[1])*lam
    if linalg.det(demon) == 0.0:
        print "矩阵不可逆"
        return
    ws = demon.T * (xMat.T * yMat)
    return ws

def ridgeTest(xArr, yArr):
    xMat = mat(xArr); yMat = mat(yArr).T
    # 计算指定维度的平均值
    yMean = mean(yMat, 0)
    yMat = yMat - yMean
    xMeans = mean(xMat, 0)
    # 计算指定维度的方差
    xVar = var(xMat, 0)
    # 对特征进行标准化处理
    xMat = (xMat - xMeans) / xVar
    numTestPts = 30
    wMat = zeros((numTestPts, shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegress(xMat, yMat, exp(i-10))
        wMat[i,:] = ws.T
    return wMat

# 一种特征标准化处理
def regularize(xMat):
    inMat  = xMat.copy()
    inMeans = mean(inMat, 0)
    inVar = var(inMat, 0)
    inMat = (inMat - inMeans) / inVar
    return inMat

def stageWise(xArr, yArr, eps = 0.01, numIt = 100):
    xMat = mat(xArr); yMat = mat(yArr).T
    yMean = mean(yMat, 0)
    yMat = yMat - yMean
    xMat = regularize(xMat)
    m, n = shape(xMat)
    returnMat = zeros((numIt, n))
    # 不是说好的开始权重是1吗。。。zeros是个毛的。。
    weights = zeros((n,1)); wsTest = weights.copy();wsMax = weights.copy()
    for i in range(numIt):
        print  weights.T
        lowestError = inf
        for j in range(n):
            for sign in [-1, 1]:
                wsTest = weights.copy()
                wsTest[j] += eps*sign
                yTest = xMat*wsTest
                rssE = ressError(yMat.A, yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        weights = wsMax.copy()
        returnMat[i,:] = weights.T
    return returnMat





