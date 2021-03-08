'''
analyzeData.py - default tab that will simply plot data
(can be FT, IF, FI) and can view via spreadsheet-like
can also show laplace 
'''

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

	def redrawPlot(self):
		# draw plot ONLY for tab 1

		if self.curFileData == None:
			return		# file not open, do nothing

		curSheet = self.curFileData[self.curSheetName]
		self.plotWindow.axes.clear()	# remove previous plot

		self.plotWindow.axes.grid(True)

		if not self.plotLaplace:
			plotTitle = '{0} {1} vs Test Time'.format(self.curSheetName,
				['Cumulative Failures', 'Interfailure Times', 'Failure Intensity'][['FT','IF','FI'].index(self.plotType)])
			if self.plotType == 'FT':	# plot selected curve type
				plotaxes = [curSheet['FT'], curSheet['FN']]
			elif self.plotType == 'IF':
				plotaxes = [curSheet['FT'], curSheet['IF']]
			elif self.plotType == 'FI':
				plotaxes = [curSheet['FT'], curSheet['FI']]
		else:
			# plot laplace test or arith avg, calculate values (adapted from R code)
			if not self.plotArithAvg:
				plotTitle = f'{self.curSheetName} Laplace Trend Test @ {int(100*self.plotLaplaceConf)}% Confidence'
				lapConf = norm.ppf(1 - self.plotLaplaceConf)	#qnorm
				#print(lapConf)
				laplace = [0]
				for i in range(1, len(curSheet['IF'])):
					sumint = 0
					for j in range(i):
						sumint += curSheet['FT'][j]
					laplace.append(((sumint/(i)) - (curSheet['FT'][i]/2)) / (curSheet['FT'][i] * (1/(12*(i))**0.5 )))
				plotaxes = [list(range(len(laplace))), laplace]
			else:
				plotTitle = f'{self.curSheetName} Running Average Trend Test'
				runAvg = []
				for i in range(len(curSheet['IF'])):
					s1 = 0
					for j in range(1+i):
						s1 += curSheet['IF'][j]
					runAvg.append(s1 / (i+1))
				plotaxes = [list(range(len(runAvg))), runAvg]

		print('plotting')
		if self.plotPtLines == 0:
			# points
			self.plotWindow.axes.plot(plotaxes[0][self.plotStartIndex:self.plotStopIndex],
						plotaxes[1][self.plotStartIndex:self.plotStopIndex],'.', label = 'Data')
		elif self.plotPtLines == 1:
			# lines
			self.plotWindow.axes.step(plotaxes[0][self.plotStartIndex:self.plotStopIndex],
						plotaxes[1][self.plotStartIndex:self.plotStopIndex], where='post', label = 'Data')
		elif self.plotPtLines == 2:
			# both
			dataplot = self.plotWindow.axes.step(plotaxes[0][self.plotStartIndex:self.plotStopIndex],
						plotaxes[1][self.plotStartIndex:self.plotStopIndex],'.-', where='post', label = 'Data')
			colorplot = self.plotWindow.axes.plot([0],[0],'.')	# old method was to plot pts and lines separately
			clr = colorplot[0].get_color()				# caused problems w/ legend, so to keep same appearance
			colorplot[0].remove()						# next plot color was taken and used
			dataplot[0].set_markerfacecolor(clr)
			dataplot[0].set_markeredgecolor(clr)

		if self.plotLaplace and not self.plotArithAvg:	# plot laplace, need to plot after due to plot limits
			self.plotWindow.axes.axhline(lapConf,linestyle='--',color='r')

		self.plotWindow.axes.set_title(plotTitle)
		self.plotWindow.draw()	# draw curves

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


	def setViewAnalyze(self, viewNum):
		if viewNum < 3:
			self.plotType = ['FT','IF','FI'][viewNum]
		
		self.plotLaplace = viewNum >= 3
		self.plotArithAvg = viewNum == 4	# accomodate 2 extra tab 1 options
		self.actionLapConf.setVisible(viewNum == 3)	# hide laplace conf button when not plotting it

		self.redrawPlot()

		print(f'set view type A to {viewNum}')


	def setPlotType(self, typeNum, rec = 0):
		self.plotPtLines = typeNum
		if rec == 0:
			self.setPlotTypeModels(typeNum, 1)
		for i, option in enumerate([self.actionPlot_Points, self.actionPlot_Lines, self.actionPlot_Both]):
			option.setChecked(i == typeNum)
		self.redrawPlot()
		print(f'set dot/line type 2 to {typeNum}')


	def arithToggle(self):
		self.plotArithAvg = not self.plotArithAvg
		self.plotLaplace = True
		self.actionTrendTest.setChecked(True)
		if self.plotArithAvg:
			self.actionPlotArith.setText('Plot: Show Laplace Test')
		else:
			self.actionPlotArith.setText('Plot: Show Arithmetic Avg.')
		self.redrawPlot()


	def laplaceQuery(self):
		text, ok = QtWidgets.QInputDialog.getDouble(self,
								"Laplace Trend Test",
								"Enter a confidence level:",
								self.plotLaplaceConf,
								0, 1, 2, QtCore.Qt.WindowFlags(), 0.01)
		if ok:
			self.plotLaplaceConf = text
			self.redrawPlot()
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
			self.redrawPlot()



	def __init__(self):
		self.plotWindow = MplCanvas(self, self.canvasDPI)
		self.gridLayout_2.addWidget(self.plotWindow, 0, 0, 1, 1)

		self.actionCF.triggered.connect(lambda: self.setViewAnalyze(0))
		self.actionTBF.triggered.connect(lambda: self.setViewAnalyze(1))
		self.actionFI.triggered.connect(lambda: self.setViewAnalyze(2))
		self.actionLap.triggered.connect(lambda: self.setViewAnalyze(3))
		self.actionArith.triggered.connect(lambda: self.setViewAnalyze(4))

		self.actionLapConf.triggered.connect(self.laplaceQuery)

		self.actionStartIndex.triggered.connect(lambda: self.rangeDialog(True))
		self.actionStopIndex.triggered.connect(lambda: self.rangeDialog(False))

		self.actionPlot_Points.triggered.connect(lambda: self.setPlotType(0))
		self.actionPlot_Lines.triggered.connect(lambda: self.setPlotType(1))
		self.actionPlot_Both.triggered.connect(lambda: self.setPlotType(2))


		self.analyzePlotType = QtWidgets.QActionGroup(self)
		self.analyzePlotType.setExclusive(True)
		self.analyzePlotType.addAction(self.actionCF)
		self.analyzePlotType.addAction(self.actionTBF)
		self.analyzePlotType.addAction(self.actionFI)
		self.analyzePlotType.addAction(self.actionLap)
		self.analyzePlotType.addAction(self.actionArith)

		self.drawTypeGroup = QtWidgets.QActionGroup(self)
		self.drawTypeGroup.setExclusive(True)
		self.drawTypeGroup.addAction(self.actionPlot_Points)
		self.drawTypeGroup.addAction(self.actionPlot_Lines)
		self.drawTypeGroup.addAction(self.actionPlot_Both)

		self.setPlotType(2)

		print('init tab 1')