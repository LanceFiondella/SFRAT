from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog

from scipy.stats import norm

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

	def __init__(self, parent=None, canvasDPI = 100):
		fig = Figure(figsize=(5, 4), dpi = canvasDPI)
		self.axes = fig.add_subplot(111)
		self.axes.grid(True)
		self.figureref = fig
		super(MplCanvas, self).__init__(fig)

class Module:


	plotType = 'FT'			# tab 1 and 2 plot style
	plotPtLines = 2			# initial state both dots n lines
	plotLaplace = False		# show laplace / arith toggle
	plotLaplaceConf = 0.9
	plotArithAvg = False
	plotStartIndex = 0		# for custom plot windowing
	plotStopIndex = 0


	def redrawPlot(self, canvas, legend=False):
		# draw plot on tab 1, has canvas and legend params for tab 2 usage

		if self.curFileData == None:
			return		# file not open, do nothing

		curSheet = self.curFileData[self.curSheetName]
		canvas.axes.clear()	# remove previous plot

		canvas.axes.grid(True)

		if not self.plotLaplace:
			if self.plotType == 'FT':	# plot selected curve type
				self.plotCurves[0] = [curSheet['FT'], curSheet['FN']]
			elif self.plotType == 'IF':
				self.plotCurves[0] = [curSheet['FT'], curSheet['IF']]
			elif self.plotType == 'FI':
				self.plotCurves[0] = [curSheet['FT'], curSheet['FI']]

		else:
			# plot laplace test or arith avg, calculate values (adapted from R code)
			if not self.plotArithAvg:
				lapConf = norm.ppf(1 - self.plotLaplaceConf)	#qnorm
				print(lapConf)
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

											# plot curves
		for plotaxes in self.plotCurves:	# implemented with multiple plot in mind, never used
			print('plotting')
			if self.plotPtLines == 0:
				# points
				canvas.axes.plot(plotaxes[0][self.plotStartIndex:self.plotStopIndex],
							plotaxes[1][self.plotStartIndex:self.plotStopIndex],'.', label = 'Data')
			elif self.plotPtLines == 1:
				# lines
				canvas.axes.step(plotaxes[0][self.plotStartIndex:self.plotStopIndex],
							plotaxes[1][self.plotStartIndex:self.plotStopIndex], where='post', label = 'Data')
			elif self.plotPtLines == 2:
				# both
				dataplot = canvas.axes.step(plotaxes[0][self.plotStartIndex:self.plotStopIndex],
							plotaxes[1][self.plotStartIndex:self.plotStopIndex],'.-', where='post', label = 'Data')
				colorplot = canvas.axes.plot([0],[0],'.')	# old method was to plot pts and lines separately
				clr = colorplot[0].get_color()				# caused problems w/ legend, so to keep same appearance
				colorplot[0].remove()						# next plot color was taken and used
				dataplot[0].set_markerfacecolor(clr)
				dataplot[0].set_markeredgecolor(clr)

		if self.plotLaplace and not self.plotArithAvg:	# plot laplace, need to plot after due to plot limits
			canvas.axes.axhline(lapConf,linestyle='--',color='r')

		canvas.draw()	# draw curves
		
		self.dataTable.clear()		# re-add numeric data to table
		self.dataTable.setColumnCount(3)
		self.dataTable.setRowCount(len(curSheet['FN']))
		self.dataTable.setHorizontalHeaderLabels(['FN','IF',
			'Running Avg' if self.plotArithAvg else 'Laplace Statistic' if self.plotLaplace else 'FT'])


		for i in range(len(curSheet['FN'])):	# make new table entries
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

		self.dataTable.resizeColumnsToContents()


	def setView(self, viewNum):
		if viewNum < 3:
			self.plotType = ['FT','IF','FI'][viewNum]
		self.modelRelPlot = (viewNum == 3)	# only appears on tab 2 so retain 1st tab functionality otherwise
		self.redrawPlot(self.plotWindow)
		self.redrawModelPlot()
		print(f'set view type to {self.plotType}')


	def setPlotType(self, typeNum, rec = 0):
		self.plotPtLines = typeNum
		if rec == 0:
			self.setPlotTypeModels(typeNum, 1)
		for i, option in enumerate([self.actionPlot_Points, self.actionPlot_Lines, self.actionPlot_Both]):
			option.setChecked(i == typeNum)
		self.redrawPlot(self.plotWindow)
		print(f'set dot/line type 2 to {typeNum}')


	def laplaceToggle(self, en):
		self.plotLaplace = en
		self.redrawPlot(self.plotWindow)
		print('toggled laplace trend test')


	def arithToggle(self):
		self.plotArithAvg = not self.plotArithAvg
		self.plotLaplace = True
		self.actionTrendTest.setChecked(True)
		if self.plotArithAvg:
			self.actionPlotArith.setText('Plot: Show Laplace Test')
		else:
			self.actionPlotArith.setText('Plot: Show Arithmetic Avg.')
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
		self.plotWindow = MplCanvas(self, self.canvasDPI)
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

		self.drawTypeGroup = QtWidgets.QActionGroup(self)
		self.drawTypeGroup.setExclusive(True)
		self.drawTypeGroup.addAction(self.actionPlot_Points)
		self.drawTypeGroup.addAction(self.actionPlot_Lines)
		self.drawTypeGroup.addAction(self.actionPlot_Both)

		self.setPlotType(2)

		print('init tab 1')