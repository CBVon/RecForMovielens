#coding:utf-8
import sys
import os

def loadMovieLensTrain(fileName='u1.base'):
    str1 = './movielens/'                         
    
    prefer = {}
    for line in open(str1+fileName,'r'):      
        (userid, movieid, rating,ts) = line.split('\t')    
        prefer.setdefault(userid, {})      
        prefer[userid][movieid] = float(rating)    

    return prefer      # {'user1':{itemid:rating, itemid2:rating, ,,}, {,,,}}

def loadMovieLensTest(fileName='u1.test'):
    str1 = './movielens/'    
    prefer = {}
    for line in open(str1+fileName,'r'):    
        (userid, movieid, rating,ts) = line.split('\t')   
        prefer.setdefault(userid, {})  
	#print (userid + " " + movieid + " " + rating)  
        prefer[userid][movieid] = float(rating)   
    return prefer                   


if __name__ == "__main__":
    print ("""This part could test the above 2 funcs!!""")
    
    trainDict = loadMovieLensTrain()
    testDict = loadMovieLensTest()

    print (len(trainDict))
    print (len(testDict))
    #print (testDict)
    print ("""Test pass!!! """)
                        

















