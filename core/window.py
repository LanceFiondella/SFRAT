'''
window.py - controls functionality of SFRAT overhead menu
actions as well as taskbar, menu bar, switch between tabs

TODO: make decimal places an option in the UI
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import os
import pandas as pd
import numpy as np


class Module:

	curFilePath = None	# maybe not needed? fns can call between selves
	curSheetName = None
	curFileData = None

	currentTab = None

	sheetIndex = 0
	sheetActions = []	# stores menu options for sheet names for deletion etc
	plotCurves = [[]]	# store all curves for plotting

	dataDecimalPlaces = 3



	def winTitle(self):	# update the window title to match the open file name
		ext = os.path.splitext(self.curFilePath)[1]
		windowTitle = f"SFRAT - {os.path.split(self.curFilePath)[1]}"
		if ext != ".csv":
			windowTitle += f": {self.curSheetName}"
		self.setWindowTitle(windowTitle)


	def numfmt(self, number):	# round to decimal places and remove following zeros
		n = round(number, self.dataDecimalPlaces)
		return str(int(n)) if n % 1 == 0 else str(n)


	def openFile_click(self, other = None, auto = False):	# open a failure data listing
		print('opening file')
		d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,
					"Open Failure Data",
					d,
					"Excel (*.xls, *.xlsx), CSV (*.csv) (*.csv *.xls *.xlsx)")#;; All files (*.*)")

		if fileName:
			try:	# if excel, load into dataframe
					# if csv, make into dataframe with 1 sheet
				ext = os.path.splitext(fileName)[1]
				if ext == '.xls' or ext == '.xlsx':
					curFileRaw = pd.read_excel(fileName, 
									sheet_name=None, engine='openpyxl')
					#print(curFileRaw)
					if not auto:	# for auto report disgregard ui
						self.menuSelect_Sheet.menuAction().setVisible(True)
				elif ext == '.csv':
					curFileRaw = {"Sheet": pd.read_csv(fileName)}
					if not auto:
						self.menuSelect_Sheet.menuAction().setVisible(False)
			except Exception as e:
				print(f'Import Error:\n {e}')	# file not convertable to pandas
				return

			self.curFilePath = fileName
			print(f'File Loaded with {len(curFileRaw)} sheets')

			if not auto:
				self.statusBar.clearMessage()

			self.convertFileData(curFileRaw)

			self.listModels()	# do before cursheetname to only do once	
			self.updateSheetSelect(self.curFileData)
			self.switchSheet(force = list(self.curFileData.keys())[0])	# pick 1st sheet

			self.winTitle()

			return

		print('open file failed')


	def exportPlot(self):
		print('saving plot')

		d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		exportPlotWindow = self.currentTab < 2 and ([self.analyzeTab, self.modelTab][self.currentTab].currentIndex() == 0)
		# if in plot tab, select is plot open or data open, otherwise data is open so export csv

		if exportPlotWindow:	# export plot
			fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Export Plot', d, 'PNG Image (*.png);; JPG Image (*.jpg *.jpeg)')[0]
			if fname and fname != '':
				[self.plotWindow, self.plotWindowModel][self.currentTab].figureref.savefig(fname)

		else:	# export data as csv
			fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Export Data', d,
				'Excel (*.xlsx)(*.xlsx);; CSV (*.csv)(*.csv);; HTML (*.html)(*.html);; JSON (*.json)(*.json);; LaTeX (*.tex)(*.tex)')[0]

			if fname and fname != '':
				exportObj = [self.dataTable, self.modelTable, self.queryTable, self.modelEvalTable][self.currentTab]
				exportFrame = pd.DataFrame(columns=[exportObj.horizontalHeaderItem(x).text() for x in range(exportObj.columnCount())])
				extidx = ['.xlsx', '.csv', '.html', '.json', '.tex'].index(os.path.splitext(fname)[1])
					# get table to export, create a new dataframe, and get the file extension to select which pandas export to use

				for index in range(exportObj.rowCount()):
					for colIndex, col in enumerate(exportFrame.columns):
						try:	# some cells are empty and will not be exported as a number
							exportFrame.at[index + 1, col] = float(exportObj.item(index, colIndex).text())
						except:	# plaintext, include it anyway
							exportFrame.at[index + 1, col] = (exportObj.item(index, colIndex).text())
					# populate dataframe by row and column

				pdExport = [exportFrame.to_excel, exportFrame.to_csv, exportFrame.to_html, exportFrame.to_json, exportFrame.to_latex][extidx]
				try:
					pdExport(fname, index=False)	# select pandas export to use then export it
				except:
					pdExport(fname)	# for formats that don't have indexing option

		if fname:		
			print('export successful to', fname)
		else:
			print('export failed')


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

			try:
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
			except:
				print(f'cannot convert "{sheet}" sheet')


	def switchSheet(self, action = None, force = None):

		sheetName = force if force != None else self.sender().text() 
					# functionality for forced sheet switch
		if sheetName == self.curSheetName:
			return	# only different sheet switch

		if force == None:	# select via button to 
			self.menuSelect_Sheet.setActiveAction(self.sender())
		else:
			for act in self.sheetActions:
				act.setChecked(force == act.text())

		self.curSheetName = sheetName
		self.plotStartIndex = 0
		self.plotStopIndex = len(self.curFileData[self.curSheetName]['IF'])
		self.winTitle()

		self.modelShow = []

		for m in self.modelActions:
			m.setChecked(False)

		self.futureFailTime = self.curFileData[self.curSheetName].FT.iloc[-1] - \
								self.curFileData[self.curSheetName].FT.iloc[-2]
		self.modelRelInterval = self.futureFailTime
		self.additionalRuntime = self.futureFailTime


		self.redrawPlot()
		self.redrawModelPlot()
		self.plotModelTable()
		self.updateQueryTable()

		self.showMode(0)

		print(f'changed to sheet {sheetName}')


	def updateSheetSelect(self, sheets):
		
		for sheet in self.sheetActions:
			self.sheetList.removeAction(sheet)

		self.sheetActions = []

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

		for idx, mode in enumerate([self.menuViewAD, self.menuViewAM,
									self.menuViewQ, self.menuViewE]):
			mode.menuAction().setVisible(idx == modeNum)
								# show right view menu


		for idx, mode in enumerate([self.actionAnalyzeData, self.actionApplyModels,
									self.actionModelResults, self.actionEvaluateModels]):
			mode.setChecked(idx == modeNum)
				# set mode checked (for force open mode)

		for idx, buttons in enumerate(self.modelButtons):
			for midx, button in enumerate(buttons):
				if modeNum == idx and idx < 9:
					button.setShortcut(f'Ctrl+{midx+1}')
				else:
					button.setShortcut('')



		if modeNum == 0:
			self.redrawPlot()
		elif modeNum == 1:
			self.redrawModelPlot()

		self.currentTab = modeNum	# used to keep track of current export


	def __init__(self):

		self.actionOpen.triggered.connect(self.openFile_click)
		self.actionExport.triggered.connect(self.exportPlot)

		self.statusBar = QtWidgets.QStatusBar()
		self.setStatusBar(self.statusBar)

		self.sheetList = QtWidgets.QActionGroup(self.menuSelect_Sheet)
		self.sheetList.setExclusive(True)
		self.menuSelect_Sheet.menuAction().setVisible(False)

		self.selPageGroup = QtWidgets.QActionGroup(self.menuMode)
		self.selPageGroup.setExclusive(True)
		self.actionAnalyzeData.setChecked(True)
		for i, x in enumerate([self.actionAnalyzeData, self.actionApplyModels,
										self.actionModelResults, self.actionEvaluateModels]):
			self.selPageGroup.addAction(x)
			x.triggered.connect(lambda _, idx = i: self.showMode(idx))


		self.statusBar.showMessage("Import a file to begin", 0)
		print('init window')

