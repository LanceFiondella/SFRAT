'''
queryResults.py - creates numeric data of predictive model
results to estimate future numeric values and store them
in a table that can be exported by the user
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from scipy.optimize import root

class Module:

	observeFailureCount = 1
	additionalRuntime = 4000
	desiredReliability = 0.9
	reliabilityInterval = 4000


	def getFailureCount(self): # parse user input for the desired future failures
		text, ok = QtWidgets.QInputDialog.getInt(self,
								"Failure Count",
								"Specify the number of failures to be observed:",
								self.observeFailureCount,
								1)
		if ok:
			self.observeFailureCount = text
			self.updateQueryTable()
			print(f'set observed failures to {text}')


	def getRuntime(self):	# parse for desired additional software runtime
		text, ok = QtWidgets.QInputDialog.getInt(self,
								"Runtime",
								"Specify the additional duration for which the software will run:",
								self.additionalRuntime,
								1) # no maximum
		if ok:
			self.additionalRuntime = text
			self.updateQueryTable()
			print(f'set runtime to {text}')


	def getReliability(self):	# get desired reliability value
		text, ok = QtWidgets.QInputDialog.getDouble(self,
								"Desired Reliability",
								"Specify the desired reliability:",
								self.desiredReliability,
								0, 1, 2, QtCore.Qt.WindowFlags(), 0.01)
		if ok:
			self.desiredReliability = text
			self.updateQueryTable()
			print(f'set des. rel. to {text}')


	def getInterval(self):	# get the computable interval for reliability
		text, ok = QtWidgets.QInputDialog.getInt(self,
								"Reliability Interval",
								"Specify the interval used to compute reliability:",
								self.reliabilityInterval,
								1) # no maximum
		if ok:
			self.reliabilityInterval = text
			self.updateQueryTable()
			print(f'set rel. interval to {text}')


	def updateQueryTable(self):	# generate the table of values

		self.queryTable.clear()
		self.queryTable.setColumnCount(5)
		self.queryTable.setRowCount(len(self.modelShow) * self.observeFailureCount)
					# tables seem to act weird when setting row count after, so estimate it high and reduce later
		
		self.queryTable.setHorizontalHeaderLabels(
			['Model',
			f'Time for R = {self.desiredReliability}\n(mission length {self.reliabilityInterval})',
			f'Failures for next\n{self.additionalRuntime} time units',
			'Failure\nNumber',
			f'Expected\nTime Until'
			])

		rowIndex = 0
		modelDisplayFlags = [False for x in self.modelShow]	# only show predictive results once

		for midx, model in enumerate(self.modelShow):

			if modelDisplayFlags[midx] == False:
				modelDisplayFlags[midx] = True

				x0 = self.curFileData[self.curSheetName]['FT'].iloc[-1]
				time_to = root(
					lambda t: self.desiredReliability - model.reliability(t, self.reliabilityInterval), [x0])
				if time_to.success:
					result = str(time_to.x[0] - x0) if (time_to.x[0] - x0 > 0) else "Achieved"
				else:
					result = "Unavailable"

				resnum = str(model.MVF(x0 + self.additionalRuntime) - model.MVF(x0))

			else:
				result = ""	# don't repeatedly show result
				resnum = ""

			for failnum in range(self.observeFailureCount):

				model.predict(failnum + 1)	# python range is 0 to N
				mvfs = model.MVFPlot()[0]

				newMName = QtWidgets.QTableWidgetItem(failnum == 0 and model.name or '')
				newTTo = QtWidgets.QTableWidgetItem(failnum == 0 and result or '')
				newNumF = QtWidgets.QTableWidgetItem(failnum == 0 and resnum)
				newNth = QtWidgets.QTableWidgetItem(str(len(mvfs)))
				newTTN = QtWidgets.QTableWidgetItem(str(mvfs[-1] - mvfs[len(self.curFileData[self.curSheetName]['FT'])-1]))

				newMName.setFlags(newMName.flags() & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
				newNth.setFlags(newMName.flags())
				newNumF.setFlags(newMName.flags())
				newTTo.setFlags(newMName.flags())
				newTTN.setFlags(newMName.flags())

				self.queryTable.setItem(rowIndex, 0, newMName)
				self.queryTable.setItem(rowIndex, 1, newTTo)
				self.queryTable.setItem(rowIndex, 2, newNumF)
				self.queryTable.setItem(rowIndex, 3, newNth)
				self.queryTable.setItem(rowIndex, 4, newTTN)

				rowIndex += 1
				if(len(mvfs) < (failnum + 1 + len(self.curFileData[self.curSheetName]['FT']))):	# if mvf count is less than expected, there are no more predicted
					break

		self.queryTable.setRowCount(rowIndex)
		self.queryTable.resizeColumnsToContents()

	def __init__(self):

		self.actionSpecFC.triggered.connect(self.getFailureCount)
		self.actionSpecRuntime.triggered.connect(self.getRuntime)
		self.actionDesRel.triggered.connect(self.getReliability)
		self.actionSpecRelInt.triggered.connect(self.getInterval)

		self.updateQueryTable()

		print('init tab 3')
