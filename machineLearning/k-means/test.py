#!usr/bin/python
# coding:utf-8

import kmeans
import matplotlib.pyplot as plt
from numpy import *
# print kmeans.random.rand(5,1)
dataSet = mat(kmeans.loadDataSet('testSet2.txt'))
# kmeans聚类
# centroids, clusterAssment = kmeans.kmeans(dataSet, 3)

# 二分均值聚类
centroids, clusterAssment = kmeans.biKmeans(dataSet,3)
print centroids
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dataSet[:,0].flatten().A[0], dataSet[:,1].flatten().A[0],s=2,c='red')
ax.scatter(centroids[:,0].flatten().A[0], centroids[:,1].flatten().A[0], s = 5, c='green')

plt.show()
