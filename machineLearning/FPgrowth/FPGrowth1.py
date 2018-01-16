#!usr/bin/python
# coding:utf-8

class FPtreeNode:
    # 定义FP树，属性为节点名字、节点出现次数、节点的父节点、与节点相似的元素项、节点的所有子节点
    def __init__(self, nameValue, numOccur, parentNode):
        self.nameValue = nameValue
        self.numOccur = numOccur
        self.parent = parentNode
        self.nodeLink = None
        self.children = {}
    # 增加节点的出现次数
    def inc(self, numOccur):
        self.numOccur += numOccur
    # 输出FP树的文本
    def disp(self, ind=1):
        print " "*ind, self.nameValue, " ",self.numOccur
        for child in self.children.values():
            child.disp(ind+1)

# 数据集和最小频繁项值
def createFPTree(dataSet, minSup = 1):
    # 建立头表，存入单个元素和相应次数
    headerTables = {}
    # 获取每个元素在数据集中出现的频率
    for trans in dataSet:
        for item in trans:
            headerTables[item] = headerTables.get(item,0) + dataSet[trans]
    # 将频率小于minSup的元素清除
    for key in headerTables.keys():
        if headerTables[key] <  minSup :
            del(headerTables[key])
    # 获取单项的频繁项集
    freqItem = set(headerTables.keys())
    if len(freqItem) == 0: return None, None
    # 建立头指针表
    for k in headerTables:
        headerTables[k] = [headerTables[k], None];
    retTree = FPtreeNode('null set', 1, None)
    # 遍历数据集
    for tranSet, count in dataSet.items():
        # 获取本条记录中的单项频繁项
        localD = {}
        for item in tranSet:
            if item in freqItem:
                localD[item] = headerTables[item][0]
        if len(localD) > 0:
            # 对频繁项进行频率排序
            orderedItems = [ v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            # 更新树
            updateTree(orderedItems, retTree, headerTables, count)
    return retTree, headerTables

def updateTree(items, inTree, headerTables, count):
    # 如果当前频繁项存在子树中，增加子树次数；否则添加新子树
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = FPtreeNode(items[0], count, inTree)
    # 如果头指针表没有指向该频繁项，则指向该项的树节点；否则调整树中相同频繁项指向
    if headerTables[items[0]][1] == None:
        headerTables[items[0]][1] = inTree.children[items[0]]
    else:
        updateHeader(headerTables[items[0]][1], inTree.children[items[0]])
    # 如果此频繁项列还有元素，继续进行迭代。
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTables, count)

def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat
def createinitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return  retDict

