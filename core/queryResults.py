'''
queryResults.py - creates numeric data of predictive model
results to estimate future numeric values and store them
in a table that can be exported by the user
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from scipy.optimize import root

class Module:

	additionalRuntime = 4000
	desiredReliability = 0.9


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


	def updateQueryTable(self):	# generate the table of values

		self.queryTable.clear()
		self.queryTable.setColumnCount(5)
		self.queryTable.setRowCount(len(self.modelShow) * self.futureFailCount)
					# tables seem to act weird when setting row count after, so estimate it high and reduce later
		
		self.queryTable.setHorizontalHeaderLabels(
			['Model',
			f'Time for R = {self.desiredReliability}\n(mission length {self.modelRelInterval})',
			f'Failures for next\n{self.additionalRuntime} time units',
			'Failure\nNumber',
			f'Expected Time\nUntil Failure N'
			])

		rowIndex = 0
		modelDisplayFlags = [False for x in self.modelShow]	# only show predictive results once

		for midx, model in enumerate(self.modelShow):

			if modelDisplayFlags[midx] == False:
				modelDisplayFlags[midx] = True

				x0 = self.curFileData[self.curSheetName]['FT'].iloc[-1]
				time_to = root(
					lambda t: self.desiredReliability - model.reliability(t, self.modelRelInterval), [x0])
				if time_to.success:
					result = self.numfmt( (time_to.x[0] - x0) ) if (time_to.x[0] - x0 > 0) else "Achieved"
				else:
					result = "Unavailable"

				resnum = model.MVF(x0 + self.additionalRuntime) - model.MVF(x0)

			else:
				result = ""	# don't repeatedly show result
				resnum = ""

			for failnum in range(self.futureFailCount):

				model.predict(failnum + 1)	# python range is 0 to N
				mvfs = model.MVFPlot()[0]

				newMName = QtWidgets.QTableWidgetItem(failnum == 0 and model.name or '')
				newTTo = QtWidgets.QTableWidgetItem(failnum == 0 and result or '')
				newNumF = QtWidgets.QTableWidgetItem(failnum == 0 and self.numfmt(resnum))
				newNth = QtWidgets.QTableWidgetItem(str(len(mvfs)))
				newTTN = QtWidgets.QTableWidgetItem(self.numfmt(mvfs[-1] - mvfs[len(self.curFileData[self.curSheetName]['FT'])-1]))

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

				if(failnum > 0 and (str(len(mvfs)) == self.queryTable.item(rowIndex-1, 3).text())):	
					break	# if this row is a duplicate of the last one, let it be overwritten

				rowIndex += 1
				if(len(mvfs) < (failnum + 1 + len(self.curFileData[self.curSheetName]['FT']))):	# if mvf count is less than expected, there are no more predicted
					break

		self.queryTable.setRowCount(rowIndex)
		self.queryTable.resizeColumnsToContents()
		print('re-evaluate query table')

	def __init__(self):

		self.actionSpecFC.triggered.connect(self.getFutureFailCount)	# will keep solid between 
		self.actionSpecRuntime.triggered.connect(self.getRuntime)
		self.actionDesRel.triggered.connect(self.getReliability)
		self.actionSpecRelInt.triggered.connect(self.getRelInterval)
		print('init tab 3')
