from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog

class Module:

	observeFailureCount = 1
	additionalRuntime = 4000
	desiredReliability = 0.9
	reliabilityInterval = 4000


	def getFailureCount(self):
		text, ok = QtWidgets.QInputDialog.getInt(self,
								"Failure Count",
								"Specify the number of failures to be observed:",
								self.observeFailureCount,
								1)
		if ok:
			self.observeFailureCount = text
			self.updateQueryTable()
			print(f'set observed failures to {text}')


	def getRuntime(self):
		text, ok = QtWidgets.QInputDialog.getInt(self,
								"Runtime",
								"Specify the additional duration for which the software will run:",
								self.additionalRuntime,
								1) # no maximum
		if ok:
			self.additionalRuntime = text
			self.updateQueryTable()
			print(f'set runtime to {text}')


	def getReliability(self):
		text, ok = QtWidgets.QInputDialog.getDouble(self,
								"Desired Reliability",
								"Specify the desired reliability:",
								self.desiredReliability,
								0, 1, 2, QtCore.Qt.WindowFlags(), 0.01)
		if ok:
			self.desiredReliability = text
			self.updateQueryTable()
			print(f'set des. rel. to {text}')


	def getInterval(self):
		text, ok = QtWidgets.QInputDialog.getInt(self,
								"Reliability Interval",
								"Specify the interval used to compute reliability:",
								self.reliabilityInterval,
								1) # no maximum
		if ok:
			self.reliabilityInterval = text
			self.updateQueryTable()
			print(f'set rel. interval to {text}')


	def updateQueryTable(self):
		self.queryTable.clear()
		self.queryTable.setColumnCount(5)
		self.queryTable.setRowCount(10) # figure this out later
		self.queryTable.setHorizontalHeaderLabels(
			['Model',
			f'Time until R = {self.desiredReliability}, mission length {self.reliabilityInterval}',
			f'Failures of next {self.additionalRuntime} time units',
			'Failure Number',
			f'Time until next {observeFailureCount} failures'
			])

		self.queryTable.resizeColumnsToContents()

	def __init__(self):

		self.actionSpecFC.triggered.connect(self.getFailureCount)
		self.actionSpecRuntime.triggered.connect(self.getRuntime)
		self.actionDesRel.triggered.connect(self.getReliability)
		self.actionSpecRelInt.triggered.connect(self.getInterval)
		print('init tab 3')
