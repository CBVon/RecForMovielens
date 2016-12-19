import pylab as pl
import numpy as np
import matplotlib.pyplot as plt

def drawPartResult(file, loc):
	f=open(file + ".txt")
	a = f.readlines()
	arrRMSE_test = []
	arrRMSE_train = []
	arrRMSE_test = [float(x.replace('\n','')) for x in a[0 : len(a) / 2]]
	arrRMSE_train = [float(x.replace('\n','')) for x in a[len(a) / 2 : len(a)]]
	'''
	pl.ion()
	x = range(len(arrRMSE_test))
	pl.plot(x, arrRMSE_test, label = 'RMSE_test')
	pl.plot(x, arrRMSE_train, label = 'RMSE_train')
	pl.legend()
	pl.show()
	pl.savefig('svd.result.png')
	'''
	 
	plt.subplot(loc)
	plt.title(file)
	plt.axis([0, len(arrRMSE_test), 0.7, 1.2])
	x = range(len(arrRMSE_test))
	plt.plot(x, arrRMSE_test, label = "RMSE_test")
	plt.plot(x, arrRMSE_train, label = "RMSE_train")
	plt.annotate(str(arrRMSE_test[len(arrRMSE_test) - 1]), xy=( len(arrRMSE_test) - 1 , arrRMSE_test[len(arrRMSE_test) - 1]))
	plt.annotate(str(arrRMSE_train[len(arrRMSE_train) - 1]), xy=( len(arrRMSE_train) - 1 , arrRMSE_train[len(arrRMSE_train) - 1]))
	plt.legend()
	#plt.savefig('svd.result.png')


if __name__=='__main__': 
	plt.figure(figsize=(16,4))
	drawPartResult('svd_init', 141)
	drawPartResult('svd', 142)
	drawPartResult('svd-train.82.k1', 143)
	drawPartResult('svd-train.78.grad', 144)
	plt.savefig('svd.result.png')
