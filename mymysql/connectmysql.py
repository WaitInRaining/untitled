#!/usr/bin/python
# coding:utf-8

from numpy import *
import mysql.connector

import Similarity

config = {'host': 'localhost',
          'user':'root',
          'password':'',
          'port':'3306',
          'database':'movielens',
          'charset':'utf8'
          }
try:
 conn = mysql.connector.connect(**config)
except mysql.connector.Error as e:
    print 'connect failed!{}'.format(e)
cursor = conn.cursor()

try:
    query_movies = 'select MovieID from movies'
    cursor.execute(query_movies)
    #data = cursor.fetchall()
    # data = []
    movies=[]
    for movieid in cursor:
        # line=[movieid,title,genres.split('|')]
        # data.append(line)
        movies.append(movieid)
    # print len(data)

    query_users = 'select  UserID from users'
    cursor.execute(query_users)
    users=[]
    for userID in cursor:
        users.append(userID)

except mysql.connector.Error as e:
    print 'connect failed!{}'.format(e)

# print movies[-1][0], users[-1][0]
# 初始化用户-物品矩阵
dataMat = zeros((users[-1][0],movies[-1][0]))

try:
    query_ratings = "select UserID, MovieID,Rating from ratings"
    cursor.execute(query_ratings)
    for userid, movieid, rating in cursor:
        print userid-1, movieid-1, rating
        dataMat[userid-1, movieid-1]=rating

finally:
    cursor.close()
    conn.close()
#得到的是一个list,(编号， 评分)
print Similarity.userSimiliar(mat(dataMat), 1, Similarity.cosSim)




