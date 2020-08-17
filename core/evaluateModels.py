from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from math import floor

class Module:

	pctPSSE = 0.9

	def AIC(self, p, model):
		return (2*p - 2*model.lnL())


	def PSSE(self, model, data):	# R array indexing is 1->N, whereas python 0->N-1
		n = len(data)
		k = max(floor(self.pctPSSE*n), 1)
		failNums = list(range(k+1,n+1))
		failTimes = data[-len(failNums):]
		mvfTab = [model.MVF(i) for i in failTimes]
		return sum((i - mvfTab[idx])**2 for idx, i in enumerate(failNums))


	def __init__(self):


		print('init tab 4')
