#!/usr/bin/python
# coding:utf-8
"""
   这是注释！
"""
# 这他妈也是注释？？
# 程序入口在哪？为毛可以直接运行？
import sys
import math
from numpy import *
import operator
import datetime

# print random.rand(3,4)
# randMat = mat(random.rand(4,4))
# print randMat
# print randMat.I # 矩阵的逆
# invRandMat = randMat.I
# print randMat*invRandMat
# print randMat*invRandMat - eye(4)

# print eye(2,3)
# print "git"

# dataMat = zeros((3,4))
# dataMat = mat([[1,2,3],
#                [2,3,4],
#                [3,4,5]])
# print dataMat
# a =  dataMat[[0,2],1]
# print a.A>3
# print a
# print linalg.norm(dataMat[:,1])
#
# print dataMat


# a = array([0,1,2,3,0,0])
# b = array([1,2,0,0,0,1])
# print list(set(nonzero(logical_or(a[:]>0, b[:]>0))[0]) - set(nonzero(a)[0]))
# print nonzero(a)[0]


# a =list([1,2,3,4])
# b=dict()
# for i in a :
#     b[i]= 5-i
#
# c =  sorted(b.items(), key=lambda j :j[1], reverse=True)
# d = list()
# for e in c:
#     d.append(e[0])
# print d

# def cosSim(inA, inB):
#     num = float(inA*inB.T)
#     denom = linalg.norm(inA) * linalg.norm(inB)
#     return 0.5 + 0.5 * (num / denom)
#
# inA = mat(array([1,2,3]))
# inB= mat(array([0,3,9]))
#
# print cosSim(inA, inB)
#
# for i in range(5):
#     print i

# dataMat = mat([[1,2,3],
#                [2,3,4],
#                [3,4,5]])
# data = mat([[2,2,2],
#            [2,2,2],
#            [2,2,2]])
# print dataMat[0,1]
# print linalg.norm(data[0,:])
# print dataMat / data

# a= full((2,3), 2)
# print a
# a[1,2]=99
# print  a
# t = array([[ 3. , 1.,  2.],
#             [ 5. , 4., 7]])
# print t
# print mean(a)
# print average(a)
# print ptp(a)
# print median(t)
# print sort(t,1)
# print var(t)
# print std(t)
# print diff(a)
# print log(e)
# print where(t >0)
# print t / a
# index=[0,1,2,3,4]
# print take(t, index)
# print  argmax(t,axis=1)
# print argmin(t)
# print maximum(a,t)
# print minimum(a,t)
# #convolve()
# print  ravel(t)
# # print split(t,3)
# print sys.argv[0]
# r = arange(5)
# s = exp(r)
# print exp(2)
# print linspace(1,8,3)
# print t.sum()
# t.fill(3)
# print t
# print dot(t,a.T)
# print ones_like(a)
# print zeros_like(a)
# print vstack((a,t))
# print intersect1d(t,r)
# print t.clip(1,2)
# r = array([1,2,5,7,9])
# print r.compress(r >2)
# print r.prod()
# print r.cumprod()
# print t.diagonal()
# print t.trace()
# print corrcoef(a,t)
# p=polyfit(index,r,4)
# print p
# print polyval(p, 90)
# print polyder(p)
# print roots(p)
# l = array([-1,-0.23, 9, 7,-965])
# print sign(l)
# print sign(t)
# print piecewise(l,[l<0,l>0], [-1,1])
# vectorize()
# print hanning()
# print isreal(t)
# print datetime.datetime.strptime("2016-08-23","%Y-%m-%d").date().weekday()

# b = loadtxt("save.txt", delimiter=" ")
# # savetxt("save.txt", b)
# print  b
# c = eye(3,4,3)
# print c

# a  = [i for i in range(10)]
# print len(a)
# print a[0:int(len(a)*0.8)]
# print a[int(len(a)*0.8):len(a)]
a1 =1;
a2 =2
a = (a1,a2,3,4)
print a
