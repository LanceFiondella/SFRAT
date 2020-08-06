from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from math import floor

class Module:

	pctPSSE = 0.9

	def AIC(self, p, model):
		return (2*p - 2*model.lnL())


	def PSSE(self, model, data):
		mvf = model.MVFVal	# includes predicted values
		n = len(data)
		k = max(floor(n*self.pctPSSE), 1)
		failN = list(range(k+1,n))	# inclusive n
		print(k,n)
		failT = data[k+1:]
		return sum((failT[index] - mvf[index])**2 for timeval in failN)


	def PSSE(self, model, data):
		n = len(data)
		k = max(floor(self.pctPSSE*n), 1)
		failNums = list(range(k,n))
		failTimes = data[-len(failNums):]
		mvfTab = [model.MVF(i) for i in failTimes]
		return sum((i - mvfTab[idx])**2 for idx, i in enumerate(failNums))


	def __init__(self):


		print('init tab 4')
