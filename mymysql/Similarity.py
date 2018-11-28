#!usr/bin/pytthon
# coding:utf-8

from numpy import *
# 已知用户物品矩阵为dataMat ，行为物品，列为用户

# 计算用户相似度
# -----------------
# 余弦相似度计算
# 欧式距离计算
def eulidSim(inA, inB):
    return 1.0 / (1.0 + linalg.norm(inA, inB))
# 皮尔逊系数计算
def pearsSim(inA, inB):
    if len(inA) <3 : return 1.0
    # 将值从[-1, 1]映射到[0, 1]
    return 0.5+0.5*corrcoef(inA, inB, rowvar=0)[0][1]
# 余弦相似度
def cosSim(inA, inB):
    num = float(inA*inB.T)
    denom = linalg.norm(inA) * linalg.norm(inB)
    # 将值从[-1, 1]映射到[0, 1]
    return 0.5 + 0.5 * (num / denom)

# 获取向量中非零元素的平均值
def avg(intA):
    return float(mean(intA[intA > 0], 1)[0][0])
# 基于用户相似度的推荐
# 数据矩阵，用户，相似度计算方法，物品
def userSimiliar(dataMat, user, simMeas, N = 5):
    userNum = shape(dataMat)[0] #获取所有用户数
    usersSim= zeros((1, userNum)) #用户相似度向量
    # 用户未评分的物品的下标
    unratedItems = nonzero(dataMat[user,:].A ==0)[1]
    unratedItemGrad = dict() #未评分物品的评分值
    unratedItemNum = dict() #根据其他用户，对未评分物品进行评分的次数

    # 用户i对商品的平均评分
    avgRate = avg(dataMat[user,:])
    for item in unratedItems:
        unratedItemNum[item] = 0
        unratedItemGrad[item] = 0
    for i in range(userNum):
        if i == user: continue
        # 获取用户相似度
        usersSim[0][i] = simMeas(dataMat[user,:], dataMat[i,:])#计算用户i和用户user的相似度
        #获取用户i评分但是用户user没有评分的物品的下标
        unratedItem = list(set(nonzero(logical_or(dataMat[user,:]>0, dataMat[i,:]>0))[1]) - set(nonzero(dataMat[user,:])[1]))
        if len(unratedItem) == 0 :continue #说明用户i所评分过的物品，用户User已评分过
        for item in unratedItem:
            # print unratedItemGrad[item],
            # print dataMat[i,item]
            unratedItemGrad[item] = unratedItemGrad[item]+ usersSim[0][i] * dataMat[i,item]
            unratedItemNum[item] =  unratedItemNum[item]+usersSim[0][i]

    for item in unratedItems:
        if unratedItemNum[item] == 0: continue
        unratedItemGrad[item] = unratedItemGrad[item] / unratedItemNum[item]
    recommand =  sorted(unratedItemGrad.items(), key=lambda jj:jj[1], reverse=True)
    recommandItems = list()
    for j in range(N):
        recommandItems.append(recommand[j])
    return recommandItems



# 基于物品相似度的推荐引擎
# 数据矩阵、用户、相似度计算方法、物品。行对应用户、列对应物品
def standEst(dataMat, user, simMeas, item):
    # 获取物品数
    n = shape(dataMat)[1]
    simTotal = 0.0; ratSimTotal = 0.0
    for j in range(n):
        # 获取用户对当前物品的评分
        userRating = dataMat[user,j]
        if userRating == 0: continue
        # 寻找对物品ITEM评分，且对当前物品有评分的用户
        # logical_and逻辑与计算，只有两个位置的都时真的时候才为真，此处计算共同对物品j和物品ITEM进行评分的用户
        # nonzeron返回非零元素的下标
        overLap = nonzero(logical_and(dataMat[:,item].A >0, dataMat[:,j].A >0))[0]
        if len(overLap) == 0: similarity = 0
        # 计算两列的相似度，即同一用户对item和j的评分的相似度
        else : similarity = simMeas(dataMat[overLap,item] , dataMat[overLap,j])
        # 获取总相似度
        simTotal += similarity
        # 获取用户总评价
        ratSimTotal += similarity * userRating
    if simTotal == 0: return 0
    else : return ratSimTotal/ simTotal


def recommend(dataMat, user, N=3, simMeas=cosSim, estMethod = standEst):
    # 获取用户没有评分的物品
    unratedItems = nonzero(dataMat[user,:].A == 0)
    if len(unratedItems) == 0: return 'you rated everything'
    itemScores = []
    # 填充用户对所有没有评分的物品的预测评分
    for item in unratedItems:
        estimatedScore = estMethod(dataMat, user, simMeas, item)
        itemScores.append((item, estimatedScore))
    #  根据评分对物品进行排序，返回Top-N
    return sorted(itemScores, key=lambda jj:jj[1], reverse=True)[:N]

def simBetweenUsers(dataMat, users, simMeas):
    # 初始化用户相似度矩阵
    simResult = zeros(((users[-1]+1), (users[-1]+1)))
    for user1 in users:
        for user2 in users:
            if(user1 != user2):
                simResult[user1][user2] = simMeas(dataMat[user1,:], dataMat[user2,:])
    return  simResult

