#!usr/bin/python
#coding:utf8

import  logRegres
from numpy import *
dataMat, Lables = logRegres.loadDataSet()
weights =  logRegres.stocGradAscent1(array(dataMat), Lables)

logRegres.plotBestFit(dataMat, Lables, weights)


# x = arange(-3.0, 3.0, 0.1)
# print x


# logRegres.muliTest()