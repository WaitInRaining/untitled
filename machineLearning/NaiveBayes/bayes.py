#!usr/bin/python
# coding:utf-8

from numpy import *
def loadDataSet():
    postingList = [['my','dog','has','flea','problems','help','please'],
                   ['maybe','not','take','him','to','dog','park','stupid'],
                   ['my','dalmation','is','so','cute','I','love','him'],
                   ['stop','posting','stupid','worthless','garbage'],
                   ['mr','licks','ate','my','steak','how','to','stop','him'],
                   ['qiut','buying','worthless','dog','food','stupid']]
    classVec = [0,1,0,1,0,1] # 1代表侮辱性的，0代表正场言论
    return postingList, classVec
# 建立词表
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document) #创建两集合的并集
    return list(vocabSet)

# 建立词向量,词在词集中存在为1，不存在为0
#第一个为总词库，第二个为输入的词列表
#输出为词列表的向量化
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word %s is not in my Vocabulary!" % word
    return returnVec

# 建立词向量，记录一个词在词集中出现的次数
def bagOfWord2VecMN(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] +=1
    return returnVec


# 第一个是文档矩阵，第二个是每篇文档的分类
# 返回为类0的条件概率，类1的条件概率，和类1的概率
def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix) #获取文档数目
    numWords = len(trainMatrix[0]) # 获取词向量长度
    # 由于trainCategory中分类为0/1，计算sum(trainCategory)就是计算分类为1的数目，即类1出现的概率
    pAbusive =  sum(trainCategory) / float(numTrainDocs)
    # 如果使用0进行初始化，假设有一个词内有出现，那么整个概率为1，此处使用拉普拉斯平滑
    p0Num = ones(numWords); p1Num = ones(numWords)
    # 因为是两类，所以分母+2
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        # 如果是类别1，则增加类1中各词汇出现的频率和类别1出现的频率
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        # 如果是其他类别，则增加其中各词汇出现的频率和此类别出现的频率，即只进行两种类别的分类
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    # 取对数防止下溢出
    p1Vec = log(p1Num / p1Denom)
    p0Vec = log(p0Num / p0Denom)

    return p0Vec, p1Vec, pAbusive

# 输入向量、类0条件概率、类1条件概率、类1概率
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 >= p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVecabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVecabList, postinDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVecabList, testEntry))
    print testEntry, 'classified as :', classifyNB(thisDoc, p0V, p1V, pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVecabList, testEntry))
    print testEntry,'classified as :', classifyNB(thisDoc, p0V, p1V, pAb)

# 文本分词,使用除单词、数字外的任意字符进行分割，然后对分割后的字符串进行小写转换
def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [token.lower() for token in listOfTokens if len(token) > 2]

def spamTest():
    docList = []; classList = []; fullText = []
    for i in range(1,26):
        # 垃圾邮件
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        # 正常邮件
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList) # 建立包含所有词的词库
    trainingSet = range(50) # 初始化训练集
    testSet = []
    # 随机选取10个进行测试，并在训练集中删除测试样本
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []; trainClasses = []
    # 获取词向量矩阵和对应词向量类别
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    # 训练分类器，获取条件概率和概率
    p0V,p1V,pSpam = trainNB0(array(trainMat), array(trainClasses))
    errorCount = 0;
    # 使用测试集检测分类器的准确率
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex] :
            errorCount +=1
            print wordVector
    print 'the error rate is :', float(errorCount / len(testSet))

# 计算词汇出现的频率,返回出现频率最高的30个词
def calcMostFreg(vocabList, fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]

def localWords(feed1, feed0):
    import feedparser
    docList = []; classList = []; fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    # 每次访问一条RSS源
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)

        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)

    vocabList = createVocabList(docList) #建立词向量
    top30Words = calcMostFreg(vocabList, fullText) #统计出现次数最多的的30个词
    # 去除出现次数最高的词
    for pairw in top30Words:
        if pairw[0] in vocabList: vocabList.remove(pairw[0])
    trainingSet = range(2*minLen); testSet = []
    # 进行测试集选取，以作交叉验证
    for i in range(4):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []; trainClass = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWord2VecMN(vocabList,docList[docIndex]))
        trainClass.append(classList[docIndex])
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClass))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWord2VecMN(vocabList, docList[docIndex])
        if classifyNB(wordList, p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ', float(errorCount) / len(testSet)
    return vocabList,p0V, p1V

