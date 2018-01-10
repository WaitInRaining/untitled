#!usr/bin/python
#coding=utf-8

import svmMLiA
dataArr, lableArr = svmMLiA.loadDataSet('testSet.txt')
# b, alpha = svmMLiA.smoSimple(dataArr, lableArr, 0.6, 0.001, 40)
# print b
# print svmMLiA.shape(alpha)
# print alpha[alpha>0]
# b,alpha = svmMLiA.smoP(dataArr,lableArr, 0.6, 0.0001, 40)
# print b
# print alpha[alpha>0]
# ws = svmMLiA.calcWs(alpha, dataArr, lableArr)
# print ws

# svmMLiA.testRbf()
svmMLiA.testDigits(('rbf',10))
# svm.testRbf()