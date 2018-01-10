#!usr/bin/python
#coding=utf8

import regTree
myDat = regTree.loadDataSet('ex00.txt')
retTree =  regTree.createTree(myDat)
print retTree
