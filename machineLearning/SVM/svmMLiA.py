#!usr/bin/python
# coding:utf-8
from numpy import *
def loadDataSet(filename):
    dataMat = []; labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[-1]))
    return dataMat, labelMat

# i为alpha的下标，m是所有alpha的数目，随机选择一个与i不等的j
def selectJrand(i, m):
    j = i
    while (j == i):
        j = int(random.uniform(0, m))
    return j
# 调整大于H，小于L的alpha值
def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj
# 输入为数据集，类别标签，惩罚因子常数c,松弛变量(在 0-1之间)，退出前最大循环次数
def smoSimple(dataMatIn, classLabels, c, toler, maxIter):
    dataMatrix =  mat(dataMatIn); labelMat = mat(classLabels).transpose()
    b = 0; m, n = shape(dataMatrix)
    alpha = mat(zeros((m,1)))
    iter = 0
    while(iter < maxIter):
        alphaParisChanged = 0
        for i in range(m):
            # g(x) = wx+b = (a1x1y1+a2x2y1+...+anxnyn)X +b,w不能  multiply是内积
            fxi = float(multiply(alpha,labelMat).T * (dataMatrix * dataMatrix[i, :].T)) +b
            Ei = fxi - float(labelMat[i]) # 误差值？？ wxi+b - yi
            # yi(wx +b) >= 1- c加入松弛变量后，alpha的限制为约束条件
            if((labelMat[i] * Ei < -toler) and (alpha[i] < c)) or ((alpha[i] > 0) and (labelMat[i] * Ei > toler)):
                j = selectJrand(i,m) # 随机选取一个j做匹配
                fxj = float(multiply(alpha, labelMat).T * (dataMatrix * dataMatrix[j,:].T )) + b
                Ej = fxj - float(labelMat[j])
                alphaIold = alpha[i].copy()
                alphaJold = alpha[j].copy()
                # 保证alpha在0-c之间
                if(labelMat[i] != labelMat[j]):
                    L = max(0, alpha[j] - alpha[i])
                    H = min(c, c + alpha[j] - alpha[i])
                else :
                    L = max(0, alpha[j] + alpha[i] - c)
                    H = min(c, alpha[j] + alpha[i])
                if L == H : print 'L==H';continue

                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0 : print 'eta >= 0';continue
                alpha[j] -= labelMat[j]*(Ei - Ej)/eta
                alpha[j] = clipAlpha(alpha[j], H, L)
                if (abs(alpha[j] - alphaJold < 0.00001)): print 'j not moving enough'; continue
                alpha[i] += labelMat[j]*labelMat[i]*(alphaJold - alpha[j])
                b1 = b - Ei - labelMat[i] * (alpha[i] -alphaIold) \
                              *dataMatrix[i,:]*dataMatrix[i,:].T-labelMat[j]*(alpha[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[   j,:].T
                b2 = b - Ej - labelMat[i] * (alpha[i]-alphaIold)\
                              *dataMatrix[i,:]*dataMatrix[j,:].T-labelMat[j]*(alpha[j]-alphaIold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0 < alpha[i]) and (c > alpha[i]): b = b1
                elif (0 < alpha[j]) and (c > alpha[j]): b = b2
                else:
                    b = (b1 + b2) / 2.0
                alphaParisChanged +=1
                print "iter: %d i:%d, pairs changed %d" % (iter, i ,alphaParisChanged)
        if(alphaParisChanged == 0): iter+=1
        else : iter = 0
        print "iteration number: %d" %iter
    return b, alpha


# 写的不对，，最后两步不知道咋写
def plotLine(dataMat, classLables, weight, b):
    import matplotlib.pyplot as plt
    dataMatix = array(dataMat)
    n = shape(dataMatix)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(classLables[i]) == 1:
            xcord1.append(dataMatix[i,0])
            ycord1.append(dataMatix[i,1])
        if int(classLables[i]) == -1:
            xcord2.append(dataMatix[i,0])
            ycord2.append(dataMatix[i,1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s = 30, c = 'red', marker='s')
    ax.scatter(xcord2, ycord2, s = 30)
    x = arange(-2,12,0.14)
    y =  weight * x.T +b[0][0]
    ax.plot(x,y)
    plt.xlabel('X1');plt.ylabel('x2')
    plt.show()


# 建立一个数据结构来保存所有的重要值
class optStruct:
    def __init__(self, dataMatIn, classLabels, C, toler,kTup):
        self.X = dataMatIn
        self.lableMat = classLabels
        self.C = C
        self.tol = toler
        self.m = shape(dataMatIn)[0]
        self.alpha = mat(zeros((self.m,1)))
        self.b = 0
        # 第一列给出eCache是否有效的标志位，第二列给出实际的E值
        self.eCache = mat(zeros((self.m, 2)))
        self.K = mat(zeros((self.m, self.m)))
        for i in range(self.m):
            self.K[:,i] = KernalTrans(self.X, self.X[i,:],kTup)

def calcEk(oS, k):
    fxk = float(multiply(oS.alpha, oS.lableMat).T * oS.K[:,k] +oS.b)
    Ek = fxk - float(oS.lableMat[k])
    return Ek
def selectJ(i, oS, Ei):
    maxK = -1; maxDeltaE = 0; Ej = 0
    oS.eCache[i] = [1,Ei]
    validEcacheList = nonzero(oS.eCache[:,0].A)[0]
    if (len(validEcacheList)) > 1:
        for k in validEcacheList:
            if k == i : continue
            Ek = calcEk(oS, k)
            deltaE = abs(Ei - Ek)
            if (deltaE > maxDeltaE):
                maxK = k; maxDeltaE = deltaE; Ej = Ek
        return maxK, Ej
    else :
        j = selectJrand(i, oS.m)
        Ej = calcEk(oS, j)
    return j ,Ej

# 计算误差并存入缓存
def updateEk(oS, k):
    Ek = calcEk(oS, k)
    oS.eCache[k] = [1, Ek]

def innerL(i, oS):
    Ei =calcEk(oS, i)
    if((oS.lableMat[i] * Ei < -oS.tol) and (oS.alpha[i] < oS.C)) or\
        ((oS.lableMat[i] * Ei >oS.tol) and (oS.alpha[i] > 0)):
        j, Ej = selectJ(i, oS, Ei)
        alphaIold = oS.alpha[i].copy(); alphaJold = oS.alpha[j].copy();
        if(oS.lableMat[i] != oS.lableMat[j]):
            L = max(0, oS.alpha[j] - oS.alpha[i])
            H = min(oS.C, oS.C + oS.alpha[j] - oS.alpha[i])
        else:
            L = max(0, oS.alpha[j] + oS.alpha[i] - oS.C)
            H = min(oS.C, oS.alpha[j] + oS.alpha[i])

        if L == H : print "L == H";return 0;
        # eta = 2.0 * oS.X[i,:]*oS.X[j,:].T - oS.X[i,:]*oS.X[i,:].T - oS.X[j,:]*oS.X[j,:].T
        # 使用核函数
        eta = 2.0 * oS.K[i,j] - oS.K[i,i] - oS.K[j,j]
        if eta >= 0: print "eta >=0";return 0
        oS.alpha[j] -=  oS.lableMat[j] *(Ei - Ej) / eta
        oS.alpha[j] = clipAlpha(oS.alpha[j], H, L)
        updateEk(oS, j)
        if (abs(oS.alpha[j] - alphaJold) < 0.00001):
            print "J not moving enough"; return 0
        oS.alpha[i] += oS.lableMat[j] * oS.lableMat[i] * (alphaJold - oS.alpha[j])
        updateEk(oS, i)
        # b1 = oS.b - Ei - oS.lableMat[i]*(oS.alpha[i] - alphaIold)* oS.X[i,:]*oS.X[i,:].T - oS.lableMat[j]*\
        #     (oS.alpha[j] - alphaJold)*oS.X[i,:]*oS.X[j,:].T
        # b2 = oS.b - Ej - oS.lableMat[i]*(oS.alpha[i] - alphaIold)* oS.X[i,:]*oS.X[i,:].T - oS.lableMat[j]*\
        #     (oS.alpha[j] - alphaJold)*oS.X[j,:]*oS.X[j,:].T
        # 使用核函数
        b1 = oS.b - Ei - oS.lableMat[i]*(oS.alpha[i] - alphaIold)*oS.K[i,i] - oS.lableMat[j]*(oS.alpha[j]-alphaJold)*oS.K[i,j]
        b2 = oS.b - Ej - oS.lableMat[i]*(oS.alpha[i] - alphaIold)*oS.K[i,j] - oS.lableMat[j]*(oS.alpha[j]-alphaJold)*oS.K[j,j]
        if (0 < oS.alpha[i]) and (oS.C > oS.alpha[i]) : oS.b = b1
        elif (0 < oS.alpha[j]) and (oS.C > oS.alpha[j]): oS.b = b2
        else :
            oS.b = (b1 + b2) / 2.0
        return 1
    else:
        return 0
# 完整版外循环
def smoP(dataMatIn, classLables, C, toler, maxIter, kTup = ('lin', 0)):
    oS = optStruct(mat(dataMatIn), mat(classLables).transpose(), C, toler, kTup)
    iter = 0;
    entireSet = True;alphaPairsChanged = 0
    while(iter < maxIter) and  ((alphaPairsChanged >0) or entireSet):
        alphaPairsChanged = 0
        if entireSet:
            for i in range(oS.m):
                alphaPairsChanged += innerL(i ,oS)
                print "fullSet, iter: %d i %d, pairs changed %d" % (iter, i, alphaPairsChanged)
            iter += 1
        else:
            nonBoundIs = nonzero((oS.alpha.A > 0) * (oS.alpha.A < C))[0]
            for i in nonBoundIs:
                alphaPairsChanged += innerL(i, oS)
                print 'non-bound, iter: %d i %d,paris changed %d' % (iter, i, alphaPairsChanged)
            iter += 1
        if entireSet : entireSet = False
        elif (alphaPairsChanged == 0): entireSet = True
        print 'iteration number: %d ' % iter
    return oS.b, oS.alpha

def calcWs(alphas, dataArr, classLabels):
   X = mat(dataArr); labelMat = mat(classLabels).transpose()
   m, n = shape(X)
   w = zeros((n,1))
   for i in range(m):
       w += multiply(alphas[i] * labelMat[i], X[i,:].T)
   return w

def KernalTrans(X,A,kTup):
    m,n = shape(X)
    K = mat(zeros((m,1)))
    # 线性核函数
    if kTup[0] == 'lin': K = X * A.T
    # 径向基核
    elif kTup[0] == 'rbf':
        for j in range(m):
            deltaRow = X[j,:] - A
            K[j] = deltaRow * deltaRow.T
        K = exp( K / (-1*kTup[1] **2))
    else : raise NameError('Houston We Have a problem That Kernal is not recognized')
    return K

def testRbf(k1 = 1.3):
    dataArr, labelArr = loadDataSet('testSetRBF.txt')
    b ,alphas = smoP(dataArr, labelArr, 200, 0.0001, 10000, ('rbf', k1))
    dataMat = mat(dataArr); labelmat = mat(labelArr).transpose()
    svInd = nonzero(alphas.A > 0)[0]
    # 构建支撑向量矩阵
    sVs = dataMat[svInd]
    labelSV = labelmat[svInd];
    print "有%d个支撑向量" % shape(sVs)[0]
    m,n = shape(dataMat)
    errorCount = 0
    for i in range(m):
        kerbelEval = KernalTrans(sVs, dataMat[i,:],('rbf', k1))
        predict = kerbelEval.T * multiply(labelSV, alphas[svInd]) + b
        # sign(x) = sgn(x)
        if sign(predict) != sign(labelArr[i]): errorCount += 1
    print "错误率为%f" % (float(errorCount)/m)
    dataArr,labelArr = loadDataSet('testSetRBF2.txt')
    errorCount = 0
    dataMat = mat(dataArr); labelmat = mat(labelArr).transpose()
    m,n = shape(dataArr)
    for i in range(m):
        kerbelEval = KernalTrans(sVs, dataMat[i,:],('rbf', k1))
        predict = kerbelEval.T * multiply(labelSV, alphas[svInd]) +b
        if sign(predict) != sign(labelArr[i]): errorCount +=1
    print "错误率为：%f" % (float(errorCount)/m)

# Svm进行手写数字识别
# 将文本表示的图像转化为向量
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        linestr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(linestr[j])
    return returnVect

def loadImages(dirName):
    from os import listdir
    hwLabels  = [];
    trainingFileList = listdir(dirName)
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileName = trainingFileList[i]
        fileStr = fileName.split(".")[0]
        classNumStr = int(fileStr.split('_')[0])
        if classNumStr == 9: hwLabels.append(-1)
        else: hwLabels.append(1)
        trainingMat[i:] = img2vector('%s/%s' % (dirName, fileName))
    return trainingMat, hwLabels

def testDigits(kTup = ('rbf',10)):
    dataArr, labelArr = loadImages('trainingDigits')
    b, alphas = smoP(dataArr, labelArr,200,0.0001,10000,kTup)
    datMat = mat(dataArr); labMat = mat(labelArr).transpose()
    svInd = nonzero(alphas.A > 0)[0]
    sVs = datMat[svInd]
    labelSV = labMat[svInd]
    print "有%d个支持向量" % shape(sVs)[0]
    m,n = shape(datMat)
    errorCount = 0;
    for i in range(m):
        kernelEval = KernalTrans(sVs,datMat[i,:],kTup)
        predict = kernelEval.T * multiply(labelSV, alphas[svInd]) +b
        if sign(predict) != sign(labelArr[i]) : errorCount +=1
    print "训练集错误率为 %f" % (float(errorCount) / m)
    dataArr, labelArr = loadImages('testDigits')
    errorCount = 0;
    dataMat = mat(dataArr); labMat = mat(labelArr).transpose()
    m,n = shape(dataArr)
    for i in range(m):
        kernelEval = KernalTrans(sVs, dataMat[i,:],kTup)
        predict = kernelEval.T * multiply(labelSV, alphas[svInd]) +b
        predict = kernelEval.T * multiply(labelSV, alphas[svInd]) + b
        if sign(predict) != sign(labelArr[i]): errorCount += 1
    print "测试集错误率为 %f" % (float(errorCount) / m)











