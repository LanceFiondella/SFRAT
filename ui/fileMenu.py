from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import logging as log
import os
import pandas as pd

from core.graphSettings import GraphSettings

class FileMenu(QHBoxLayout):
    def __init__(self, container, menu):
        super().__init__()
        self.container = container
        self.menu = menu

        self.initUI()


    def initUI(self):
        self.fileMenu = self.menu.addMenu("File")
        self.dataMenu = self.menu.addMenu("Data")
        self.modelMenu = self.menu.addMenu("Model")
        #self.viewMenu = self.menu.addMenu("View")

        self.initFileMenu()
        self.initDataMenu()
        self.initModelMenu()


    def initFileMenu(self):
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open Data File')
        openFile.triggered.connect(self.fileOpened)
        openFile.setMenuRole(QAction.NoRole)
        self.fileMenu.addAction(openFile)

    def initDataMenu(self):
        dataAction = QAction('dataAction', self)
        self.dataMenu.addAction(dataAction)

        self.dataMenu.addSeparator()

        self.viewStyle = QActionGroup(self.dataMenu)

        self.viewPoints = QAction('View Points on graph', self, checkable=True)
        self.viewPoints.setShortcut('Ctrl+P')
        self.viewPoints.setStatusTip('View Points on graphs')
        self.viewStyle.addAction(self.viewPoints)

        self.viewLines = QAction('View Lines on Graph', self, checkable=True)
        self.viewLines.setShortcut('Ctrl+L')
        self.viewLines.setStatusTip('View Lines on graphs')
        self.viewStyle.addAction(self.viewLines)

        self.viewBoth = QAction('View Both Lines and Points', self, checkable=True)
        self.viewBoth.setShortcut('Ctrl+B')
        self.viewBoth.setStatusTip('View Both Lines and points on graphs')
        self.viewStyle.addAction(self.viewBoth)

        self.viewStyle.triggered.connect(self.changeGraphSettings)

        self.dataMenu.addActions(self.viewStyle.actions())



    def initModelMenu(self):
        modelAction = QAction('modelAction', self)
        self.modelMenu.addAction(modelAction)


    def fileOpened(self):
        # open a file dialog
        files = QFileDialog.getOpenFileName(
            self.container, 'Open profile', "",
            filter=('Data Files (*.csv *.xls *.xlsx)'))
        # if a file was selected read it
        if files[0]:
            log.info("Opening:" + files[0])
            self.filename, fileExtension = os.path.splitext(files[0])
            if fileExtension == ".csv":
                self.container.data = pd.read_csv(files[0])
            else:
                self.container.data = pd.read_excel(files[0])
            self.container.updateGraphs()

    def changeGraphSettings(self):
        log.info("Updating Graph Setings")
        if self.viewLines.isChecked():
            g = GraphSettings.LINES
        elif self.viewPoints.isChecked():
            g = GraphSettings.POINTS
        elif self.viewBoth.isChecked():
            g = GraphSettings.BOTH

        self.container.dataTab.graphSettings.viewStyle = g
        self.container.updateGraphs()















#
