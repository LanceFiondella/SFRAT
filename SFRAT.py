#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
import os
import pandas as pd
from core import ui, window, analyzeData, applyModels, evaluateModels


class SFRAT(QtWidgets.QMainWindow, ui.Ui_MainWindow,
				window.Module, analyzeData.Module, applyModels.Module, evaluateModels.Module):
	
	canvasDPI = 90

	def __init__(self, parent=None):
		super(SFRAT, self).__init__(parent)
		self.setupUi(self)

		window.Module.__init__(self)
		analyzeData.Module.__init__(self)
		applyModels.Module.__init__(self)

		self.showMode(0)


def main():
	app = QApplication(sys.argv)
	form = SFRAT()
	form.show()
	app.exec_()

if __name__ == '__main__':
	main()
