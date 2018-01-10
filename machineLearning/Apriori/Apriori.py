#!usr/bin/python
# coding:utf-8

def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
# 构建单个物品的项集列表
def createC1(dataSet):
    c1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    # 对于c1中每个项构建一个不变集合
    return map(frozenset, c1)
# 扫描数据集
def scanD(D, ck, minSupport):
     ssCnt = {}
     for tid in D:
         for can in ck:
             if can.issubset(tid):
                 if not ssCnt.has_key(can): ssCnt[can] = 1
                 else : ssCnt[can] += 1
     numItem = float(len(D))
     retList= []
     supportData = {}
     for key in ssCnt:
         support = ssCnt[key] / numItem
         if support >= minSupport:
             retList.insert(0,key)
             supportData[key] = support
     return retList, supportData
# 生成频繁项大小为K的频繁项集
def aprioriGen(LK, k):
    retList = []
    lenLK = len(LK)
    for i in range(lenLK):
        for j in range(i+1, lenLK):
            L1 = list(LK[i])[:k-2];L2 = list(LK[j])[:k-2]
            L1.sort();L2.sort()
            if L1 == L2:
                retList.append(LK[i] | LK[j])
    return retList
# 生成所有频繁项集和对应支持度
def apriori(dataSet, minSupport = 0.5):
    c1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, c1, minSupport)
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0):
        ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L , supportData
# 计算置信度：频繁项集、频繁项集中的单项、数据集、规则列表、最小置信度
def calcConf(freqSet, H, supportData, br1, minConf = 0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print freqSet-conseq,'-->',conseq,'conf:',conf
            br1.append((freqSet-conseq, conseq, conf))
    return prunedH
# 参数：频繁项集、可以出现在规则右部的元素列表H
def ruleFromConseq(FreqSet, H, supportData, br1, minConf = 0.7):
    m = len(H[0])
    if (len(FreqSet) > (m+1)):
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(FreqSet, Hmp1, supportData, br1, minConf)
        if (len(Hmp1) > 1):
            ruleFromConseq(FreqSet, Hmp1, supportData, br1, minConf)

def generateRules(L, supportData, minConf = 0.7):
    bigReluList = []
    # 从1开始，值获取有两个或更多元素的集合
    for i in range(1 , len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > i):
                ruleFromConseq(freqSet, H1, supportData, bigReluList, minConf)
            else:
                calcConf(freqSet, H1, supportData,bigReluList, minConf)
    return bigReluList
