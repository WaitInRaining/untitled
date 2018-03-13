#!usr/bin/python
#coding:utf-8

import svd

data = svd.loadExDate()
U, sigma, VT = svd.linalg.svd(data)

sig3 = svd.mat([[sigma[0],0,0], [0, sigma[1], 0], [0,0,sigma[2]]])
print  U[:,:3] *sig3 * VT[:3,:]