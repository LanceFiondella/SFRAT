from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from math import floor

class Module:

	def AIC(self, p, lnL):
		return (2*p - 2*lnL)


	def PSSE(self, model, d, model_params, percent):
		t = 0
		n = len(d)
		k = max(floor(n*percent), 1)
		failN = list(range(k+1,n+1))	# inclusive n
		failT = d[-len(failN):]
		return 


	def __init__(self):


		print('init tab 4')


		'''
	sum(
			(failN[i] - model['MVF'])
		)


	sum(
		(failNums - get(paste(model,"_MVF_cont",sep="")) (model_params,failTimes))^2
		)
		'''