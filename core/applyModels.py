from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import time


class MplCanvas(FigureCanvasQTAgg):

	def __init__(self, parent=None, canvasDPI = 100):
		fig = Figure(figsize=(5, 4), dpi = canvasDPI)
		self.axes = fig.add_subplot(111)
		self.axes.grid(True)
		self.figureref = fig
		super(MplCanvas, self).__init__(fig)

class Module:

	futureFailCount = 1
	futureFailTime = 1000
	modelShow = []
	modelDataOnPlot = True
	modelRelPlot = False
	modelRelInterval = 1000
	modelDataEnd = True
	modelData = {}
	modelActions = []

	def toggleModel(self, state):
		if self.curFileData == None:
			self.sender().setChecked(False)
			return	# file not open

		index = int(self.sender().objectName()[10:])#everything after "actionShow"
		model = self.modules[index]

		if state:
			new = model(data=self.curFileData[self.curSheetName], rootAlgoName='bisect')
			new.findParams(1)
			self.statusBar.clearMessage()

			if new.converged == False:
				qm = QtWidgets.QMessageBox
				ret = qm.question(self,'', "The model did not find a correct fit solution. This will likely result in an inaccurate curve. Would you still like to evaluate it?", qm.Yes | qm.No)
				if ret == qm.No:
					self.sender().setChecked(False)
					return

			self.modelShow.append(new)

		else:
			for m in self.modelShow:
				if type(m) == model:
					#print('remove',m)
					self.modelShow.remove(m)

		# assumes model toggle succeeded past this point

		for checkBox in self.modelActions:	# update checked status between menus
			if checkBox.objectName()[10:] == str(index):	# index match so model match
				checkBox.setChecked(state)

		self.plotModelTable()	# update model accuracy table (tab4)
		self.redrawModelPlot()

	def listModels(self):	# add all models dynamically to the menus

		menus = [self.menuViewAM, self.menuViewQ, self.menuViewE]	# menus and corresponding placeholder locations
		place = [self.actionModelPlaceholder, self.actionQueryPlaceholder, self.actionEvalPlaceholder]

		if self.curSheetName != None:
			return	# is called before setting cursheetname to only do once
		for midx in range(len(menus)):
			for idx, m in enumerate(self.modules):
				newAction = QtWidgets.QAction(self)
				newAction.setCheckable(True)
				newAction.setObjectName(f"actionShow{idx}")
				newAction.setText(f'Show {m.name}')
				self.modelActions.append(newAction)
				newAction.triggered.connect(self.toggleModel)
				menus[midx].insertAction(place[midx], newAction)

	def redrawModelPlot(self):

		if self.curFileData == None:
			return	# file not open

		self.plotWindowModel.axes.clear()
		self.plotWindowModel.axes.grid(True)

		if self.modelDataOnPlot and not self.modelRelPlot:
			self.redrawPlot(self.plotWindowModel, legend=True)

		for model in self.modelShow:
			# if plot reliability growth do stuff
			if self.modelRelPlot:
				x, y = model.relGrowthPlot(self.modelRelInterval)
			else:
				x, y = model.MVFPlot() if self.plotType == 'FT' else model.FIPlot() if self.plotType == 'FI' else model.MTTFPlot()

			pL = '' if self.plotPtLines == 0 else '-' if self.plotPtLines == 1 else '--'
			pM = '.' if self.plotPtLines == 0 else None if self.plotPtLines == 1 else '.'
			self.plotWindowModel.axes.plot(x, y, linestyle=pL, marker = pM, label = model.name)

		x1, x2 = self.plotWindowModel.axes.get_xlim()
		self.plotWindowModel.axes.set_xlim(right = x2 + self.futureFailTime)

		if self.modelDataEnd:
			curSet = self.curFileData[self.curSheetName][self.plotType]
			self.plotWindowModel.axes.axvline(curSet[len(curSet)-1],linestyle='--',color='k')

		if len(self.modelShow) > 0:
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

	def setPlotTypeModels(self, typeNum, rec = 0):
		self.plotPtLines = typeNum
		if rec == 0:
			self.setPlotType(typeNum, 1)
		for i, option in enumerate([self.actionPlot_Points_2, self.actionPlot_Lines_2, self.actionPlot_Both_2]):
			option.setChecked(i == typeNum)
		self.redrawModelPlot()
		print(f'set dot/line type 1 to {typeNum}')

	def getRelInterval(self):
		text, ok = QtWidgets.QInputDialog.getInt(self,
					"Reliability Interval",
					"Enter interval for model reliability plot:",
					self.modelRelInterval,
					0, 1000000000, 1 )
		if ok:
			self.modelRelInterval = text
			self.redrawModelPlot()

	def __init__(self):

		self.actionSelFFC.triggered.connect(self.getFutureFailCount)
		self.actionSelFFD.triggered.connect(self.getFutureFailDur)

		self.actionShowPlotData.triggered.connect(lambda x: self.setModelDataView(0, x))
		self.actionShowPlotDataEnd.triggered.connect(lambda x: self.setModelDataView(1, x))

		self.plotWindowModel = MplCanvas(self, self.canvasDPI)
		self.gridLayout_6.addWidget(self.plotWindowModel, 0, 0, 1, 1)

		self.drawTypeGroup2 = QtWidgets.QActionGroup(self)
		self.drawTypeGroup2.setExclusive(True)
		self.drawTypeGroup2.addAction(self.actionPlot_Points_2)
		self.drawTypeGroup2.addAction(self.actionPlot_Lines_2)
		self.drawTypeGroup2.addAction(self.actionPlot_Both_2)

		self.actionPlot_Points_2.triggered.connect(lambda: self.setPlotTypeModels(0))
		self.actionPlot_Lines_2.triggered.connect(lambda: self.setPlotTypeModels(1))
		self.actionPlot_Both_2.triggered.connect(lambda: self.setPlotTypeModels(2))

		self.actionCF_2.triggered.connect(lambda: self.setView(0))
		self.actionTBF_2.triggered.connect(lambda: self.setView(1))
		self.actionFI_2.triggered.connect(lambda: self.setView(2))
		self.actionPlotRel.triggered.connect(lambda: self.setView(3))

		self.actionSelRel.triggered.connect(self.getRelInterval)
		
		print('init tab 2')