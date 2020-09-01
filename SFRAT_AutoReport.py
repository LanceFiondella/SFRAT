#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys, os, datetime
import pandas as pd
from core import report_ui, window, analyzeData, applyModels, queryResults, evaluateModels


from models import DSS, GM, GO, ISS, JM, WEI
models = [DSS.DSS, GM.GM, GO.GO, ISS.ISS, JM.JM, WEI.WEI]	# must include for model to appear


class SFRAT_AutoReport(QtWidgets.QMainWindow, report_ui.Ui_MainWindow,
				window.Module,
				analyzeData.Module, applyModels.Module,
				queryResults.Module,evaluateModels.Module):	# each tab is assigned its own file
	
	canvasDPI = 90	# quick adjust for all matplotlib canvas DPIs
	runModels = []
	runSheets = []
	sheetName = None
	sheetData = None

	plots = [	"cfplot1.png", 
				"ifplot1.png", 
				"fiplot1.png", 
				"lapplot1.png",
				"avgplot1.png", 
				"cfplot2.png",
				"ifplot2.png",
				"fiplot2.png",
				"relplot2.png", ]

	def exportReport(self):

		modelsToRun = list([models[self.runModels.index(x)] for x in self.runModels if x.checkState()])

		if self.curFileData == None:
			self.statusBar.showMessage("Import a file to begin", 1000)
			return

		if len(modelsToRun) == 0:
			self.statusBar.showMessage("Model(s) must be selected", 1000)
			return

		self.plotLaplaceConf = self.lapConfBox.value()/100	# tab 1 values
		self.plotPtLines = 2 if self.plotBoth.isChecked() else 1 if self.plotLines.isChecked() else 0 if self.plotPts.isChecked() else 2

		self.futureFailCount = self.predictBox.value()		# tab 2 values
		self.modelDataOnPlot = self.plotModelData.isChecked()
		self.modelDataEnd = self.plotDataEnd.isChecked()
		self.modelRelInterval = self.reliabilityBox.value()

		self.pctPSSE = self.psseBox.value()/100	# tab 3 values
		self.additionalRuntime = self.runtimeBox.value()
		self.desiredReliability = self.desRelBox.value()/100

		verboseReport = self.verboseBox.isChecked()

		printData = {'FN':list(self.sheetData['FN'])[:self.dataPtBox.value()],
					 'FT':list(self.sheetData['FT'])[:self.dataPtBox.value()],
					 'IF':list(self.sheetData['IF'])[:self.dataPtBox.value()]}
		printStr = "\n".join([f"{self.numfmt(printData['FN'][i])} & {self.numfmt(printData['IF'][i])} & {self.numfmt(printData['FT'][i])} \\\\"
						for i in range(self.dataPtBox.value()) ])



		if len(modelsToRun) == 1:
			modelStr = f'{modelsToRun[0].name} model'
		elif len(modelsToRun) == 2:
			modelStr = f'{modelsToRun[0].name} and {modelsToRun[1].name} models'
		else:
			modelStr = ', '.join(m[:-1]) + ', and ' + m[-1]

		with open('report/template.tex','r') as f:
			texlines = f.readlines()

		replace = [
		("$authorname$", os.getlogin()),
		("$date$", datetime.date.today().strftime("%B %d, %Y")),
		("$sheet$", self.sheetName),
		("$numpoints$", self.numfmt(self.dataPtBox.value())),
		("$ftab$", printStr),
		("$cfplot$", self.plots[0]),
		("$ifplot$", self.plots[1]),
		("$fiplot$", self.plots[2]),
		("$lappct$", self.numfmt(self.plotLaplaceConf*100)),
		("$lapplot$", self.plots[3]),
		("$runavg$", self.plots[4]),
		("$models_on$", modelStr),
		("$datashown$", "The original data is also shown." if verboseReport else ''),
		("$modelcfplot$", self.plots[5]),
		("$modelifplot$", self.plots[6]),
		("$modelfiplot$", self.plots[7]),
		("$relduration$", self.numfmt(self.modelRelInterval)),
		("$modelrelplot$", self.plots[8]),
		("$futurefailtime$", self.numfmt(self.additionalRuntime)),
		("$futurefailnum$", self.numfmt(self.futureFailCount)),
		("$desrelpct$", self.numfmt(self.desiredReliability*100)),


		("$qtab$",''),
		("$bestAICmodel$",''),
		("$pssepct$",self.numfmt(self.pctPSSE*100)),
		("$psse1minus$",self.numfmt((1-self.pctPSSE)*100)),
		("$bestPSSEmodel$",'')
		]


		outlines = []
		for i, line in enumerate(texlines):
			nl = line
			for tup in replace:
				nl = nl.replace(tup[0], tup[1])
			outlines.append(nl)

		with open('report/output.tex','w') as f:
			f.writelines(outlines)

		for ptype in ['FT','IF','FI']:
			pass

		# self.plotType = 'FT', self.plotLaplace, self.plotArithAvg, self.modelPlotType = 'FT', self.modelRelPlot
		return

	def listModels(self):	# override applyModels.py listmodels, called from file open

		# first clear existing models
		for p in self.runModels:
			self.modelSelect.takeItem(0)

		self.runModels = []

		for idx, m in enumerate(self.modules):
			newItem = QtWidgets.QListWidgetItem(f'Apply {m.name}')
			newItem.setFlags(newItem.flags() | QtCore.Qt.ItemIsUserCheckable)
			newItem.setCheckState(False)
			self.runModels.append(newItem)
			self.modelSelect.addItem(newItem)

		return

	def updateSheetSelect(self, data):	# override window.py called from file open

		for p in self.runSheets:
			self.sheetSelect.takeItem(0)

		self.runSheets = []

		for idx, sheet in enumerate(data):
			newItem = QtWidgets.QListWidgetItem(f'Sheet {str(sheet)}')
			self.runSheets.append(newItem)
			self.sheetSelect.addItem(newItem)

		self.sheetSelect.setCurrentRow(0)


		return

	def switchSheet(self, row = None, force = None):	# override window.py, row clicked
												# keep force arg as it exists in SFRAT call
		self.sheetName = str(list(self.curFileData.keys())[self.sheetSelect.currentRow()])
		self.sheetData = self.curFileData[self.sheetName]

		tbf = int(self.sheetData['FT'].iloc[-1] - self.sheetData['FT'].iloc[-2])
		self.reliabilityBox.setValue(tbf)
		self.runtimeBox.setValue(tbf)
		return

	def winTitle(self):	#override window.py
		return

	def __init__(self, parent=None):
		super(SFRAT_AutoReport, self).__init__(parent)
		self.setupUi(self)

		self.modules = models
		# don't initialize 4 tab UI, initialize auto report instead

		self.actionOpen.triggered.connect(lambda: self.openFile_click(auto=True))
		self.actionExport.triggered.connect(self.exportReport)

		self.statusBar = QtWidgets.QStatusBar()
		self.setStatusBar(self.statusBar)

		self.sheetSelect.currentRowChanged.connect(self.switchSheet)




def main():
	app = QApplication(sys.argv)
	form = SFRAT_AutoReport()
	form.show()
	app.exec_()

if __name__ == '__main__':
	main()
