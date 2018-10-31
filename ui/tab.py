from PyQt5.QtWidgets import *
from ui.sideMenu import SideMenu

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from core.graphSettings import GraphSettings

# creates a tab with a side menu and a figure window
class Tab(QWidget):
    DATA_TAB = SideMenu.DATA_MENU
    MODEL_TAB = SideMenu.MODEL_MENU
    def __init__(self, container, mode):
        super().__init__()
        self.container = container
        self.mode = mode
        self.initUI()
        self.graphSettings = GraphSettings()

    def initUI(self):
        # setup menu
        self.layout = QHBoxLayout()
        self.sideMenu = SideMenu(self, self.container, self.mode)
        self.layout.addLayout(self.sideMenu, 20)
        self.setLayout(self.layout)

        # setup graph
        self.plotWidget = QWidget()
        plotLayout = QVBoxLayout()
        self.figure = Figure(tight_layout={"pad": 2.0})
        self.plotFigure = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(self.plotFigure, self.plotWidget)
        plotLayout.addWidget(self.plotFigure, 1)
        plotLayout.addWidget(toolbar)
        self.plotWidget.setLayout(plotLayout)

        self.layout.addWidget(self.plotWidget, 80)
        #self.addToolBar(QtCore.Qt.RightToolBarArea, NavigationToolbar(self.plotFigure, self))
        self.plot = self.plotFigure.figure.subplots()

    def updateGraph(self):
        self.plot.clear()
        self.plot.figure.canvas.draw()

    #def updateGraph(self):
    #    pass
