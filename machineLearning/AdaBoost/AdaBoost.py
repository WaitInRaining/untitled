#!usr/bin/python
#coding=utf-8
from numpy import *
def loadsimpData():
    dataMat = matrix([[1., 2.1],
                      [2., 1.1],
                      [1.3, 1.],
                      [1., 1.],
                      [2., 1.]])
    classLabels = [1.0,1.0, -1.0, -1.0, 1.0]
    return dataMat, classLabels

#构建单层决策树--------------


# 简易分类，判断属性值是大于threshVal的多还是小于threshVal的多
def stumpClassify(dataMat, dimen, threshVal, threshIneq):
    retArray = ones((shape(dataMat)[0],1))
    if threshIneq == 'lt':
        retArray[dataMat[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMat[:,dimen] > threshVal] = -1.0
    return  retArray

# 数据集，类别，权重
def bulidStump(dataArr, classLabels, D):
    dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
    m, n = shape(dataMatrix)
    numSteps = 10.0;
    # 存储给定权重向量D时所得到的最佳单层决策树信息
    bestStump = {}; bestClassEst = mat(zeros((m,1)))
    minError = inf
    # 在数据的所有特征上遍历
    for i in range(n):
        # 使用最小值和最大值来恒定步长
        rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max()
        stepSize = (rangeMax - rangeMin) / numSteps
        # 遍历各级步长
        for j in range(-1, int(numSteps) + 1):
            # lt 为less than gt是greater than 即大于和小于；遍历大于小于
            for inequal in {'lt', 'gt'}:
                threshVal = (rangeMin + float(j) * stepSize)
                # 获取第i行数据的预测值
                predictedVals = stumpClassify(dataMatrix, i, threshVal, inequal)
                # 如果预测失败，errArr对应部分为1
                errArr = mat(ones((m,1)))
                errArr[predictedVals == labelMat] = 0
                # 进行权重重新计算
                weightedError = D.T * errArr
                # print "split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, threshVal, inequal, weightedError)
                # 如果当前错误率小于已有最小错路率，记录该单层决策树
                if weightedError < minError:
                    minError = weightedError
                    bestClassEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump, minError, bestClassEst

def adaBoostTrainsDS(dataArr, classLabels, numIt = 40):
    weakClassArr = [];
    m = shape(dataArr)[0]
    D = mat(ones((m,1))/m)
    aggClassEst = mat(zeros((m,1)))
    # 迭代numIt次
    for i in range(numIt):
        # 获取当前最佳单层决策树和相应错误率
        bestStump, error, classEst = bulidStump(dataArr,classLabels,D)
        # 输出当前权重
        # print D.T
        alpha = float(0.5*log((1.0-error) / max(error, 1e-16)))
        bestStump['alpha'] = alpha
        # 加入当前分类器到弱分类组中
        weakClassArr.append(bestStump)
        # print "classEst: ", classEst.T
        # 计算新的权重
        expon = multiply(-1*alpha*mat(classLabels).T, classEst)
        D = multiply(D, exp(expon))
        D = D / D.sum()
        aggClassEst += alpha * classEst
        # print  "aggClassEst: ", aggClassEst.T
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T, ones((m,1)))
        errorRate = aggErrors.sum() / m
        print "total error:", errorRate
        if errorRate == 0.0:break
    # return weakClassArr
    return weakClassArr, aggClassEst


def AdaClassify(datToClass, classFileArr):
    dataMat = mat(datToClass)
    m = shape(dataMat)[0]
    aggClassEst = mat(zeros((m,1)))
    for i in range(len(classFileArr)):
        classEst = stumpClassify(dataMat, classFileArr[i]['dim'], classFileArr[i]['thresh'], classFileArr[i]['ineq'])
        aggClassEst += classFileArr[i]['alpha'] * classEst
        print aggClassEst
    return sign(aggClassEst)


def loadDataSet(fileName):
    # 获取特征数
    numFeat = len(open(fileName).readline().split('\t'))
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat
# 第一个参数为分类器预测强度，第二个为类别
def plotROC(predStrengths, classLabels):
    import matplotlib.pyplot as plt
    cur = (1.0, 1.0)
    ySum = 0.0
    # 获取正确的类别数
    numPosClas = sum(array(classLabels) == 1.0)
    yStep = 1 / float(numPosClas)
    xStep = 1 / float(len(classLabels) - numPosClas)
    sortedIndicies = predStrengths.argsort()
    fig = plt.figure()
    fig.clf()
    ax = plt.subplot(111)
    for index in sortedIndicies.tolist()[0]:
        if classLabels[index] == 1.0:
            delx =0; delY = yStep;
        else:
            delx = xStep; delY = 0
            ySum  += cur[1]
        ax.plot([cur[0], cur[0] - delx], [cur[1], cur[1] - delY], C='b')
        cur = (cur[0] - delx, cur[1] -delY)
    ax.plot([0,1], [0,1],'b--')
    plt.xlabel('False positive rate'); plt.ylabel('true positive rate')
    plt.title('roc')
    print 'auc:', ySum * xStep
    plt.show()







