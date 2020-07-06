from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import time

from models import DSS, GM, GO, ISS, JM, WEI
modules = [DSS.DSS, GM.GM, GO.GO, ISS.ISS, JM.JM, WEI.WEI]


class MplCanvas(FigureCanvasQTAgg):

	def __init__(self, parent=None, canvasDPI = 100):
		fig = Figure(figsize=(5, 4), dpi = canvasDPI)
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

	def toggleModel(self, state):
		if self.curFileData == None:
			return	# file not open

		index = int(self.sender().objectName()[10:])
		model = modules[index]
		if state:
			new = model(data=self.curFileData[self.curSheetName], rootAlgoName='newton')
			new.findParams(1)
			self.modelShow.append(new)
			self.statusBar.clearMessage()
		else:
			for m in self.modelShow:
				if type(m) == model:
					self.modelShow.remove(m)
		self.redrawModelPlot()

	def listModels(self):	# add all models dynamically to the menu
		for idx, m in enumerate(modules):
			newAction = QtWidgets.QAction(self)
			newAction.setCheckable(True)
			newAction.setObjectName(f"actionShow{idx}")
			newAction.setText(f'Show {m.name}')
			newAction.triggered.connect(self.toggleModel)
			self.menuViewAM.insertAction(self.actionModelPlaceholder, newAction)


	def redrawModelPlot(self):
		if self.curFileData == None:
			return	# file not open

		self.plotWindowModel.axes.clear()
		if self.modelDataOnPlot:
			self.redrawPlot(self.plotWindowModel)

		for model in self.modelShow:
			x = model.MVFPlot()[0]
			y = model.MVFPlot()[1]

			pL = None if self.plotPtLines == 0 else '-' if self.plotPtLines == 1 else '--'
			pM = '.' if self.plotPtLines == 0 else None if self.plotPtLines == 1 else '.'
			self.plotWindowModel.axes.plot(x, y, linestyle=pL, marker = pM, label = model.name)

		x1, x2 = self.plotWindowModel.axes.get_xlim()
		self.plotWindowModel.axes.set_xlim(right = x2 + self.futureFailTime)

		if self.modelDataEnd:
			curSet = self.curFileData[self.curSheetName][self.plotType]
			self.plotWindowModel.axes.axvline(curSet[len(curSet)-1],linestyle='--',color='k')

		self.plotWindowModel.axes.legend(loc = 'best')
		self.plotWindowModel.draw()

	def getFutureFailDur(self):
		text, ok = QtWidgets.QInputDialog.getInt(self,
					"Model Prediction",
					"Enter duration for model extension:",
					self.futureFailTime,
					0, 1000000, 1000 )
		if ok:
			self.futureFailTime = text
			self.redrawModelPlot()

	def getFutureFailCount(self):
		text, ok = QtWidgets.QInputDialog.getInt(self,
					"Model Prediction",
					"Enter number of predicted failures:",
					self.futureFailCount,
					1, 1000000, 1 )
		if ok:
			self.futureFailCount = text
			self.redrawModelPlot()

	def setModelDataView(self, typeID, val):
		if typeID == 0:
			self.modelDataOnPlot = val
		elif typeID == 1:
			self.modelDataEnd = val
		print('set plot param',typeID,'to',val)
		self.redrawModelPlot()

	def setPlotTypeModels(self, typeNum):
		self.plotPtLines = typeNum
		self.redrawModelPlot()
		print(f'set dot/line type to {typeNum}')



	def __init__(self):

		self.actionSelFFC.triggered.connect(self.getFutureFailCount)
		self.actionSelFFD.triggered.connect(self.getFutureFailDur)

		self.actionShowPlotData.triggered.connect(lambda x: self.setModelDataView(0, x))
		self.actionShowPlotDataEnd.triggered.connect(lambda x: self.setModelDataView(1, x))

		self.plotWindowModel = MplCanvas(self, self.canvasDPI)
		self.gridLayout_6.addWidget(self.plotWindowModel, 0, 0, 1, 1)

		self.actionPlot_Points_2.triggered.connect(lambda: self.setPlotTypeModels(0))
		self.actionPlot_Lines_2.triggered.connect(lambda: self.setPlotTypeModels(1))
		self.actionPlot_Both_2.triggered.connect(lambda: self.setPlotTypeModels(2))

		#self.actionRun_Models.triggered.connect(self.computeModels)

		self.listModels()

		print('init tab 2')