#!usr/bin/python
#coding=utf8

import AdaBoost
import boost
from numpy import *
D = mat(ones((5,1))/5)
# dataArr, classlabel = AdaBoost.loadsimpData()
# print AdaBoost.bulidStump(dataArr, classlabel, D)
# classFileArr =  AdaBoost.adaBoostTrainsDS(dataArr, classlabel,9)
# boost.adaBoostTrainDS(dataArr, classlabel,9)
# print AdaBoost.AdaClassify([0,0], classFileArr)

dataArr, classLabel = AdaBoost.loadDataSet('horseColicTraining2.txt')
# 40次迭代效果最佳，错误13个
classofyArray,aggClassEst = AdaBoost.adaBoostTrainsDS(dataArr,classLabel, 43)

# testArr, testLabel = AdaBoost.loadDataSet('horseColicTest2.txt')
# prediction10 = AdaBoost.AdaClassify(testArr, classofyArray)
# errArr = mat(ones((67,1)))
# print errArr[prediction10 != mat(testLabel).T].sum()
AdaBoost.plotROC(aggClassEst.T,classLabel)
