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
          'charset':'utf8',
          'buffered': True,
          }
try:
 conn = mysql.connector.connect(**config)
except mysql.connector.Error as e:
    print 'connect failed!{}'.format(e)
cursor = conn.cursor()

users = []
movies = []
try:
    query_movies = 'select movieid from movies'
    cursor.execute(query_movies)
    # data = cursor.fetchall()
    # data = []

    for movieid in cursor:
        # line=[movieid,title,genres.split('|')]
        # data.append(line)
        movies.append(movieid[0])
    # print len(data)

    query_users = 'select UserID from users'
    cursor.execute(query_users)

    for userID in cursor:
        users.append(userID[0])

except mysql.connector.Error as e:
    print 'connect failed!{}'.format(e)

# print movies[-1][0], users[-1][0]
# 初始化用户-物品矩阵
print users[-1], movies[-1]
dataMat = zeros((users[-1]+1,movies[-1]+1))

try:
    query_ratings = "select UserID, MovieID,Rating from ratings"
    cursor.execute(query_ratings)
    for userid, movieid, rating in cursor:
        # print userid, movieid, rating
        dataMat[userid, movieid]=rating
finally:
    cursor.close()
    conn.close()
#得到的是一个list,(编号， 评分)
# print Similarity.userSimiliar(mat(dataMat), 1, Similarity.cosSim)
result = Similarity.simBetweenUsers(mat(dataMat), users, Similarity.cosSim)
for user1 in users:
    for user2 in users:
        print user1, user2, result[user1, user2]



