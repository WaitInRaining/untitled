#!usr/bin/python
#coding:utf-8

from numpy import *
import operator
from os import listdir

"""
初始化数据集
"""
def createDataSet():
    group = array([[1.0, 1.1],\
                   [1.0, 1.0],\
                   [0, 0],\
                   [0 , 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

# 分类算法，参数：输入向量，训练样本集，标签向量，最近邻数目
def classify(inX, dataset, lables, k) :
    # 获取数据集的大小
    dataSetSize = dataset.shape[0]
    # 对输入样本进行维度扩充，减去训练集的各个样本
    diffMat = tile(inX, (dataSetSize, 1)) - dataset

    # 平方计算
    sqDiffMat = diffMat ** 2
    # # 求和
    sqDistances = sqDiffMat.sum(axis=1)
    # # 开方
    distances =  sqDistances ** 0.5
    # 以上使用欧氏距离计算输入样本 和训练集样本的距离

    # distances  = []
    # xt = dataset.T  # 获取样本的转置
    # D = cov(xt)  # 计算协方差矩阵
    # invD = linalg.inv(D)  # 获取逆矩阵
    #
    # for i in range(dataSetSize):
    #     tp = inX - dataset[i]
    #     distances.append(sqrt(dot(dot(tp,invD),tp.T)))
    #使用马氏距离计算输入样本 和训练集样本的距离

    # for i in range(dataSetSize):
    #    distances.append(dot(inX.T,dataset[i]) /
    #                     (((inX.T*inX).sum(axis=0)*(dataset[i].T*dataset[i]).sum(axis=0)) ** 0.5))
    # 使用余弦相似度计算距离

    # distances = array(distances)
    # 按照距离进行排序
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        # 获取前k个样本的类别
        voteIlabel = lables[sortedDistIndicies[i]]
        # 累计前k个样本分属类别的数目
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # 将字典分解为元组，然后按照第二元素的次序对元组进行排序
    sortedClassCount = sorted(classCount.iteritems(),\
                              key = operator.itemgetter(1), reverse=True)
    # 返回频率最高的元素标签
    return sortedClassCount[0][0]
# 使用wk_knn,这种方法对k个近邻的样本按照他们距离待分类样本的远近给一个权值
def wk_knn(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    w=[]
    for i in range(k):
        w.append((distances[sortedDistIndicies[k-1]]-distances[sortedDistIndicies[i]]\
        )/(distances[sortedDistIndicies[k-1]]-distances[sortedDistIndicies[0]]))
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + w[i]
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]



def file2matrix(fileName):
    # 打开文件
    file = open(fileName)
    # 按行获取文件内容
    arrayOLines = file.readlines()
    # 获取行数
    numberOfLines = len(arrayOLines)
    # 创建一个numberOfLines行，3列的零矩阵
    returnMat = zeros((numberOfLines, 2))
    # 初始化元组
    classLableVector = []
    index  = 0
    for line in arrayOLines :
        # 截掉所有的回车字符串
        line = line.strip()
        # 进行每列划分
        listFromLine = line.split('\t')
        # 获取样本向量
        returnMat[index,:] = listFromLine[0:2]
        # 获取样本类别
        classLableVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLableVector
# 使用的是min-max标准化
def autoNorm(dateSet):
    # 每列的最小值
    minVals = dateSet.min(0)
    # 每列的最大值
    maxVals = dateSet.max(0)
    ranges = maxVals - minVals
    # 生成一个和dateSet一样大小的零矩阵
    norDataSet = zeros(shape(dateSet))
    # 得到dateSet的行数
    m = dateSet.shape[0]
    normDataSet = dateSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))
    return  normDataSet, ranges, minVals
# 结果测试，随机抽取十分之一为测试结果
def datingClassTest() :
    hoRatio = 0.10
    dataMat, labels = file2matrix("datingTestSet2.txt")
    normMat, ranges, minVals = autoNorm(dataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify(normMat[i, :],normMat[numTestVecs:m, :],\
                                    labels[numTestVecs:m], 3)
        print ("分类为：%d,正确为：%d" % (classifierResult, labels[i]))
        if (classifierResult != labels[i]) :
            errorCount +=1.0
    print ("错误率为：%f" % (errorCount / float(numTestVecs)))
# 不适用归一化测试数据集
def datingTestNoNorm():
    hoRation = 0.10
    dataMat , Labels = file2matrix('datingTestSet2.txt')
    m = dataMat.shape[0]
    numTestVecs = int(m*hoRation)
    errCount = 0
    for i in range(numTestVecs):
        classifiResult = classify(dataMat[i,:], dataMat[numTestVecs:m, :], Labels[numTestVecs:m], 3)
        print ("分类为：%d, 正确为: %d" % (classifiResult, Labels[i]))
        if(classifiResult != Labels[i]) :
            errCount = errCount+1
    print "错误率为：%f" % (errCount/ float(numTestVecs))
#输入样本测试结果
def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percenTats = float(raw_input("percentage of time spent playing video game?"))
    fMiles = float(raw_input("frequent filer miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    dataMat, labels = file2matrix("datingTestSet2.txt")
    normMat, ranges, minVals = autoNorm(dataMat)
    inArr = array([fMiles, percenTats, iceCream])
    classifierResult = classify((inArr-minVals)/ranges,normMat,labels,3 )
    print "You will probably like this person:",resultList[classifierResult-1]

# 将文本表示的图像转化为向量
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        linestr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(linestr[j])
    return returnVect

def handwritingClassTest():
    Labels = []
    trainFileList = listdir('trainingDigits')
    m = len(trainFileList)
    trainDataMat = zeros((m,1024))
    # 获取训练集和训练类别
    for i in range(m):
        # 获取文件
        fileNameStr = trainFileList[i]
        # 获取文件名称：0_0
        filestr = fileNameStr.split('.')[0]
        classNum = int(filestr.split('_')[0])#获取正确数字
        Labels.append(classNum);
        # 填充训练集
        trainDataMat[i,:] = img2vector('trainingDigits/%s' %fileNameStr)
    # 获取训练集
    testFileList = listdir("testDigits")
    errorCount = 0;
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        filestr = fileNameStr.split('.')[0]
        classNumStr = int(filestr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' %fileNameStr)
        classifyResult =  classify(vectorUnderTest, trainDataMat, Labels, 3)
        print "识别的数：%d,真正的数：%d" %(classifyResult, classNumStr)
        if classifyResult != classNumStr:
            ++errorCount
    print "总错误数：%d" % errorCount
    print "错误率为：%d" % (errorCount/float(mTest))
