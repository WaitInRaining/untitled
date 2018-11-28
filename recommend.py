#!usr/bin/pytthon
# coding:utf-8
import numpy as np

a = [1,2,3,0,0,0,3]
b = [0,0,2,0,0,0,1]

data = np.mat([[1,2,3,0,0,0,3],
 [0, 0, 2, 0, 0, 0, 1]])

maxValue = 1.0 / np.max(data)
print data * maxValue

