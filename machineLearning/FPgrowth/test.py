#/usr/bin/python
# coding:utf-8

import fpGrowth

simpDat = fpGrowth.loadSimpDat()
dataSet = fpGrowth.createInitSet(simpDat)

retTree, headTab = fpGrowth.createTree(dataSet, 3)
retTree.disp()