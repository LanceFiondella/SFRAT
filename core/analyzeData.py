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


	plotType = 'FT'
	plotPtLines = 2	# initial state both dots n lines
	plotLaplace = False
	plotLaplaceConf = 0.9
	plotArithAvg = False
	plotStartIndex = 0
	plotStopIndex = 0


	def redrawPlot(self, canvas):
		# draw plot
		if self.curFileData == None:
			return	# file not open
		curSheet = self.curFileData[self.curSheetName]
		canvas.axes.clear()

		if not self.plotLaplace:
			if self.plotType == 'FT':
				self.plotCurves[0] = [curSheet['FT'], curSheet['FN']]
			elif self.plotType == 'IF':
				self.plotCurves[0] = [curSheet['FT'], curSheet['IF']]
			elif self.plotType == 'FI':
				self.plotCurves[0] = [curSheet['FT'], curSheet['FI']]

		else:
			# plot laplace test
			if not self.plotArithAvg:
				laplace = [0]
				for i in range(1, len(curSheet['IF'])):
					sumint = 0
					for j in range(i):
						sumint += curSheet['FT'][j]
					laplace.append(((sumint/(i)) - (curSheet['FT'][i]/2)) / (curSheet['FT'][i] * (1/(12*(i))**0.5 )))
				self.plotCurves[0] = [list(range(len(laplace))), laplace]
			else:
				runAvg = []
				for i in range(len(curSheet['IF'])):
					s1 = 0
					for j in range(1+i):
						s1 += curSheet['IF'][j]
					runAvg.append(s1 / (i+1))
				self.plotCurves[0] = [list(range(len(runAvg))), runAvg]

		for plotaxes in self.plotCurves:
			print('plotting')
			if self.plotPtLines == 1 or self.plotPtLines == 2:
				canvas.axes.step(plotaxes[0][self.plotStartIndex:self.plotStopIndex],
							plotaxes[1][self.plotStartIndex:self.plotStopIndex], where='post')
			if self.plotPtLines == 0 or self.plotPtLines == 2:
				canvas.axes.plot(plotaxes[0][self.plotStartIndex:self.plotStopIndex],
							plotaxes[1][self.plotStartIndex:self.plotStopIndex],'.')

		canvas.draw()
		self.dataTable.clear()

		self.dataTable.setColumnCount(3)
		self.dataTable.setRowCount(len(curSheet['FN']))

		self.dataTable.setHorizontalHeaderLabels(['FN','IF',
			'Running Avg' if self.plotArithAvg else 'Laplace Statistic' if self.plotLaplace else 'FT'])


		for i in range(len(curSheet['FN'])):
			if self.plotLaplace:
				if self.plotArithAvg:
					num = runAvg[i]
				else:
					num = laplace[i]
			else:
				num = curSheet['FT'][i]

			newFN = QtWidgets.QTableWidgetItem(str(curSheet['FN'][i]))
			newIF = QtWidgets.QTableWidgetItem(str(curSheet['IF'][i]))
			newFT = QtWidgets.QTableWidgetItem(str(num))

			newFN.setFlags(newFN.flags() & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
			newIF.setFlags(newIF.flags() & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
			newFT.setFlags(newFT.flags() & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)

			self.dataTable.setItem(i, 0, newFN)
			self.dataTable.setItem(i, 1, newIF)
			self.dataTable.setItem(i, 2, newFT)


	def setView(self, viewNum):
		self.plotType = ['FT','IF','FI'][viewNum]
		self.redrawPlot(self.plotWindow)
		print(f'set view type to {self.plotType}')


	def setPlotType(self, typeNum):
		self.plotPtLines = typeNum
		self.redrawPlot(self.plotWindow)
		print(f'set dot/line type to {typeNum}')


	def laplaceToggle(self, en):
		self.plotLaplace = en
		self.redrawPlot(self.plotWindow)
		print('toggled laplace trend test')


	def arithToggle(self):
		self.plotArithAvg = not self.plotArithAvg
		self.plotLaplace = True
		self.actionTrendTest.setChecked(True)
		if self.plotArithAvg:
			self.actionPlotArith.setText('Plot: Toggle Laplace Test')
		else:
			self.actionPlotArith.setText('Plot: Arithmetic Average')
		self.redrawPlot(self.plotWindow)


	def laplaceQuery(self):
		text, ok = QtWidgets.QInputDialog.getDouble(self,
								"Laplace Trend Test",
								"Enter a confidence level:",
								self.plotLaplaceConf,
								0, 1, 2, QtCore.Qt.WindowFlags(), 0.01)
		if ok:
			self.plotLaplaceConf = text
			self.redrawPlot(self.plotWindow)
			print(f'set laplace conf to {text}')


	def rangeDialog(self, typ):
		if typ:
			text, ok = QtWidgets.QInputDialog.getInt(self,
						"Edit Range",
						f"Enter a start index",
						self.plotStartIndex, 
						0, max(len(self.curFileData[self.curSheetName]['IF']), self.plotStopIndex)
						)
		else:
			text, ok = QtWidgets.QInputDialog.getInt(self,
						"Edit Range",
						f"Enter a stop index",
						self.plotStopIndex, 
						max(self.plotStartIndex, 0), len(self.curFileData[self.curSheetName]['IF'])
						)
		if ok:
			if typ == True:
				self.plotStartIndex = text
				print(f'set start idx to {text}')
			else:
				self.plotStopIndex = text
				print(f'set stop idx to {text}')
			self.redrawPlot(self.plotWindow)



	def __init__(self):
		self.plotWindow = MplCanvas(self, width=1, height=1)
		self.gridLayout_2.addWidget(self.plotWindow, 0, 0, 1, 1)

		self.actionCF.triggered.connect(lambda: self.setView(0))
		self.actionTBF.triggered.connect(lambda: self.setView(1))
		self.actionFI.triggered.connect(lambda: self.setView(2))

		self.actionLapConf.triggered.connect(self.laplaceQuery)
		self.actionTrendTest.triggered.connect(self.laplaceToggle)
		self.actionPlotArith.triggered.connect(self.arithToggle)

		self.actionStartIndex.triggered.connect(lambda: self.rangeDialog(True))
		self.actionStopIndex.triggered.connect(lambda: self.rangeDialog(False))

		self.actionPlot_Points.triggered.connect(lambda: self.setPlotType(0))
		self.actionPlot_Lines.triggered.connect(lambda: self.setPlotType(1))
		self.actionPlot_Both.triggered.connect(lambda: self.setPlotType(2))

		self.showMode(0)
		self.actionAnalyzeData.triggered.connect(lambda: self.showMode(0))
		self.actionApplyModels.triggered.connect(lambda: self.showMode(1))
		self.actionModelResults.triggered.connect(lambda: self.showMode(2))
		self.actionEvaluateModels.triggered.connect(lambda: self.showMode(3))