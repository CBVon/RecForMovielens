import os
import time
from math import sqrt
from loadMovieLens import loadMovieLensTrain
from loadMovieLens import loadMovieLensTest
import pylab as pl
import matplotlib.pyplot as plt 

def CFdraw():
    #plt.figure()  

    f1 = open('resultO.txt')
    a1 = f1.readlines()
    a1 = [x.split('\t') for x in a1[0:20000]]
    b1 = [float(x[2].replace('\n','')) for x in a1]
    xx = []
    xx = range(len(b1))
    #x = range(len(self.arrRMSE_test))
    plt.scatter(xx, b1, label = 'resultO', color = 'black', s = 1)

    f2 = open('./movielens/u1.test')
    a2 = f2.readlines()
    a2 = [x.split('\t') for x in a2]
    b2 = [float(x[2]) for x in a2]
    #x = range(len(self.arrRMSE_test))
    plt.scatter(xx, b2, label = 'u1.test', color = 'r', s = 1)

    f3 = open('resultP.txt')
    a3 = f3.readlines()
    a3 = [x.split('\t') for x in a3[0:20000]]
    b3 = [float(x[2].replace('\n','')) for x in a3]
    #x = range(len(self.arrRMSE_test))
    plt.scatter(xx, b3, label = 'resultP', color = 'g', s = 1)

    plt.legend()
    #plt.show()
    plt.savefig('resultO&P.png')

if __name__ == "__main__":
    CFdraw()
