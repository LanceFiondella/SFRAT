from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import logging as log
import os
import pandas as pd

from core.graphSettings import GraphSettings
from core.dataClass import Data

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
        #self.dataMenu.addSeparator()
        self.dataMenu.addSection("Plot Graph with")

        self.viewStyle = QActionGroup(self.dataMenu)

        self.viewPoints = QAction('View Points', self, checkable=True)
        self.viewPoints.setShortcut('Ctrl+P')
        self.viewPoints.setStatusTip('View Points on graphs')
        self.viewStyle.addAction(self.viewPoints)

        self.viewLines = QAction('View Lines', self, checkable=True)
        self.viewLines.setShortcut('Ctrl+L')
        self.viewLines.setStatusTip('View Lines on graphs')
        self.viewStyle.addAction(self.viewLines)

        self.viewBoth = QAction('View Point and Lines', self, checkable=True)
        self.viewBoth.setShortcut('Ctrl+B')
        self.viewBoth.setStatusTip('View Both Lines and points on graphs')
        self.viewStyle.addAction(self.viewBoth)

        self.viewStyle.triggered.connect(self.changeGraphSettings)

        self.dataMenu.addActions(self.viewStyle.actions())

        self.viewTrend = QActionGroup(self.dataMenu)

        self.viewData = QAction("View Data", self, checkable=True)
        self.viewData.setShortcut('Ctrl+D')
        self.viewData.setStatusTip('View Data')

        self.viewTest = QAction("View Trend", self, checkable=True)
        self.viewTest.setShortcut('Ctrl+T')
        self.viewTest.setStatusTip('View Trend Test')


        self.dataMenu.addSection("View Data or Trend")
        self.viewTrend.addAction(self.viewData)
        self.viewTrend.addAction(self.viewTest)
        self.dataMenu.addActions(self.viewTrend.actions())




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
                # if the file is a csv read the data and set no availabe sheets
                self.container.data = Data(pd.read_csv(files[0]))
                self.container.sheets = ["No Sheets Available"]
                self.container.currentSheet = self.container.sheets[0]
            else:
                # if Excel file handle multi sheets
                self.container.sheets = pd.ExcelFile(files[0]).sheet_names
                self.container.currentSheet = self.container.sheets[0]
                self.container.fullDataSet = pd.read_excel(files[0], None)
                self.container.data = Data(\
                self.container.fullDataSet[self.container.currentSheet])

            self.container.updateGraphs()
            self.container.updateSheets()

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
