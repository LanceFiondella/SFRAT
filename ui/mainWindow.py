from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np

import logging as log

from ui.topMenu import TopMenu
from ui.sideMenu import SideMenu

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'SFRAT Python'
        self.left = 10
        self.top = 10
        self.width = 1080
        self.height = 720
        self._main = QtWidgets.QWidget()

        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QVBoxLayout(self._main)

        self.initUI()
        self.drawGraph()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.topMenu = TopMenu(self)
        self.sideMenu = SideMenu(self)
        self.layout.addLayout(self.topMenu)
        self.hBox = QHBoxLayout()
        self.layout.addLayout(self.hBox)
        self.hBox.addLayout(self.sideMenu, 20)

        self.show()

    def drawGraph(self):
        self.plotFigure = FigureCanvas(Figure(figsize=(5, 3)))
        self.hBox.addWidget(self.plotFigure, 80)
        #self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(dynamic_canvas, self))

        self.plot = self.plotFigure.figure.subplots()
        self._update_canvas()


    def _update_canvas(self):
        self.plot.clear()
        t = np.linspace(0, 10, 101)
        self.plot.plot(t, np.sin(t))
        self.plot.figure.canvas.draw()













#
