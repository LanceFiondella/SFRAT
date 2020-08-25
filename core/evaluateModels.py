from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from math import floor

class Module:

	pctPSSE = 0.9

	def AIC(self, model):
		return (2*len(model.params) - 2*model.lnL())


	def PSSE(self, model, data):	# R array indexing is 1->N, whereas python 0->N-1
		n = len(data)
		k = max(floor(self.pctPSSE*n), 1)
		failNums = list(range(k+1,n+1))
		failTimes = data[-len(failNums):]
		mvfTab = [model.MVF(i) for i in failTimes]
		return sum((i - mvfTab[idx])**2 for idx, i in enumerate(failNums))

	def fisher(self, model=None, data=None):
		return 0

	def getPSSEpct(self):
		text, ok = QtWidgets.QInputDialog.getDouble(self,
								"PSSE Data Percentage",
								"Specify the percentage of data to use for PSSE:",
								self.pctPSSE,
								0, 1, 2, QtCore.Qt.WindowFlags(), 0.01)
		if ok:
			self.pctPSSE = text
			self.plotModelTable()
			print(f'set PSSE to {text*100}%')


	def plotModelTable(self):	# calculates AIC and PSSE for each model
								# called when a model is toggled (via applyModels)
		self.modelEvalTable.clear()
		self.modelEvalTable.setColumnCount(4)
		self.modelEvalTable.setRowCount(len(self.modelShow))
		self.modelEvalTable.setHorizontalHeaderLabels(['Model', 'AIC', f'PSSE {round(self.pctPSSE*100)}% Data', 'Fisher Information'])

		for idx, model in enumerate(self.modelShow):

			newMName = QtWidgets.QTableWidgetItem(model.name)
			newMAIC = QtWidgets.QTableWidgetItem(str(self.AIC(model)))
			newMPSSE = QtWidgets.QTableWidgetItem(str(self.PSSE(model, self.curFileData[self.curSheetName]['FT'])))
			newMfisher = QtWidgets.QTableWidgetItem(str(self.fisher()))

			newMName.setFlags(newMName.flags() & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
			newMAIC.setFlags(newMName.flags())
			newMfisher.setFlags(newMName.flags())
			newMPSSE.setFlags(newMName.flags())	# copy flags from first element

			self.modelEvalTable.setItem(idx, 0, newMName)
			self.modelEvalTable.setItem(idx, 1, newMAIC)
			self.modelEvalTable.setItem(idx, 2, newMPSSE)
			self.modelEvalTable.setItem(idx, 3, newMfisher)


		self.modelEvalTable.resizeColumnsToContents()
		print('re-evaluate model table')


	def __init__(self):

		self.actionPSSEpct.triggered.connect(self.getPSSEpct)
		self.plotModelTable()
		print('init tab 4')
