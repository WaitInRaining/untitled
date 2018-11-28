#!usr/bin/pytthon
# coding:utf-8

from numpy import *
def loadTrainData(fileName):
    data = zeros((944,1683))
    fr = open(fileName)
    for line in fr:
        curLine = line.strip().split('|')
        userId = int(curLine[0])
        movieId = int(curLine[1])
        ratting = int(curLine[2])
        # print userId, movieId,ratting
        data[userId, movieId] = ratting
    return data

# 原始的皮尔逊相似度
def pearsSim(inA, inB):
    if len(inA) <3 : return 1.0
    return corrcoef(inA, inB, rowvar=0)[0][1]
# 杰卡德-皮尔逊相似度
def jaccardPearSim(intA, intB):
    # 交集数
    intersectionNum = float(len(set(np.nonzero(intA)[0]) & set(np.nonzero(intB)[0])))
    if(intersectionNum) == 0:
        return 0.0
    # 并集数
    unionNum = float(len(set(np.nonzero(intA)[0]) | set(np.nonzero(intB)[0])))
    return intersectionNum / unionNum * corrcoef(intA, intB, rowvar=0)[0][1]

def pearSim(userA, userB):
    return  float(corrcoef(userA, userB,rowvar=0)[0][1])

# 师姐的皮尔逊相似度， 向量为行向量，列为电影id,平均评价次数，
def aPearSim(data ,userA, userB, avgRatingCount):
    # 求交集，返回电影id列表
    sim = set(nonzero(userA)[1]) & set(nonzero(userB)[1])
    # 交集数
    intersectionNum = float(len(sim))
    if (intersectionNum) == 0:
        return 0.0

    weight = intersectionNum / len(set(nonzero(userA)[1]))
    avgRatingA = sum([float(userA[0, item]) for item in sim]) / len(sim)
    avgRatingB = sum([float(userB[0, item]) for item in sim]) / len(sim)
    # *hotProductWeight(data, item, avgRatingCount)
    sumDiff = sum([(float(userA[0, item]) - avgRatingA) * (float(userB[0, item] - avgRatingB)
                                                           * hotProductWeight(data, item, avgRatingCount))for item in sim])
    if(sumDiff == 0):
        return 0.0
    sqrtSumA = sqrt(sum([pow(userA[0, item] - avgRatingA, 2) for item in sim]))
    sqrtSumB = sqrt(sum([pow(userB[0, item] - avgRatingB, 2) for item in sim]))
    # * hotProductWeight(data, item, avgRatingCount)
    # sumDiff = sum([(float(userA[0, item]) - avgRatingA) * (float(userB[0, item] - avgRatingB) ) for item in sim])
    return float(sumDiff / (sqrtSumA*sqrtSumB))*weight

# 杰卡德-皮尔逊相似度
def jaccPearSim(userA, userB):
    # 求交集，返回电影id列表
    sim = set(nonzero(userA)[1]) & set(nonzero(userB)[1])
    # 交集数
    intersectionNum = float(len(sim))
    if (intersectionNum) == 0:
        return 0.0

    weight = intersectionNum / len(set(nonzero(userA)[1]) | set(nonzero(userB)[1]))
    avgRatingA = sum([float(userA[0, item]) for item in sim]) / len(sim)
    avgRatingB = sum([float(userB[0, item]) for item in sim]) / len(sim)
    # *hotProductWeight(data, item, avgRatingCount)
    sumDiff = sum([(float(userA[0, item]) - avgRatingA) * (float(userB[0, item] - avgRatingB))for item in sim])
    if(sumDiff == 0):
        return 0.0
    sqrtSumA = sqrt(sum([pow(userA[0, item] - avgRatingA, 2) for item in sim]))
    sqrtSumB = sqrt(sum([pow(userB[0, item] - avgRatingB, 2) for item in sim]))
    # * hotProductWeight(data, item, avgRatingCount)
    # sumDiff = sum([(float(userA[0, item]) - avgRatingA) * (float(userB[0, item] - avgRatingB) ) for item in sim])
    return float(sumDiff / (sqrtSumA*sqrtSumB))*weight

def myPearSim(data,userA, userB):
    # 求交集，返回电影id列表
    sim = set(nonzero(userA)[1]) & set(nonzero(userB)[1])
    # 交集数
    intersectionNum = float(len(sim))
    if (intersectionNum) == 0:
        return 0.0
    weight = intersectionNum / sqrt( len(set(nonzero(userA)[1])) * len(set(nonzero(userB)[1])))
    avgRatingA = sum([float(userA[0, item]) for item in sim]) / len(sim)
    avgRatingB = sum([float(userB[0, item]) for item in sim]) / len(sim)
    # *hotProductWeight(data, item, avgRatingCount)
    sumDiff = sum([(float(userA[0, item]) - avgRatingA) * (float(userB[0, item] - avgRatingB)*getHotweight(data, item,userA[0, item] ))for item in sim])
    if(sumDiff == 0):
        return 0.0
    sqrtSumA = sqrt(sum([pow(userA[0, item] - avgRatingA, 2) for item in sim]))
    sqrtSumB = sqrt(sum([pow(userB[0, item] - avgRatingB, 2) for item in sim]))
    # * hotProductWeight(data, item, avgRatingCount)
    # sumDiff = sum([(float(userA[0, item]) - avgRatingA) * (float(userB[0, item] - avgRatingB) ) for item in sim])
    return float(sumDiff / (sqrtSumA*sqrtSumB))*weight

# 获取我的热门物品影响系数，用户-评分矩阵， 产品id，用户对该产品的评分
def  getHotweight(data, productId, userPre):
    sumRates = sum(data[:,productId])
    return pow(e, userPre / sumRates)


# data为一个矩阵,获取平均评价次数
def getAvgRatingCount(data):
    exist = (data >0) * 1.0
    # 获取1行，n列元素全为1的矩阵
    factor = ones((1,shape(data)[0]))
    return float(average(dot(factor, exist), 1))

# 获取该商品的评价次数，intA为列向量
def getRattingCount(intA):
    return float(len(nonzero(intA)[1]))

# 师姐的热门商品权重
def hotProductWeight(data, productId, avgRatingCount):
    count = getRattingCount(data[:,productId])
    if count <= 0.0:
        return 0.0
    return float(avgRatingCount / count)+1

# 获取用户对商品的平均评分 用户user的评分矩阵
def avgRating(user):
    # 获取列数
    colNum = shape(user)[1]
    factor = ones((colNum,1))
    sumRating = float(dot(user,factor))
    count =  float(len(nonzero(user)[1]))
    if(count == 0):
        return 0.0
    return sumRating / count

# 获取用户user对产品的预测评分，输入评分矩阵，相似度矩阵，最近相似用户，用户，产品
def getPreRate(data, userSims, userNN, user, product):
    # 计算用户的平均评分
    avgRate = avgRating(user)
    # 获取相似度的和
    simSum = 0.0
    diffSum = 0.0
    for index in userNN:
        simSum += userSims[0, index]
        rbp = data[index,product]
        rb = avgRating(data[index,:])
        simAB = userSims[0, index]
        diffSum  += simAB * (rbp - rb)
    if(diffSum == 0):
        return avgRate
    return avgRate + float(diffSum / simSum)



# 推荐方法：输入用户-项目矩阵，相似度方法，用户id,最近邻数目,preRate为预测的用户-项目评分矩阵
def recommend(data, simMeans, user, k, preRate):
    # 获取用户评分矩阵，并排序，取前k个作为近邻用户
    userSims = []
    # 获取所有用户数
    userNum = shape(data)[0]
    userSims = zeros((1, userNum))#初始化用户相似度矩阵
    # 获取所有商品的平均评价次数
    avgRatingCount = getAvgRatingCount(data)

    # 用户数从1开始，下标与用户id对应,
    for i in range(userNum):
        # 用户数从1开始
        if(i == 0):
            continue
        #  如果是当前用户则忽略
        if(i == user):
            continue
        # 肖宇航
        # userSims[0,i] = simMeans(data=data, userA=data[user,:], userB=data[i,:], avgRatingCount=avgRatingCount)
        # 原始的
        # userSims[0, i] = simMeans( userA=data[user, :], userB=data[i, :])
        # 我的
        userSims[0,i] = simMeans(data, userA=data[user,:], userB=data[i,:])

    # 取相似度最大的前K个用户的下标
    maxSim = 1.0 /max(userSims[0])
    userSims = userSims *maxSim
    usersNN  =  array(argsort(userSims)[0,userNum-k:userNum])
    # 获取用户没有评分的物品列表
    unratedItems = nonzero(data[user, :].A == 0)[1]
    if(len(unratedItems) == 0) :
        print "已评价全部商品"
        return []
    # 计算用户对物品的评分
    prelist = []
    avgRatingUser = avgRating(data[user,:])
    for index in unratedItems:
        if (index == 0):
            continue
        # 获取评价此物品的用户
        userIndex = nonzero(data[:,index])[0]
        userNeed = set(userIndex) & set(usersNN)
        if(len(userNeed) == 0):
            preRate[user,index] =avgRatingUser
        else:
            preRate[user,index] = getPreRate(data,userSims,userNeed,data[user,:],index)
        # prelist.append(preRate)
        # if(preRate[user, index] > 3):
        # print user, index , preRate[user, index]
    # print sort(prelist)

def getMEA(preRate, accRate):
    user = 1
    pre = array(nonzero(preRate[user, :]))[0]
    sum = 0.0
    count = len(pre)
    for index in pre:
        if (index < 273):
            sum += abs(float(preRate[user, index] - accRate[user, index]))
            # print index, float(preRate[user,index] - accRate[user,index])
    return float(sum / count)
    # accRateArr = array(accRate)
    # sum = 0.0
    # for user in accRateArr:
    #     userSum = 0.0
    #     count = len(user)
    #     if(count == 0):
    #         continue;
    #     for item in user:
    #         userSum += abs(float(preRate[user,item] - item))
    #     sum += userSum
    # return float(sum / len(accRateArr))

