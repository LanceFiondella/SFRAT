from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
import os
import sfrat
import pandas as pd
import matplotlib


matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)


class SFRAT(QtWidgets.QMainWindow, sfrat.Ui_MainWindow):

	curFilePath = None	# maybe not needed? fns can call between selves
	curSheetName = None
	curFileRaw = None
	curFileData = None

	plotType = 'FT'
	plotPtLines = 2	# initial state both dots n lines
	plotLaplace = False
	plotLaplaceConf = 0.9
	plotArithAvg = False

	sheetIndex = 0
	sheetActions = []	# stores menu options for sheet names for deletion etc

	plotCurves = [[]]	# store all curves for plotting

	def winTitle(self):
		windowTitle = f"SFRAT - {os.path.split(self.curFilePath)[1]}"
		self.setWindowTitle(windowTitle)


	def openFile_click(self, other):
		print('opening file')
		options = QFileDialog.Options()
		fileName, _ = QFileDialog.getOpenFileName(self,"Open Data", options=options)
		# todo restrict input files to xlsx or csv
		if fileName:
			try:
				self.curFilePath = fileName
				self.curFileRaw = pd.read_excel(fileName, 
									sheet_name=None,	# load all sheets
									ignore_index=True)
				print(f'File Loaded with {len(self.curFileRaw)} sheets')
				# pd.read_csv
			except:
				print('Import Error')	# file not convertable to pandas
				return

			self.winTitle()
			self.convertFileData()
			self.updateSheetSelect(self.curFileData)	
			self.curSheetName = list(self.curFileData.keys())[0]	# pick 1st sheet
			self.redrawPlot()

			return
		print('open file failed')

	def convertFileData(self):
		self.curFileData = {}	# uses FN, IF, and FT, some datasets dont use
		for sheet in self.curFileRaw:
			newFrame = {}
			keys = self.curFileRaw[sheet].keys()

			if 'T' in keys:
				newFrame['FN'] = self.curFileRaw[sheet]['T'].copy()
			elif 'FN' in keys:
				newFrame['FN'] = self.curFileRaw[sheet]['FN'].copy()

			if 'IF' in keys:
				newFrame['IF'] = self.curFileRaw[sheet]['IF'].copy()
			elif 'FC' in keys:
				newFrame['IF'] = self.curFileRaw[sheet]['FC'].copy()

			if 'FT' in keys:
				newFrame['FT'] = self.curFileRaw[sheet]['FT'].copy()
			elif 'CFC' in keys:
				newFrame['FT'] = self.curFileRaw[sheet]['CFC'].copy()

			if 'IF' in newFrame.keys() and not 'FT' in newFrame.keys():
				# sheet has IF, convert for FT/CFC
				newFrame['FT'] = [newFrame['IF'][0]]
				for idx in range(1,len(newFrame['IF'])):
					newFrame['FT'].append(newFrame['FT'][idx - 1] + newFrame['IF'][idx])
				print(f'{sheet} missing FT, calc from IF')
			elif 'FT' in newFrame.keys() and not 'IF' in newFrame.keys():
				newFrame['IF'] = [newFrame['FT'][0]]
				for idx in range(1,len(newFrame['FT'])):
					newFrame['IF'].append(newFrame['FT'][idx] - newFrame['FT'][idx - 1])
				print(f'{sheet} missing IF, calc from FT')

			newFrame['FI'] = []
			for fi in newFrame['IF']:
				if fi == 0:
					newFrame['FI'].append(-1)
					continue
				newFrame['FI'].append(1/fi)
			mx = max(newFrame['FI'])
			for i, fi in enumerate(newFrame['FI']):
				if fi == -1:
					newFrame['FI'][i] = 2*mx # todo make this better

			self.curFileData[str(sheet)] = newFrame

		return

	def switchSheet(self):
		self.menuSelect_Sheet.setActiveAction(self.sender())
		sheetName = self.sender().text()
		self.curSheetName = sheetName
		self.redrawPlot()
		print(f'changed to sheet {sheetName}')

	def updateSheetSelect(self, sheets):
		for old_action in self.sheetActions:
			old_action.deleteLater()	# remove sheets from last file

		for sheet in sheets:
			sheetAction = QtWidgets.QAction(self)
			sheetAction.setText(sheet)
			sheetAction.triggered.connect(self.switchSheet)
			self.menuSelect_Sheet.addAction(sheetAction)
			self.sheetActions.append(sheetAction)
							# later maybe cleaner method for indexing button

	def showMode(self, modeNum):
		print(f'switch to mode {modeNum}')
		for idx, mode in enumerate([self.analyzeData,
									self.applyModels,
									self.modelResults,
									self.evalResults]):
			if idx == modeNum:
				mode.show()
			else:
				mode.hide()
		return

	def redrawPlot(self):
		# draw plot
		if self.curFileData == None:
			return	# file not open
		curSheet = self.curFileData[self.curSheetName]
		self.plotWindow.axes.clear()

		if not self.plotLaplace:
			self.plotCurves[0] = [curSheet['FN'],
								curSheet[self.plotType]]
			if self.plotType == 'FT':
				self.plotCurves[0].reverse()

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
				self.plotWindow.axes.step(plotaxes[0], plotaxes[1], where='post')
			if self.plotPtLines == 0 or self.plotPtLines == 2:
				self.plotWindow.axes.plot(plotaxes[0], plotaxes[1],'.')

		self.plotWindow.draw()
		self.dataTable.clear()

		self.dataTable.setColumnCount(3)
		self.dataTable.setRowCount(len(curSheet['FN']))

		self.dataTable.setHorizontalHeaderLabels(['FN','IF',
			'Running Avg' if self.plotArithAvg else 'Laplace Statistic' if self.plotLaplace else 'FT'])


		for i in range(len(curSheet['FN'])):
			newFN = QtWidgets.QTableWidgetItem(str(curSheet['FN'][i]))
			newIF = QtWidgets.QTableWidgetItem(str(curSheet['IF'][i]))
			newFT = QtWidgets.QTableWidgetItem(str(runAvg[i]) if self.plotArithAvg else str(laplace[i]) if self.plotLaplace else str(curSheet['FT'][i]))

			newFN.setFlags(newFN.flags() & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
			newIF.setFlags(newIF.flags() & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)
			newFT.setFlags(newFT.flags() & ~QtCore.Qt.ItemIsEditable & ~QtCore.Qt.ItemIsSelectable)

			self.dataTable.setItem(i, 0, newFN)
			self.dataTable.setItem(i, 1, newIF)
			self.dataTable.setItem(i, 2, newFT)

		return

	def setView(self, viewNum):
		self.plotType = ['FT','IF','FI'][viewNum]
		self.redrawPlot()
		print(f'set view type to {self.plotType}')

	def setPlotType(self, typeNum):
		self.plotPtLines = typeNum
		self.redrawPlot()
		print(f'set dot/line type to {typeNum}')

	def laplaceToggle(self, en):
		self.plotLaplace = en
		self.redrawPlot()
		print('toggled laplace trend test')

	def arithToggle(self):
		self.plotArithAvg = not self.plotArithAvg
		if self.plotArithAvg:
			self.actionPlotArith.setText('Plot: Toggle Laplace Test')
		else:
			self.actionPlotArith.setText('Plot: Arithmetic Average')
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
	

	def __init__(self, parent=None):
		super(SFRAT, self).__init__(parent)
		self.setupUi(self)

		self.plotWindow = MplCanvas(self, width=1, height=1)
		self.gridLayout_2.addWidget(self.plotWindow, 0, 0, 1, 1)

		self.actionCF.triggered.connect(lambda: self.setView(0))
		self.actionTBF.triggered.connect(lambda: self.setView(1))
		self.actionFI.triggered.connect(lambda: self.setView(2))

		self.actionLapConf.triggered.connect(self.laplaceQuery)
		self.actionTrendTest.triggered.connect(self.laplaceToggle)
		self.actionPlotArith.triggered.connect(self.arithToggle)

		self.actionPlot_Points.triggered.connect(lambda: self.setPlotType(0))
		self.actionPlot_Lines.triggered.connect(lambda: self.setPlotType(1))
		self.actionPlot_Both.triggered.connect(lambda: self.setPlotType(2))

		self.showMode(0)
		self.actionAnalyzeData.triggered.connect(lambda: self.showMode(0))
		self.actionApplyModels.triggered.connect(lambda: self.showMode(1))
		self.actionModelResults.triggered.connect(lambda: self.showMode(2))
		self.actionEvaluateModels.triggered.connect(lambda: self.showMode(3))


def main():
	app = QApplication(sys.argv)
	form = SFRAT()
	form.show()
	app.exec_()

if __name__ == '__main__':
	main()
