from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)

class Module:

	futureFailCount = 1
	futureFailTime = 1000
	modelShow = []
	modelDataOnPlot = True
	modelDataEnd = True
	modelPlotType = 'FT'
	modelData = {}

	def computeModels():
		return	

	def redrawModelPlot():
		if self.curFileData == None:
			return	# file not open

		self.redrawPlot

	def getFutureFailDur(self):
		text, ok = QtWidgets.QInputDialog.getInt(self,
					"Model Prediction",
					"Enter duration for model extension:",
					self.futureFailTime,
					0, 1000000, 1000 )
		if ok:
			self.futureFailTime = text
			self.redrawModelPlot(self.plotWindowModel)

	def getFutureFailCount(self):
		text, ok = QtWidgets.QInputDialog.getInt(self,
					"Model Prediction",
					"Enter number of predicted failures:",
					self.futureFailCount,
					1, 1000000, 1 )
		if ok:
			self.futureFailCount = text
			self.redrawModelPlot(self.plotWindowModel)

	def setModelDataView(self, typeID, val):
		if typeID == 0:
			self.modelDataOnPlot = val
			print(val)
		elif typeID == 1:
			self.modelDataEnd = val



	def __init__(self):

		self.actionSelFFC.triggered.connect(self.getFutureFailCount)
		self.actionSelFFD.triggered.connect(self.getFutureFailDur)

		self.actionShowPlotData.triggered.connect(lambda x: self.setModelDataView(0, x))

		self.plotWindowModel = MplCanvas(self, width=1, height=1)
		self.gridLayout_6.addWidget(self.plotWindowModel, 0, 0, 1, 1)