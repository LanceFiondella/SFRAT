from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import pandas as pd

import logging as log

from ui.fileMenu import FileMenu
from ui.sideMenu import SideMenu
from ui.tabs import *

from models.NullModel import NullModel

from core.dataClass import Data

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

        # default linear dataset
        self.data = Data(pd.DataFrame({"FN": np.linspace(0, 10, 101),
        "FT": np.linspace(0, 10, 101)}))

        # sheets used for load excel data
        self.sheets = ["No Sheets"]
        self.currentSheet = self.sheets[0]

        # default to no model
        self.model = NullModel()

        self.menu = FileMenu(self, self.menuBar())

        self.initUI()


    def initUI(self):
        # setup window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # setup tabs
        self.initTabs()

        self.show()

    def initTabs(self):
        self.tabs = QTabWidget()
        self.dataTab = DataTab(self)
        self.modelTab = ModelTab(self)

        self.tabs.addTab(self.dataTab, "Data Tab")
        self.tabs.addTab(self.modelTab, "Model Tab")

        self.layout.addWidget(self.tabs)

    def updateGraphs(self):
        self.dataTab.updateGraph()
        self.modelTab.updateGraph()

    def updateSheets(self):
        self.dataTab.updateSheets()











#
