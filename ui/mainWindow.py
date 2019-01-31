#Python imports
from collections import OrderedDict

# PyQt5 Imports
from PyQt5.QtWidgets import QMainWindow, QAction, QWidget, QVBoxLayout, QTabWidget, \
                            QMessageBox, QGroupBox, QLineEdit, QListWidget, \
                            QAbstractItemView, QMessageBox, QHBoxLayout, \
                            QLabel, QComboBox, QTableView,\
                            QPushButton, qApp, QFileDialog, QActionGroup
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import pyqtSignal

# Misc Imports
import numpy as np
import pandas as pd
import logging as log

# Local Imports
import models
from core.dataClass import Data
from core.trendTests import *
from core.rootFind import RootFind
from core.graphSettings import PlotSettings
from ui.commonWidgets import ComputeWidget, PlotAndTable
from ui.resultWindow import ResultWindow


class MainWindow(QMainWindow):
    # Signals
    importFileSignal = pyqtSignal()

    def __init__(self, debug=False):
        """
        MainWindow class that displays the initial state of the app
        This is where the user imports and analyses raw data
        """
        super().__init__()

        # Setup main window parameters
        self.title = 'SFRAT'
        self.left = 10
        self.top = 10
        self.width = 1080
        self.height = 720
        self._main = MainWidget()
        self.setCentralWidget(self._main)

        # Set debug mode
        self.debug = debug

        # Set data
        self.data = Data()
        self.trendTests = {cls.__name__: cls for
                           cls in TrendTest.__subclasses__()}
        self.plotSettings = PlotSettings()

        # Signal connections
        self.importFileSignal.connect(self.importFile)
        self._main.sideMenu.viewChangedSignal.connect(self.setDataView)
        self._main.sideMenu.runModelSignal.connect(self.runModels)

        self.ax = self._main.plotAndTable.figure.add_subplot(111)

        self.initUI()

    def closeEvent(self, event):
        """
        Clicking the x button of the main window exits the app
        """
        qApp.quit()

    def initUI(self):
        """
        Initialize the UI of the main window
        """
        # setup window
        self.setupMenu()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Ready')
        self.viewType = 'view'
        self.index = 0
        self.show()

    def runModels(self, modelDetails):
        """
        Run all selected models using the root finding algorithm selected

        Args:
            modelDetails: Dictionary of models and algorithms to run
        """
        modelsToRun = modelDetails['modelsToRun']
        algoToRun = modelDetails['algoToRun']
        if self.data:
            self.computeWidget = ComputeWidget(modelsToRun,
                                               algoToRun, self.data)
            self.computeWidget.results.connect(self.displayResults)
        else:
            QMessageBox.about(self.container, "No data found",
                              "Please load failure data in csv"
                              "or excel format")

    def displayResults(self, results):
        """
        Display results in a separate window.

        Args:
            results: List of models whose roots have been evaluated
        """
        self.resultWindow = ResultWindow(results)

    def importFile(self):
        """
        Import selected file

        """
        self._main.sideMenu.sheetSelect.addItems(self.data.sheetNames)
        self.setDataView('view', 0)

    def changeSheet(self, index):
        """
        Change the current sheet to display

        Args:
            index: index of the sheet
        """
        self.data.currentSheet = index
        self._main.plotAndTable.figure.canvas.draw()

    def setDataView(self, viewType, index):
        """
        Set the data to be displayed

        Args:
            viewType: string that determines view
            index: index of the dataview list
        """
        if self.data.getData() is not None:
            if viewType == 'view':
                self.setRawDataView(index)
            elif viewType == 'trend':
                self.setTrendTest(index)
            elif viewType == 'sheet':
                self.changeSheet(index)
            self.viewType = viewType
            self.index = index

    def setRawDataView(self, index):
        self._main.plotAndTable.tableWidget.setModel(self.data.getDataModel())
        dataframe = self.data.getData()
        if index == 0:
            # Cumulative Failures

            self.ax = self.plotSettings.generatePlot(
                                            self.ax, dataframe['FT'],
                                            dataframe['FN'],
                                            title="Cumulative Failures",
                                            xLabel="Cumulative Time (s)",
                                            yLabel="Number of Failures")
        elif index == 1:
            # Times between failures
            self.ax = self.plotSettings.generatePlot(
                                            self.ax, dataframe['FT'],
                                            dataframe['IF'],
                                            title="Interfailure Times",
                                            xLabel="Cumulative Time (s)",
                                            yLabel="Times between "
                                            "successive failures")
        elif index == 2:
            # Failure intensity
            self.ax = self.plotSettings.generatePlot(
                                            self.ax, dataframe['FT'],
                                            1/dataframe['IF'],
                                            title="Failure Intensity",
                                            xLabel="Cumulative Time (s)",
                                            yLabel="Number of Failures "
                                            "per Unit Time")
        self._main.plotAndTable.figure.canvas.draw()

    def setTrendTest(self, index):
        """
        Set the view to a trend test

        Args:
            index: index of the list of trend test
        """
        trendTest = list(self.trendTests.values())[index]()
        trendData = trendTest.run(self.data.getData())
        self.ax = self.plotSettings.generatePlot(self.ax, trendData['X'],
                                                 trendData['Y'],
                                                 title=trendTest.name,
                                                 xLabel=trendTest.xAxisLabel,
                                                 yLabel=trendTest.yAxisLabel)
        self._main.plotAndTable.figure.canvas.draw()

    def setPlotStyle(self, style='-o', plotType='step'):
        """
        Set the style and type of plot

        Keyword Args:
            style: Dotted, line or both
            plotType: step or plot or any matplotlib plotting function
        """
        self.plotSettings.style = style
        self.plotSettings.plotType = plotType
        self.updateUI()

    def updateUI(self):
        """
        Change Plot, Table and SideMenu
        when the state of the Data object changes

        Should be called explicitly
        """
        self.setDataView(self.viewType, self.index)

    def setupMenu(self):
        """
        Setup contents of the menu bar
        """

        self.menu = self.menuBar()
        # Setting up fileMenu
        fileMenu = self.menu.addMenu("File")
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open Data File')
        openFile.triggered.connect(self.fileOpened)
        exitApp = QAction('Exit', self)
        exitApp.setShortcut('Ctrl+Q')
        exitApp.setStatusTip('Exit App')
        exitApp.triggered.connect(qApp.quit)

        fileMenu.addAction(openFile)
        fileMenu.addAction(exitApp)

        # Setting up data menu
        dataMenu = self.menu.addMenu("Data")
        dataMenu.addSection("Plot Graph with")

        viewStyle = QActionGroup(dataMenu)

        viewPoints = QAction('View Points', self, checkable=True)
        viewPoints.setShortcut('Ctrl+P')
        viewPoints.setStatusTip('View Points on graphs')
        viewPoints.triggered.connect(
            lambda: self.setPlotStyle(style='o',
                                      plotType='plot'))
        viewStyle.addAction(viewPoints)

        viewLines = QAction('View Lines', self, checkable=True)
        viewLines.setShortcut('Ctrl+L')
        viewLines.setStatusTip('View Lines on graphs')
        viewLines.triggered.connect(lambda: self.setPlotStyle(style='-'))
        viewStyle.addAction(viewLines)

        viewBoth = QAction('View Point and Lines', self, checkable=True)
        viewBoth.setShortcut('Ctrl+B')
        viewBoth.setStatusTip('View Both Lines and points on graphs')
        viewBoth.setChecked(True)
        viewBoth.triggered.connect(lambda: self.setPlotStyle(style='-o'))
        viewStyle.addAction(viewBoth)
        # viewStyle.triggered.connect(self.changeGraphSettings)
        dataMenu.addActions(viewStyle.actions())
        viewTrend = QActionGroup(dataMenu)

        viewData = QAction("View Data", self, checkable=True)
        viewData.setShortcut('Ctrl+D')
        viewData.setStatusTip('View Data')
        viewData.triggered.connect(self._main.sideMenu.viewModeChanged)
        viewData.setChecked(True)

        viewTest = QAction("View Trend", self, checkable=True)
        viewTest.setShortcut('Ctrl+T')
        viewTest.setStatusTip('View Trend Test')
        viewTest.triggered.connect(self._main.sideMenu.testChanged)

        dataMenu.addSection("View Data or Trend")
        viewTrend.addAction(viewData)
        viewTrend.addAction(viewTest)
        dataMenu.addActions(viewTrend.actions())

        if self.debug:
            debugMenu = self.menu.addMenu("Debug")

    def fileOpened(self):
        """
        File open dialog
        """
        files = QFileDialog.getOpenFileName(
                            self, 'Open profile', "",
                            filter=('Data Files (*.csv *.xls *.xlsx)'))
        if files[0]:
            self.data.importFile(files[0])
        self.importFileSignal.emit()


class MainWidget(QWidget):
    """
    Central widget of the main window.
    Consists of a sideMenu and a tabWidget with plot and table

    Note: Doesn't need to be a separate class.
    If merged with MainWindow class, will eliminate the need for signals

    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.sideMenu = SideMenu()
        self.plotAndTable = PlotAndTable()
        self.layout.addLayout(self.sideMenu, 20)
        self.layout.addWidget(self.plotAndTable, 80)
        self.setLayout(self.layout)


class SideMenu(QVBoxLayout):
    viewChangedSignal = pyqtSignal(str, int)
    runModelSignal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupSideMenu()

    def setupSideMenu(self):
        self.viewDataGroup = QGroupBox('Select, Analyze, and'
                                       'Subset Failure Data')
        self.viewDataGroup.setLayout(self.setupViewDataGroup())
        self.addWidget(self.viewDataGroup)

        self.applyModelsGroup = QGroupBox('Configure and Apply Models')
        self.applyModelsGroup.setLayout(self.setupApplyModelsGroup())
        self.addWidget(self.applyModelsGroup)

        # signals
        self.testSelect.currentIndexChanged.connect(self.testChanged)
        self.viewMode.currentIndexChanged.connect(self.viewModeChanged)
        self.sheetSelect.currentIndexChanged.connect(self.sheetChanged)
        self.addStretch(1)

    def setupApplyModelsGroup(self):
        applyModelsGroupLayout = QVBoxLayout()

        self.futurePredictionsInput = QLineEdit("1")
        self.futurePredictionsInput.setValidator(QIntValidator())

        self.modelListWidget = QListWidget()
        self.modelListWidget.addItems([model.name for model in
                                       models.modelList.values()])
        self.modelListWidget.setSelectionMode(
                                QAbstractItemView.ExtendedSelection)

        self.algoListWidget = QListWidget()
        self.algoListWidget.addItems([name for name in
                                      RootFind.bracketedAlgos +
                                      RootFind.nonbracketedAlgos])

        self.computeButton = QPushButton("Compute")
        self.computeButton.clicked.connect(self.runModels)

        applyModelsGroupLayout.addWidget(QLabel("Specify the number of "
                                                "failures\n into the "
                                                "future to predict"))
        applyModelsGroupLayout.addWidget(self.futurePredictionsInput)
        applyModelsGroupLayout.addWidget(QLabel("Select the models to apply \n"
                                                "Ctrl + click to select "
                                                "multiple models"))
        applyModelsGroupLayout.addWidget(self.modelListWidget)
        applyModelsGroupLayout.addWidget(QLabel("Select the root finding "
                                                "algorithm to apply"))
        applyModelsGroupLayout.addWidget(self.algoListWidget)

        applyModelsGroupLayout.addWidget(self.computeButton)

        return applyModelsGroupLayout

    def runModels(self):
        selectedFullNames = [item.text() for item in
                             self.modelListWidget.selectedItems()]
        modelsToRun = [model for model in models.modelList.values()
                       if model.name in selectedFullNames]
        if self.algoListWidget.selectedItems():
            algoToRun = self.algoListWidget.selectedItems()[0].text()
        self.runModelSignal.emit({'modelsToRun': modelsToRun,
                                  'algoToRun': algoToRun})

    def setupViewDataGroup(self):
        viewDataGroupLayout = QVBoxLayout()
        viewDataGroupLayout.addWidget(QLabel("Select Sheet"))

        self.sheetSelect = QComboBox()
        # self.sheetSelect.addItems(self.mainWindow.sheets)
        viewDataGroupLayout.addWidget(self.sheetSelect)

        viewDataGroupLayout.addWidget(QLabel("Failure Data View Mode"))
        self.viewMode = QComboBox()
        self.viewMode.addItems(["Cumulative", "Time Between Failures",
                                "Failure Intensity"])
        viewDataGroupLayout.addWidget(self.viewMode)

        self.testSelect = QComboBox()
        trendTests = {cls.__name__: cls for
                      cls in TrendTest.__subclasses__()}
        self.testSelect.addItems([test.name for test in
                                  trendTests.values()])
        viewDataGroupLayout.addWidget(self.testSelect)
        self.testSelect.setEnabled(False)
        return viewDataGroupLayout

    def viewModeChanged(self):
        self.testSelect.setEnabled(False)
        self.viewMode.setEnabled(True)
        log.info("Changed View mode to" + self.viewMode.currentText())
        self.viewChangedSignal.emit('view', self.viewMode.currentIndex())

    def testChanged(self):
        self.testSelect.setEnabled(True)
        self.viewMode.setEnabled(False)
        self.viewChangedSignal.emit('trend', self.testSelect.currentIndex())

    def sheetChanged(self):
        self.viewChangedSignal.emit('sheet', self.sheetSelect.currentIndex())

    # update any display that relies on data from outside the class
    def updateSheets(self):
        log.info("Updating Sheets")
        self.sheetSelect.clear()
        self.sheetSelect.addItems(self.mainWindow.sheets)
