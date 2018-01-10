#!usr/bin/python
# coding:utf-8
import bayes
import re
import feedparser
# listOPosts, listClasses = bayes.loadDataSet()
# myVocablist = bayes.createVocabList(listOPosts)
# print myVocablist
# print bayes.setOfWords2Vec(myVocablist, listOPosts[0])


# trainMat = []
# for postinDoc in listOPosts:
#     trainMat.append(bayes.setOfWords2Vec(myVocablist, postinDoc))
# print  bayes.trainNB0(trainMat, listClasses)
# bayes.testingNB()

# mySent = 'This book is the best book on Python pr M.L. I have ever laid eyes upon.'
# regEx = re.compile('\\W*')
# listOfTokens = regEx.split(mySent)
# print listOfTokens
# bayes.spamTest()

ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
print len(ny['entries'])
sf = feedparser.parse('http://sfbay.craigslist.org/tsp/index.rss')
print len(sf['entries'])
vocabList, pSF, pNY = bayes.localWords(ny, sf)
