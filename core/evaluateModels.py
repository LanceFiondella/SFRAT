'''
evaluateModels.py - apply different score values to models
in order to quickly compare how well they work
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from math import floor

class Module:

	pctPSSE = 0.9

	def AIC(self, model):
		return (2*len(model.params) - 2*model.lnL())


	def PSSE(self, model, data):			# replaced with working version
		n = len(data)
		k = max(floor(self.pctPSSE*n), 1)	# get psse% of data as points, e.g. 90%

		fit_pts= data[:k]					# grab first 90% of points
		check_pts = data[k:]				# grab rest of points

		newmodel = model.__class__(data=fit_pts, rootAlgoName='bisect')
		newmodel.findParams(n-k)			# fit model to first chunk, predict rest 

		exp_fns = [newmodel.MVF(i) for i in check_pts['FT']]
		real_fns = list(check_pts['FN'])	#grab expected MVFs and known real MVFs for remaining time

		pssecalc = sum((exp_fns[i] - real_fns[i])**2 for i in range(len(exp_fns)))
											# calc SSE
		del newmodel	# delete model made for just this purpose
		return pssecalc

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
		self.modelEvalTable.setColumnCount(3)
		self.modelEvalTable.setRowCount(len(self.modelShow))
		self.modelEvalTable.setHorizontalHeaderLabels(['Model', 'AIC', f'PSSE {round(self.pctPSSE*100)}% Data'])

		for idx, model in enumerate(self.modelShow):

			newMName = QtWidgets.QTableWidgetItem(model.name)
			newMAIC = QtWidgets.QTableWidgetItem(self.numfmt(self.AIC(model)))
			newMPSSE = QtWidgets.QTableWidgetItem(self.numfmt(self.PSSE(model, self.curFileData[self.curSheetName])))

			newMName.setFlags(newMName.flags() & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
			newMAIC.setFlags(newMName.flags())
			newMPSSE.setFlags(newMName.flags())	# copy flags from first element

			self.modelEvalTable.setItem(idx, 0, newMName)
			self.modelEvalTable.setItem(idx, 1, newMAIC)
			self.modelEvalTable.setItem(idx, 2, newMPSSE)


		self.modelEvalTable.resizeColumnsToContents()
		print('re-evaluate model table')


	def __init__(self):

		self.actionPSSEpct.triggered.connect(self.getPSSEpct)
		print('init tab 4')
