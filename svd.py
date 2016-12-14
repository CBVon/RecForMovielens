''''' 
ref : http://blog.csdn.net/daer520/article/details/19929523
'''  

import random  
import math  
import cPickle as pickle  
import pylab as pl

class SVD():  
    def __init__(self,allfile,trainfile,testfile,factorNum=5):  
        #all data file  
        self.allfile=allfile  
        #training set file  
        self.trainfile=trainfile  
        #testing set file  
        self.testfile=testfile  
        #get factor number  
        self.factorNum=factorNum  
        #get user number  
        self.userNum=self.getUserNum()  
        #get item number  
        self.itemNum=self.getItemNum()  
        #learning rate  
        self.learningRate=0.01  
        #the regularization lambda  
        self.regularization=0.05  
        #initialize the model and parameters  
        self.initModel()  
	self.arrRMSE_test = []
        self.arrRMSE_train = []

    #get user number function  
    def getUserNum(self):  
        file=self.allfile  
        cnt=0  
        userSet=set()  
        for line in open(file):  
            user=line.split('\t')[0].strip()  
            if user not in userSet:  
                userSet.add(user)  
                cnt+=1  
        return cnt  

    #get item number function  
    def getItemNum(self):  
        file=self.allfile  
        cnt=0  
        itemSet=set()  
        for line in open(file):  
            item=line.split('\t')[1].strip()  
            if item not in itemSet:  
                itemSet.add(item)  
                cnt+=1  
        return cnt  

    #initialize all parameters  
    def initModel(self):  
        self.av=self.average(self.trainfile)  
        self.bu=[0.0 for i in range(self.userNum)]  
        self.bi=[0.0 for i in range(self.itemNum)]  
        temp=math.sqrt(self.factorNum)  
        self.pu=[[(0.1*random.random()/temp) for i in range(self.factorNum)] for j in range(self.userNum)]  
        self.qi=[[(0.1*random.random()/temp) for i in range(self.factorNum)] for j in range(self.itemNum)]  
        print "Initialize end.The user number is:%d,item number is:%d,the average score is:%f" % (self.userNum,self.itemNum,self.av) 
 
    #train model    
    def train(self,iterTimes=100):  
        print "Beginning to train the model......"  
        trainfile=self.trainfile  
        preRmse=10000.0  
        for iter in range(iterTimes):  
            fi=open(trainfile,'r')  
            #read the training file  
            for line in fi:  
                content=line.split('\t')  
                user=int(content[0].strip())-1  
                item=int(content[1].strip())-1  
                rating=float(content[2].strip())  
                #calculate the predict score  
                pscore=self.predictScore(self.av,self.bu[user],self.bi[item],self.pu[user],self.qi[item])  
                #the delta between the real score and the predict score  
                eui=rating-pscore  
                  
                #update parameters bu and bi(user rating bais and item rating bais)  
                self.bu[user]+=self.learningRate*(eui-self.regularization*self.bu[user])  
                self.bi[item]+=self.learningRate*(eui-self.regularization*self.bi[item])  
                for k in range(self.factorNum):  
                    #temp=self.pu[user][k]  
                    #update pu,qi  
                    self.pu[user][k]+=self.learningRate*(eui*self.qi[user][k]-self.regularization*self.pu[user][k])  
                    self.qi[item][k]+=self.learningRate*(self.pu[user][k]*eui-self.regularization*self.qi[item][k])  
                #print pscore,eui  
            #close the file  
            fi.close()  
            #calculate the current rmse  
            curTestRmse=self.test(self.av,self.bu,self.bi,self.pu,self.qi,self.testfile)
	    curTrainRmse = self.test(self.av,self.bu,self.bi,self.pu,self.qi,self.trainfile)  
	    self.arrRMSE_test.append(curTestRmse)
	    self.arrRMSE_train.append(curTrainRmse)
	    print "Iteration %d times : " % (iter + 1)
            print "RMSE_test  is : %f" % (curTestRmse)  
	    print "RMSE_train is : %f" % (curTrainRmse)
            if curTrainRmse+0.001>preRmse:  
                break  
            else:  
                preRmse=curTrainRmse  
        print "Iteration finished!"  
	#print ("RMSE of test set is : " + s.test(self, ))

    #test on the test set and calculate the RMSE  
    def test(self,av,bu,bi,pu,qi,f):  
        #testfile=self.testfile  
        rmse=0.0  
        cnt=0  
        fi=open(f)  
        for line in fi:  
            cnt+=1  
            content=line.split('\t')  
            user=int(content[0].strip())-1  
            item=int(content[1].strip())-1  
            score=float(content[2].strip())  
            pscore=self.predictScore(av,bu[user],bi[item],pu[user],qi[item])  
            rmse+=math.pow(score-pscore,2)  
        fi.close()  
        return math.sqrt(rmse/cnt)  

    #calculate the average rating in the training set  
    def average(self,filename):  
        result=0.0  
        cnt=0  
        for line in open(filename):  
            cnt+=1  
            score=float(line.split('\t')[2].strip())  
            result+=score  
        return result/cnt  

    #calculate the inner product of two vectors  
    def innerProduct(self,v1,v2):  
        result=0.0  
        for i in range(len(v1)):  
            result+=v1[i]*v2[i]  
        return result  

    def predictScore(self,av,bu,bi,pu,qi):  
        pscore=av+bu+bi+self.innerProduct(pu,qi)  
        if pscore<1:  
            pscore=1  
        if pscore>5:  
            pscore=5  
        return pscore  

    def drawRmse(self):
	#pl.figure('svd.png')
	pl.ion()
	x = range(len(self.arrRMSE_test))
	pl.plot(x, self.arrRMSE_test, label = 'RMSE_test')
	pl.plot(x, self.arrRMSE_train, label = 'RMSE_train')
	pl.legend()
	pl.show()
	pl.savefig('svd.png')

if __name__=='__main__':  
    s=SVD("./movielens/u.data","./movielens/u1.base","./movielens/u1.test")  
    #print s.userNum,s.itemNum  
    #print s.average("data\\ua.base")  
    s.train() 
    s.drawRmse() 
    





