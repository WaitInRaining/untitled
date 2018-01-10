#!usr/bin/python
#coding=utf8

import regression
from numpy import *
import matplotlib.pyplot as plt
dataMat, labels = regression.loadDataSet('ex0.txt')
ws = regression.standRegres(dataMat, labels)
# print ws
#
# # 绘制原始数据
xMat = mat(dataMat); yMat = mat(labels)
fig =  plt.figure()
ax = fig.add_subplot(111)
ax.scatter(xMat[:,1].flatten().A[0], yMat.T[:,0].flatten().A[0], s =2, c='red')
#
#
# # 预测数据
# yHat = regression.lwlrTest(dataMat, dataMat, labels,k=0.003)
# srtInd = xMat[:,1].argsort(0)
# xSort = xMat[srtInd][:,0,:]
# ax.plot(xSort[:,1], yHat[srtInd])
# plt.show()

xCopy = xMat.copy()
xCopy.sort(0)
yHat = xCopy * ws
ax.plot(xCopy[:,1], yHat)
print corrcoef(yHat.T, yMat)
plt.show()

# 在训练集上预测鲍鱼年龄
featArr ,ageArr = regression.loadDataSet('abalone.txt')
# predictionArr01 = regression.lwlrTest(featArr[0:99], featArr[0:99],ageArr[0:99],0.0972)
# predictionArr1 = regression.lwlrTest(featArr[0:99], featArr[0:99],ageArr[0:99],1.0)
# predictionArr10 = regression.lwlrTest(featArr[0:99], featArr[0:99],ageArr[0:99],10)
#
# print regression.ressError(ageArr[0:99], predictionArr01.T)
# print regression.ressError(ageArr[0:99], predictionArr1.T)
# print regression.ressError(ageArr[0:99], predictionArr10.T)
# 在测试集上预测鲍鱼年龄，在测试集上，k=2时效果最好
# predictionArr01 = regression.lwlrTest(featArr[100:199], featArr[0:99],ageArr[0:99],0.0972)
# predictionArr1 = regression.lwlrTest(featArr[100:199], featArr[0:99],ageArr[0:99],1.0)
# predictionArr10 = regression.lwlrTest(featArr[100:199], featArr[0:99],ageArr[0:99],2)
# print regression.ressError(ageArr[100:199], predictionArr01.T)
# print regression.ressError(ageArr[100:199], predictionArr1.T)
# print regression.ressError(ageArr[100:199], predictionArr10.T)

# 岭回归 这个有问题，下次看一下
ridgeWeights = regression.ridgeTest(featArr, ageArr)
#
# # 前向逐步回归
stageWise =  regression.stageWise(featArr, ageArr,0.01, 200)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(ridgeWeights)
# ax.plot(stageWise)
# plt.show()

