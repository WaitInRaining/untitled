#!usr/bin/python
# coding:utf-8
import Apriori

dataSet = Apriori.loadDataSet()
print dataSet
# c1 = Apriori.createC1(dataSet)
# print c1
# D = map(set, dataSet)
# L1, supportData0 = Apriori.scanD(D, c1, 0.5)
# print L1
# print supportData0
L,supportData = Apriori.apriori(dataSet)
print L
print supportData
print '\n'
rules = Apriori.generateRules(L, supportData, 0.7)
print rules


print  dataSet[0][:1]