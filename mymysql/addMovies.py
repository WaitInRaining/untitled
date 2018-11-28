 # coding:utf-8

import mysql.connector

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
    file =  open("G:/movies.txt")
    movie = 0
    for i in file.readlines():
        lineStr = i.split(":")
        if(i == "" or len(i) == 1):
            break
        print i+str(len(i))+":111"
        movieID =int(lineStr[0])
        movie = movieID
        genres = lineStr[-1]
        title = "".join(lineStr[1:-1])
        insert_movie = "insert into newmovies(movieId, title, genres) values(%s,%s,%s)"
        cursor.execute(insert_movie,(movieID, title, genres))
    conn.commit()
except mysql.connector.Error as e:
    print 'connect failed!{}'.format(e)+movie
finally:
    cursor.close()
    conn.close()

