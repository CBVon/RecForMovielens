#coding:utf-8
#!/usr/bin/env python  
#Filename:sortForFile 
'''
f=open('result.txt') 
a = f.readlines()
a = [x.split('\t') for x in a]  
a = [[x[0],x[1].replace('\n','')] for x in a] 
f.close() 
b = [[int(x[0]), int(x[1])] for x in a]  
b.sort()  
b = [str(x[0]) + '\t' + str(x[1]) + '\n' for x in b]
f=open('result.txt', "w")   
f.writelines(b)  
f.close()  
'''
import math
def getRmse():
    f1 = open('result.txt')
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
    rmse = math.sqrt(rmse)
    return rmse


#f = open('result.txt', "w+")
str = "RMSE is : "
#f.write(str)
#f.write(getRmse())
#print getRmse()
