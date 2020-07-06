from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import os
import pandas as pd


class Module:

	curFilePath = None	# maybe not needed? fns can call between selves
	curSheetName = None
	curFileData = None

	exportCanvas = None

	sheetIndex = 0
	sheetActions = []	# stores menu options for sheet names for deletion etc
	plotCurves = [[]]	# store all curves for plotting


	def winTitle(self):
		ext = os.path.splitext(self.curFilePath)[1]
		windowTitle = f"SFRAT - {os.path.split(self.curFilePath)[1]}"
		if ext != ".csv":
			windowTitle += f": {self.curSheetName}"
		self.setWindowTitle(windowTitle)


	def openFile_click(self, other):
		print('opening file')

		d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
					"Open Failure Data",
					d,
					"Excel (*.xls, *.xlsx), CSV (*.csv) (*.csv *.xls *.xlsx);; All files (*.*)")

		if fileName:
			try:	# if excel, load into dataframe
					# if csv, make into dataframe with 1 sheet
				ext = os.path.splitext(fileName)[1]
				if ext == '.xls' or ext == '.xlsx':
					curFileRaw = pd.read_excel(fileName, 
									sheet_name=None,	# load all sheets
									ignore_index=True)
					self.menuSelect_Sheet.menuAction().setVisible(True)
				elif ext == '.csv':
					curFileRaw = {"Sheet": pd.read_csv(fileName)}
					self.menuSelect_Sheet.menuAction().setVisible(False)
			except:
				print('Import Error')	# file not convertable to pandas
				return

			self.curFilePath = fileName
			print(f'File Loaded with {len(curFileRaw)} sheets')

			self.convertFileData(curFileRaw)	
			self.curSheetName = list(self.curFileData.keys())[0]	# pick 1st sheet
			self.plotStartIndex = 0
			self.plotStopIndex = len(self.curFileData[self.curSheetName]['IF'])
			self.updateSheetSelect(self.curFileData)
			self.redrawPlot(self.plotWindow)
			self.winTitle()

			return
		print('open file failed')


	def convertFileData(self, iData):

		self.curFileData = {}	# uses FN, IF, and FT, some datasets dont use
		for sheet in iData:
			newFrame = {}
			keys = iData[sheet].keys()

			if 'T' in keys:
				newFrame['FN'] = iData[sheet]['T'].copy()
			elif 'FN' in keys:
				newFrame['FN'] = iData[sheet]['FN'].copy()

			if 'IF' in keys:
				newFrame['IF'] = iData[sheet]['IF'].copy()
			elif 'FC' in keys:
				newFrame['IF'] = iData[sheet]['FC'].copy()

			if 'FT' in keys:
				newFrame['FT'] = iData[sheet]['FT'].copy()
			elif 'CFC' in keys:
				newFrame['FT'] = iData[sheet]['CFC'].copy()

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
					newFrame['FI'][i] = float('inf')
					#newFrame['FI'][i] = 2*mx # todo make this better

			self.curFileData[str(sheet)] = pd.DataFrame.from_dict(newFrame)


	def switchSheet(self):
		self.menuSelect_Sheet.setActiveAction(self.sender())
		sheetName = self.sender().text()
		self.curSheetName = sheetName
		self.plotStartIndex = 0
		self.plotStopIndex = len(self.curFileData[self.curSheetName]['IF'])
		self.winTitle()
		self.redrawPlot(self.plotWindow)
		print(f'changed to sheet {sheetName}')


	def updateSheetSelect(self, sheets):
		for old_action in self.sheetActions:
			old_action.deleteLater()	# remove sheets from last file

		for sheet in sheets:
			sheetAction = QtWidgets.QAction(self, checkable=True)
			sheetAction.setText(sheet)
			sheetAction.setChecked(sheet == self.curSheetName)
			sheetAction.triggered.connect(self.switchSheet)
			self.sheetList.addAction(sheetAction)
			self.sheetActions.append(sheetAction)

		self.menuSelect_Sheet.addActions(self.sheetList.actions())
							# later maybe cleaner method for indexing button

	def showMode(self, modeNum):
		print(f'switch to mode {modeNum}')
		for idx, mode in enumerate([self.analyzeData, self.applyModels,
									self.modelResults, self.evalResults]):
			if idx == modeNum:	# hide all but active tab
				mode.show()
			else:
				mode.hide()

		for idx, mode in enumerate([self.menuViewAD,
									self.menuViewAM]):
			mode.menuAction().setVisible(idx == modeNum)
								# show right view menu

		for idx, mode in enumerate([self.plotWindow,
									self.plotWindowModel]):
			if idx == modeNum:
				self.exportCanvas = mode

		return


	def __init__(self):
		self.actionOpen.triggered.connect(self.openFile_click)

		self.statusBar = QtWidgets.QStatusBar()
		self.setStatusBar(self.statusBar)
		self.statusBar.showMessage("Ready", 1000)

		self.sheetList = QtWidgets.QActionGroup(self.menuSelect_Sheet)
		self.sheetList.setExclusive(True)
		self.menuSelect_Sheet.menuAction().setVisible(False)

		self.actionAnalyzeData.triggered.connect(lambda: self.showMode(0))
		self.actionApplyModels.triggered.connect(lambda: self.showMode(1))
		self.actionModelResults.triggered.connect(lambda: self.showMode(2))
		self.actionEvaluateModels.triggered.connect(lambda: self.showMode(3))



		print('init window')