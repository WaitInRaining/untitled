#!usr/bin/python
# coding:utf-8


import tree
import treeplotter

# dataset = [[1,1,'yes'],
#            [1,1,'yes'],
#            [1,0,'no'],
#            [0,1,'no'],
#            [0,1,'no']]
# labels = ['no surfacing', 'filppers']
# dataset[0][-1] = 'maybe'
# shannonEnt =  tree.calcShannonEnt(dataset)
# print shannonEnt

# print tree.splitDataSet(dataset, 0, 0)
# print tree.chooseBestFeature(dataset)
# print tree.createTree(dataset, labels)
# treeplotter.createPlot()
# myTree = treeplotter.retrieveTree(0)
# print myTree
# print treeplotter.getNumLeafs(myTree)
# print treeplotter.getTreeDepth(myTree)
# treeplotter.createPlot(myTree)
# print tree.classify(myTree, labels,[1,1])
fr = open('lenses.txt')
lines = fr.readlines()

lensesAll = [ inst.split("\t") for inst in lines]
lensesTrain = lensesAll[5:len(lines)]
lensesLables = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = tree.createTree(lensesTrain, lensesLables[:])
# treeplotter.createPlot(lensesTree)
# lensesTree =  tree.grabTree( 'Decision.txt')
# treeplotter.createPlot(lensesTree)
for i in range(5):
    print "分类为%s, 正确为%s" %(tree.classify(lensesTree, lensesLables, lensesAll[i][0:-1]), lensesAll[i][-1])



