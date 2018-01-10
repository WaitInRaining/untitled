#!/usr/bin/python
# coding:utf-8
import sys
import math

# import first
# # list排序
# list = [1,8,5,7,9,9,9]
# print list
# list.sort()
# print list
# print list.count(9)
# print len(list)

# 可以输入表达式，但是在输入字符串的时候需要用""括起来
# l = input("请输入：")
# print l
"哈哈哈"
# print (list,l)
l= list(range(5))
print
l = [1,2,3,4,5]
k = [2,3,4,5,6,7,8]

for x,y in zip(l,k):
    print x ,y ,"--",x+y
j = list(zip(l,k))
print j
j = list(map(ord,'spafwusgfvu'))
print j

# 文件
f = open("E:/1.txt")
s = f.readlines()
for i in s :
    a = i.split(",")
    print a
for i in l :
    k.append(i)

print k
print sum(l)
print max(k)
h = ["2","3"]
print max(h)
r  =range(10)
print r
i = iter(r)
print i
def multipy(x,y= 3 ):
    print x,y

X = 1;
Y = [1,2]


multipy(x=X);

dic = {'key1':1, 'key2' : 2}
print list(dic.keys())
for i in dic :
    print dic[i]

def f(**args) :
    print args
f(a =1, b =2)

def f(*agrs) : print agrs
f(1,2,3,0,4)

def func(a,b,c,d):
    print  a,b,c,d
l = [1,2,3,4]
func(*(1,2),**{'c':3,'d':4})

def fun(a,b):
    a[0] =5
    b = 2
c = 1
fun(l[:],c)
print l,c
def mysum(L):
   return 0 if not L else L[0] + mysum(L[1:])
print mysum(l)

def funn(a):
    b = 'spam'
    return b*a
print funn(8)
print funn.__name__
# print dir(funn)
funn.cout = 1;
print funn.cout

def knights():
    ti = 'str'
    action = (lambda x: ti +' '+x)
    return action
act = knights()
print act('heihei')
print list(range(-5,5))
print list(filter((lambda x:x>0),range(-5,5)))

def fun(x):
    for i in x:
     if(i % 2) :
        return i
c = fun()
print filter(c,[1,2,3,4])