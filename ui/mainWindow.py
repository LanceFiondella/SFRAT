from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import pandas as pd

import logging as log

from ui.topMenu import TopMenu
from ui.sideMenu import SideMenu
from ui.tab import Tab

from models.NullModel import NullModel

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

        self.data = pd.DataFrame({"FN": np.linspace(0, 10, 101),
        "FT": np.linspace(0, 10, 101)})

        self.model = NullModel()

        self.initUI()


    def initUI(self):
        # setup window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # setup tabs
        self.initTabs()
        #setup graph
        self.show()

    def initTabs(self):
        self.tabs = QTabWidget()
        self.dataTab = Tab(self, SideMenu.DATA_MENU)
        self.modelTab = Tab(self, SideMenu.MODEL_MENU)

        self.tabs.addTab(self.dataTab, "Data Tab")
        self.tabs.addTab(self.modelTab, "Model Tab")


        self.layout.addWidget(self.tabs)

    def initGraph(self):
        self.figure = Figure(figsize=(5, 3))
        self.plotFigure = FigureCanvas(self.figure)
        self.layout.addWidget(self.plotFigure, 90)
        #self.addToolBar(QtCore.Qt.RightToolBarArea, NavigationToolbar(self.plotFigure, self))
        self.plot = self.plotFigure.figure.subplots()

    def updateGraph(self):
        self.plot.clear()

        # plot data
        self.plot.step(self.data["FT"], self.data["FN"])

        # plot model data
        mdata = self.model.crunch(self.data)
        self.plot.plot(mdata["X"], mdata["Y"])

        # labels
        self.plot.set_title("Number of Failures vs. Time ")
        self.plot.set_xlabel("Cumulative Time (s)")
        self.plot.set_ylabel("Number of Failures")
        self.plot.legend(["Data", self.model.name])
        self.plot.figure.canvas.draw()













#
