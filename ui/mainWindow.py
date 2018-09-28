from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np

import logging as log

class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title = 'SFRAT Python'
		self.left = 10
		self.top = 10
		self.width = 1080
		self.height = 720
		self.initUI()
		self.drawGraph()


	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.show()

	def drawGraph(self):
		self._main = QtWidgets.QWidget()
		self.setCentralWidget(self._main)
		layout = QtWidgets.QVBoxLayout(self._main)

		dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
		layout.addWidget(dynamic_canvas)
		self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(dynamic_canvas, self))

		self._dynamic_ax = dynamic_canvas.figure.subplots()
		self._update_canvas()


	def _update_canvas(self):
		self._dynamic_ax.clear()
		t = np.linspace(0, 10, 101)
		# Shift the sinusoid as a function of time.
		self._dynamic_ax.plot(t, np.sin(t))
		self._dynamic_ax.figure.canvas.draw()













#
