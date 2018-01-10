#!usr/bin/python
#coding:utf-8

import kNN
import  numpy as np
import matplotlib

import matplotlib.pyplot as plt
# group, lable = kNN.createDataSet()
# print group
# print lable
# print kNN.classify([0,0], group, lable,3)

# dataMat, lables = kNN.file2matrix('datingTestSet2.txt')
# print dataMat
# print  lables[0:20]

# fig = plt.figure()
# ax = fig.add_subplot(111)
# # 数字5表示的是显示出来的样本点的大小
# ax.scatter(dataMat[:,0], dataMat[:,1], 5*np.array(lables), 5*np.array(lables))
# plt.show()
# normMat, ranges, minVals = kNN.autoNorm(dataMat)
# print normMat
# print ranges
# print minVals
kNN.datingClassTest()
# kNN.classifyPerson()
# kNN.datingTestNoNorm()


# k = kNN.array([1,2,3,4])
# n = kNN.array([2,3,4,5])
# print kNN.dot(k.T, n)
# print (k*k.T).sum(axis=0)**0.5


# 数字识别
# testVector = kNN.img2vector("testDigits/0_3.txt");
# print testVector[0,0:31]
# print testVector[0, 32:63]
# kNN.handwritingClassTest()

# f = open("1.txt")
# lines =  f.readlines()
# print len(lines)