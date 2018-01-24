#!usr/bin/python
# coding:utf-8
from numpy import *
def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in  fr.readlines()]
    dataArr = [map(float, line) for line in stringArr]
    return mat(dataArr)

# 输入数据集和主维度数
def pca(dataMat, topNfeat= 99999):
    meanVals = mean(dataMat, axis=0)
    meanRemoved = dataMat - meanVals
    covMat = cov(meanRemoved, rowvar=0)#求协方差矩阵
    eigVals, eigVects = linalg.eig(mat(covMat)) #计算矩阵的特征值和特征向量
    eigValInd = argsort(eigVals)# 对特征值进行从小到大排序，返回的是特征值对应的下标
    eigValInd = eigValInd[:-(topNfeat+1):-1]#将特征值逆置
    # 将数据转换到新的空间
    redEigVects = eigVects[:,eigValInd]
    lowDDataMat = meanRemoved * redEigVects #暂时没有理解
    reconMat = (lowDDataMat * redEigVects.T) + meanVals#暂时没有理解
    return lowDDataMat, reconMat

def replaceNaNwithMeans():
    dataMat = loadDataSet('secom.data', ' ')
    numFeat = shape(dataMat)[1]
    for i in range(numFeat):
        meanVal = mean(dataMat[nonzero(~isnan(dataMat[:,i].A))[0],i])
        dataMat[nonzero(isnan(dataMat[:,i].A))[0], i] = meanVal
    return dataMat


