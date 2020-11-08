#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
import os
import pandas as pd
from core import ui, window, analyzeData, applyModels, queryResults, evaluateModels

'''
This is the core SFRAT file. It loads its functionality from other "core" files,
namely each tab of the SFRAT plus some common window functionality. Each tab is
treated as a "module" in an attempt to allow for easy accessing and indexing of
data between tabs, however precaution must be taken in order to not overwrite
functionality between tabs. The overall design makes use of a minimal amount of
required python libraries, however some are needed for desktop use (qt), data
processing (pandas), plotting (matplotlib), as well as other basic functionality
which makes use of the pre-existing default modules.
'''


from models import DSS, GM, GO, ISS, JM, WEI
models = [DSS.DSS, GM.GM, GO.GO, ISS.ISS, JM.JM, WEI.WEI]	# must include for model to appear


class SFRAT(QtWidgets.QMainWindow, ui.Ui_MainWindow,
				window.Module,
				analyzeData.Module, applyModels.Module,
				queryResults.Module,evaluateModels.Module):	# each tab is assigned its own file
	
	canvasDPI = 90	# quick adjust for all matplotlib canvas DPIs

	def __init__(self, parent=None):
		super(SFRAT, self).__init__(parent)
		self.setupUi(self)

		self.modules = models

		window.Module.__init__(self)	# load window and 4 tabs
		analyzeData.Module.__init__(self)
		applyModels.Module.__init__(self)
		queryResults.Module.__init__(self)
		evaluateModels.Module.__init__(self)

		self.showMode(0)	# setup done, show first tab
		print('SFRAT initialized')


def main():
	app = QApplication(sys.argv)
	form = SFRAT()
	form.show()
	app.exec_()

if __name__ == '__main__':
	main()
