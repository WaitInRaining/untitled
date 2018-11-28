#!usr/bin/pytthon
# coding:utf-8

import  Recommend
import numpy as np
import  threading
import  thread
data = Recommend.loadTrainData("G://ml-100k//u1.base")
data = np.mat(data)

# sim =  Recommend.aPearSim(data, data[1,:], data[29,:], avgRatingCount)
#
# print sim
# print preRate
maes = []
preRate = np.zeros(np.shape(data))
testData = Recommend.loadTrainData("G://ml-100k//u1.test")
avgRatingCount = Recommend.getAvgRatingCount(data)

def run(m):
    for k in range(5):
        for i in range(943):
            Recommend.recommend(data, Recommend.myPearSim, i + 1, (k+ m + 1) * 10, preRate)
        mae = Recommend.getMEA(preRate, testData)
        print mae
        maes[k+m] = mae


# threads = []
# for i in range(5):
#     t = threading.Thread(target=run, args=(i,))
#     threads.append(t)
#
# for t in threads:
#     t.start()


for i in range(20):
    Recommend.recommend(data, Recommend.myPearSim, 1, (i + 1) * 10, preRate)
    mae = Recommend.getMEA(preRate, testData)
    print mae
    maes.append(mae)
print maes











# print data

# data = np.mat([[1,2,3,0,0,0,3],
#  [0, 0, 2, 0, 0, 0, 1]])
#
# print np.nonzero(data[:,0])[0]
# print np.nonzero(data[:,6])[0]

# print np.nonzero(data[0,:].A == 0)[1]
# print np.sort(data[0,:])
# print np.argsort(data[0,:])
# print np.array(np.argsort(data[0,:])[0,3:7])[0]
# avgRatingCount = Recommend.getAvgRatingCount(data)
# print  Recommend.getRattingCount(data[0,:])
# print Recommend.hotProductWeight(data, 0, avgRatingCount)
# print Recommend.aPearSim(userA=data[0, :], userB=data[1,:], data=data, avgRatingCount=avgRatingCount)
# x = np.mat([3,3])
# y = np.mat([2,1])
# print np.corrcoef(x, y, rowvar=0)[0][1]