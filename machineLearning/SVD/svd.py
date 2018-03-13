#!usr/bin/python
# coding:utf-8
from numpy import *

# 初始化用户-物品矩阵，行为用户，列为物品
def loadExDate():
    return [[1,1,1,0,0],
            [2,2,2,0,0],
            [1,1,1,0,0],
            [5,5,5,0,0],
            [1,1,0,2,2],
            [0,0,0,3,3],
            [0,0,0,1,1]]

# 相似度计算
# 欧式距离计算
def eulidSim(inA, inB):
    return 1.0 / (1.0 + linalg.norm(inA, inB))
# 皮尔逊系数计算
def pearsSim(inA, inB):
    if len(inA) <3 : return 1.0
    return 0.5+0.5*corrcoef(inA, inB, rowvar=0)[0][1]
# 余弦相似度
def cosSim(inA, inB):
    num = float(inA.T*inB)
    denom = linalg.norm(inA,) * linalg.norm(inB)
    return 0.5 + 0.5 * (num / denom)

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