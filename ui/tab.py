from PyQt5.QtWidgets import *
from ui.sideMenu import SideMenu

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# creates a tab with a side menu and a figure window
class Tab(QWidget):
    DATA_TAB = SideMenu.DATA_MENU
    MODEL_TAB = SideMenu.MODEL_MENU
    def __init__(self, container, mode):
        super().__init__()
        self.container = container
        self.mode = mode
        self.initUI()

    def initUI(self):
        # setup menu
        self.layout = QHBoxLayout()
        self.sideMenu = QVBoxLayout()
        self.layout.addLayout(SideMenu(self, self.mode), 20)
        self.setLayout(self.layout)

        # setup graph
        self.figure = Figure(figsize=(5, 3))
        self.plotFigure = FigureCanvas(self.figure)
        self.layout.addWidget(self.plotFigure, 80)
        #self.addToolBar(QtCore.Qt.RightToolBarArea, NavigationToolbar(self.plotFigure, self))
        self.plot = self.plotFigure.figure.subplots()

    def updateGraph(self):
        self.plot.clear()
        self.data = self.container.data
        # plot data
        self.plot.step(self.data["FT"], self.data["FN"])

        # labels
        self.plot.set_title("Number of Failures vs. Time ")
        self.plot.set_xlabel("Cumulative Time (s)")
        self.plot.set_ylabel("Number of Failures")
        self.plot.figure.canvas.draw()
