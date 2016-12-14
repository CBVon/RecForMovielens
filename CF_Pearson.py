#coding:utf-8
# ref : http://blog.csdn.net/database_zbye/article/details/8664516

import os
import time
from math import sqrt
from loadMovieLens import loadMovieLensTrain
from loadMovieLens import loadMovieLensTest
    
# compuer similarity(pearson) between person1, 2
def sim_pearson(prefer, person1, person2):
    sim = {}
    # find the comman item between person1, 2
    for item in prefer[person1]:
        if item in prefer[person2]:
            sim[item] = 1           # sim[] : used for saving comman item 
    n = len(sim)
    if len(sim)==0:
        return -1

    sum1 = sum([prefer[person1][item] for item in sim])  
    sum2 = sum([prefer[person2][item] for item in sim])  

    sum1Sq = sum( [pow(prefer[person1][item] ,2) for item in sim] )
    sum2Sq = sum( [pow(prefer[person2][item] ,2) for item in sim] )

    sumMulti = sum([prefer[person1][item]*prefer[person2][item] for item in sim])

    num1 = sumMulti - (sum1*sum2/n)
    num2 = sqrt( (sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))  
    if num2==0: 
        return 0  

    result = num1/num2
    return result


# get TopK similarity users compared to "person" for itemId   
def topKMatches(prefer, person, itemId, k=20, sim = sim_pearson):
    userSet = []
    scores = []
    users = []
    # userSet : saving users who has prefered item
    for user in prefer:
        if itemId in prefer[user]:
            userSet.append(user)

    scores = [(sim(prefer, person, other),other) for other in userSet if other!=person]
    scores.sort()
    scores.reverse()

    if len(scores)<=k:       
        for item in scores:
            users.append(item[1]) 
        return users
    else:                  
        kscore = scores[0:k]
        for item in kscore:
            users.append(item[1])  
        return users               


# get average prefer fro "userId"
def getAverage(prefer, userId):
    count = 0
    sum = 0
    for item in prefer[userId]:
        sum = sum + prefer[userId][item]
        count = count+1
    return sum/count


# use "weighted average strategy" to predict userId's prefer for itemID      
def getRating(prefer1, userId, itemId, knumber=20,similarity=sim_pearson):
    sim = 0.0
    averageOther =0.0
    jiaquanAverage = 0.0
    simSums = 0.0
    #  users for saving topK neighbour who has prefered  
    users = topKMatches(prefer1, userId, itemId, k=knumber, sim = sim_pearson)

    averageOfUser = getAverage(prefer1, userId)     

    # weighted average
    for other in users:
        sim = similarity(prefer1, userId, other) 
	simSums += abs(sim)    
        averageOther = getAverage(prefer1, other)      
        jiaquanAverage +=  (prefer1[other][itemId]-averageOther)*sim   

    # if(simSums == 0) : let other topK similar user's average be the return      
    if simSums==0:
        return averageOfUser
    else:
        return (averageOfUser + jiaquanAverage/simSums)  



# get all "prediction prefer" of users in testfile, and save it in "resultP.txt" 
def getAllUserRating(fileTrain='u1.base', fileTest='u1.test', fileResult='resultP.txt', similarity=sim_pearson):
    prefer1 = loadMovieLensTrain(fileTrain)         
    prefer2 = loadMovieLensTest(fileTest)            
    inAllnum = 0

    file = open(fileResult, 'a')
    #file.write("%s\n"%("------------------------------------------------------"))
    
    for userid in prefer2:             
        for item in prefer2[userid]:   
            rating = getRating(prefer1, userid, item, 20)   
            file.write('%s\t%s\t%s\n'%(userid, item, rating))
            inAllnum = inAllnum +1 
    file.close()
    print("-------------Completed!!-----------",inAllnum)

def f(a,b):
    return a-b

# sort "resultP.txt" by user_first, item_second
def sort():
    f=open('resultP.txt') 
    a = f.readlines()
    a = [x.split('\t') for x in a]  
    a = [[x[0],x[1],x[2].replace('\n','')] for x in a] 
    f.close() 
    b = [[int(x[0]), int(x[1]), float(x[2])] for x in a]  
    b.sort()  
    b = [str(x[0]) + '\t' + str(x[1]) + '\t' + str(x[2]) + '\n' for x in b]
    f=open('resultP.txt', "w")   
    f.writelines(b)  
    f.close()    

# get Rese between "resultP.txt" and real "u1.test"
def getRmse():
    f1 = open('resultP.txt')
    a1 = f1.readlines()
    a1 = [x.split('\t') for x in a1]
    b1 = [float(x[2].replace('\n','')) for x in a1]
    f2 = open('./movielens/u1.test')
    a2 = f2.readlines()
    a2 = [x.split('\t') for x in a2]
    b2 = [float(x[2].replace('\n','')) for x in a2]

    rmse = 0.0
    for x in range(len(b1)):
	#print b1[x]	
	rmse += (b1[x] - b2[x]) * (b1[x] - b2[x])
    rmse /= len(b1)
    rmse = sqrt(rmse)
    return rmse

if __name__ == "__main__":
    start = time.clock()
    print("\n--------------Movielens dataset——userbased CF(pearson)--------------\n")
    if os.path.exists('resultP.txt'):   	
	os.remove('resultP.txt')
    getAllUserRating('u1.base', 'u1.test', 'resultP.txt')
    sort()
    Rmse = getRmse()
    print("RMSE(pearson) is : ", Rmse)
    f = open('resultP.txt', "a+")
    f.write("RMSE(pearson) is : " + str(Rmse) + "\n")
    end = time.clock()
    print("Running time is : ", end - start)
    f.write("Running time is : " + str(end - start) + "\n")









