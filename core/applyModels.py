'''
applyModels.py - view data as well as apply different
SRGMs, view and compare data plus show reliability growth

TODO: cache model results so that when they're toggled they don't re-calculate
'''

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
	modelPlotType = 'FT'
	modelShow = []
	modelDataOnPlot = True
	modelRelPlot = False
	modelRelInterval = 1000
	modelDataEnd = True
	modelData = {}
	modelActions = []


	def toggleModel(self, state):	# called every time a model is toggled via any of last 3 tabs
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

		self.updateQueryTable()
		self.plotModelTable()	# update model accuracy table (tab4)
		self.redrawModelPlot()


	def listModels(self):	# add all models dynamically to the menus

		menus = [self.menuViewAM, self.menuViewQ, self.menuViewE]	# menus and corresponding placeholder locations
		place = [self.actionModelPlaceholder, self.actionQueryPlaceholder, self.actionEvalPlaceholder]

		if self.curSheetName != None:
			return	# is called before setting cursheetname to only do once
		self.modelActions = []
		for midx in range(len(menus)):
			for idx, m in enumerate(self.modules):
				newAction = QtWidgets.QAction(self)
				newAction.setCheckable(True)
				newAction.setObjectName(f"actionShow{idx}")
				newAction.setText(f'Show {m.name}')
				self.modelActions.append(newAction)
				newAction.triggered.connect(self.toggleModel)
				menus[midx].insertAction(place[midx], newAction)
				self.modelButtons[midx+1].append(newAction)



	def redrawDataModelPlot(self):	#copied from tab 1 to save lot of frustration between drawing modes

		curSheet = self.curFileData[self.curSheetName]
		self.plotWindowModel.axes.clear()	# remove previous plot

		self.plotWindowModel.axes.grid(True)

		if self.modelPlotType == 'FT':	# plot selected curve type
			plotaxes = [curSheet['FT'], curSheet['FN']]
		elif self.modelPlotType == 'IF':
			plotaxes = [curSheet['FT'], curSheet['IF']]
		elif self.modelPlotType == 'FI':
			plotaxes = [curSheet['FT'], curSheet['FI']]

		print('plotting')
		if self.plotPtLines == 0:
			# points
			self.plotWindowModel.axes.plot(plotaxes[0], plotaxes[1],'.', label = 'Data')
		elif self.plotPtLines == 1:
			# lines
			self.plotWindowModel.axes.step(plotaxes[0], plotaxes[1], where='post', label = 'Data')
		elif self.plotPtLines == 2:
			# both
			dataplot = self.plotWindowModel.axes.step(plotaxes[0], plotaxes[1],'.-', where='post', label = 'Data')
			colorplot = self.plotWindowModel.axes.plot([0],[0],'.')	# old method was to plot pts and lines separately
			clr = colorplot[0].get_color()				# caused problems w/ legend, so to keep same appearance
			colorplot[0].remove()						# next plot color was taken and used
			dataplot[0].set_markerfacecolor(clr)
			dataplot[0].set_markeredgecolor(clr)

		self.plotWindowModel.draw()	# draw curves


	def redrawModelPlot(self):

		if self.curFileData == None:
			return	# file not open

		self.plotWindowModel.axes.clear()
		self.plotWindowModel.axes.grid(True)
		curSet = self.curFileData[self.curSheetName]['FT']	# keep track of FT as other plots also need time scale

		if self.modelRelPlot:
			plotTitle = f'{self.curSheetName} Reliability Plot @ {self.modelRelInterval} Length Interval'
		else:
			plotTitle = '{0} {1} vs Test Time'.format(self.curSheetName,
				['Cumulative Failures', 'Interfailure Times', 'Failure Intensity'][['FT','IF','FI'].index(self.modelPlotType)])

		if self.modelDataOnPlot and not self.modelRelPlot:
			self.redrawDataModelPlot()

		for model in self.modelShow:
			# if plot reliability growth do stuff
			if self.modelRelPlot:
				x, y = model.relGrowthPlot(self.modelRelInterval)
			else:
				model.predict(self.futureFailCount)
				x, y = model.MVFPlot() if self.modelPlotType == 'FT' else model.FIPlot() if self.modelPlotType == 'FI' else model.MTTFPlot()

			pL = '' if self.plotPtLines == 0 else '-' if self.plotPtLines == 1 else '--'
			pM = '.' if self.plotPtLines == 0 else None if self.plotPtLines == 1 else '.'
			self.plotWindowModel.axes.plot(x, y, linestyle=pL, marker = pM, label = model.name)

		if self.modelDataEnd:
			self.plotWindowModel.axes.axvline(curSet[len(curSet)-1],linestyle='--',color='k')

		#x1, x2 = self.plotWindowModel.axes.get_xlim()
		self.plotWindowModel.axes.set_xlim(right = curSet[len(curSet)-1] + self.futureFailTime)

		if len(self.modelShow) > 0:
			self.plotWindowModel.axes.legend(loc = 'best')

		self.plotWindowModel.axes.set_title(plotTitle)
		self.plotWindowModel.draw()


		curSheet = self.curFileData[self.curSheetName]
		self.modelTable.clear()		# re-add numeric data to table
		self.modelTable.setColumnCount(1 + (5 * len(self.modelShow)))
		self.modelTable.setRowCount(len(curSheet['FN']) + self.futureFailCount)

		
		modelLabels = ['FN']

		for i, fn in enumerate(curSheet['FN']):
			newfn = QtWidgets.QTableWidgetItem(str(fn))
			newfn.setFlags(newfn.flags() & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
			self.modelTable.setItem(i, 0, newfn)

		for midx, x in enumerate(self.modelShow):
			mdl = x.__class__.__name__
			modelLabels += [f'{mdl} Time', f'{mdl} FT', f'{mdl} IF', f'{mdl} FI', f'{mdl} Rel. Growth']

			for i, mvf in enumerate(x.MVFPlot()[0]):
				newMVF = QtWidgets.QTableWidgetItem(self.numfmt(mvf))
				newMVF.setFlags(newfn.flags())
				self.modelTable.setItem(i, 1 + 5*midx, newMVF)

			for i, cft in enumerate(x.MVFPlot()[1]):
				newCFT = QtWidgets.QTableWidgetItem(self.numfmt(cft))
				newCFT.setFlags(newfn.flags())
				self.modelTable.setItem(i, 2 + 5*midx, newCFT)

			for i, ift in enumerate(x.MTTFPlot()[1]):
				newIFT = QtWidgets.QTableWidgetItem(self.numfmt(ift))
				newIFT.setFlags(newfn.flags())
				self.modelTable.setItem(i, 3 + 5*midx, newIFT)

			for i, nfi in enumerate(x.FIPlot()[1]):
				newNFI = QtWidgets.QTableWidgetItem(self.numfmt(nfi))
				newNFI.setFlags(newfn.flags())
				self.modelTable.setItem(i, 4 + 5*midx, newNFI)

			for i, rel in enumerate(x.relGrowthPlot(self.modelRelInterval)[1]):
				newREL = QtWidgets.QTableWidgetItem(self.numfmt(rel))
				newREL.setFlags(newfn.flags())
				self.modelTable.setItem(i, 5 + 5*midx, newREL)

		for row in range(self.modelTable.rowCount()):	# fill empty cells so that they can't be edited
			for col in range(self.modelTable.columnCount()):
				if self.modelTable.item(row, col) == None:
					emptyItem = QtWidgets.QTableWidgetItem('')
					emptyItem.setFlags(newfn.flags())
					self.modelTable.setItem(row, col, emptyItem)

		self.modelTable.setHorizontalHeaderLabels(modelLabels)
		self.modelTable.resizeColumnsToContents()


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
			self.updateQueryTable()		# query table also predicts future N failures, share between tabs


	def setViewModel(self, viewNum):
		if viewNum < 3:
			self.modelPlotType = ['FT','IF','FI'][viewNum]

		self.modelRelPlot = (viewNum == 3)	# only appears on tab 2 so retain 1st tab functionality otherwise
		self.actionSelRel.setVisible(viewNum == 3)
		self.redrawModelPlot()
		print(f'set view type B to {viewNum}')


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
			self.updateQueryTable()	# parameter also saved with query table


	def __init__(self):

		self.actionSelFFC.triggered.connect(self.getFutureFailCount)
		self.actionSelFFD.triggered.connect(self.getFutureFailDur)

		self.actionShowPlotData.triggered.connect(lambda x: self.setModelDataView(0, x))
		self.actionShowPlotDataEnd.triggered.connect(lambda x: self.setModelDataView(1, x))

		self.plotWindowModel = MplCanvas(self, self.canvasDPI)
		self.gridLayout_6.addWidget(self.plotWindowModel, 0, 0, 1, 1)

		self.modelButtons = [[],[],[],[]]	# for storage for later setting model shortcuts dynamically
											# since 3 sets of model toggles, can only have 1 set of non-ambiguous shortcuts
											# must disable other 2 sets, have 4 menus for toggle in showMode since 4 tabs

		self.modelPlotGroup = QtWidgets.QActionGroup(self)
		self.modelPlotGroup.setExclusive(True)
		self.modelPlotGroup.addAction(self.actionCF_2)
		self.modelPlotGroup.addAction(self.actionTBF_2)
		self.modelPlotGroup.addAction(self.actionFI_2)
		self.modelPlotGroup.addAction(self.actionPlotRel)

		self.drawTypeGroup2 = QtWidgets.QActionGroup(self)
		self.drawTypeGroup2.setExclusive(True)
		self.drawTypeGroup2.addAction(self.actionPlot_Points_2)
		self.drawTypeGroup2.addAction(self.actionPlot_Lines_2)
		self.drawTypeGroup2.addAction(self.actionPlot_Both_2)

		self.actionPlot_Points_2.triggered.connect(lambda: self.setPlotTypeModels(0))
		self.actionPlot_Lines_2.triggered.connect(lambda: self.setPlotTypeModels(1))
		self.actionPlot_Both_2.triggered.connect(lambda: self.setPlotTypeModels(2))

		self.actionCF_2.triggered.connect(lambda: self.setViewModel(0))
		self.actionTBF_2.triggered.connect(lambda: self.setViewModel(1))
		self.actionFI_2.triggered.connect(lambda: self.setViewModel(2))
		self.actionPlotRel.triggered.connect(lambda: self.setViewModel(3))

		self.actionSelRel.triggered.connect(self.getRelInterval)
		
		print('init tab 2')