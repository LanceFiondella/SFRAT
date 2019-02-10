from PyQt5.QtWidgets import QMainWindow, QMenuBar, QHBoxLayout, QWidget,\
                            QGroupBox, QListWidget, QAbstractItemView,\
                            QVBoxLayout, QLabel, QComboBox, QAction, \
                            QActionGroup, QLineEdit, QTableView
from matplotlib.backends.backend_qt5agg import FigureCanvas,\
                     NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
# from core.graphSettings import GraphSettings
from core.graphSettings import PlotSettings
from ui.commonWidgets import PlotAndTable
from core.dataClass import PandasModel


class ResultWindow(QWidget):
    CUMULATIVE_FAILURES = 0
    TIMES_BETWEEN_FAILURES = 1
    FAILURE_INTENSITY = 2
    RELIABILITY_GROWTH = 3

    def __init__(self, results, data, predictPoints, sheetName="Raw Data", parent=None):
        super(ResultWindow, self).__init__(parent)
        self.results = results
        self.data = data
        self.predictPoints = predictPoints
        # self.graphSettings = GraphSettings()
        self.plotSettings = PlotSettings()
        self.currentPlotView = 0
        self.showRawData = True
        self.sheetName = sheetName
        self.setupWindow()
        self.show()

    def setupWindow(self):
        self.setWindowTitle('Result Window')
        self.setupMenu()
        self.setupCentralWidget()
        self.plot = self.plotTableWidget.plotFigure.figure.subplots()
        self.updateUI()

    def setupMenu(self):
        self.menu = QMenuBar(self)
        dataMenu = self.menu.addMenu('Plot')

        dataMenu.addSection("Plot Graph with")
        viewStyle = QActionGroup(dataMenu)
        viewPoints = QAction('View Points', self, checkable=True)
        viewPoints.setShortcut('Ctrl+P')
        viewPoints.setStatusTip('View Points on graphs')
        viewPoints.triggered.connect(
            lambda: self.setPlotStyle(style='o'))
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

        rawDataToggleAction = QAction('Show Raw Data', self, checkable=True)
        rawDataToggleAction.setShortcut('Ctrl+R')
        rawDataToggleAction.setStatusTip('Show raw data on plot')
        rawDataToggleAction.triggered.connect(self.toggleRawData)
        rawDataToggleAction.setChecked(True)
        dataMenu.addAction(rawDataToggleAction)

    def toggleRawData(self):
        if self.showRawData:
            self.showRawData = False
        else:
            self.showRawData = True
        self.updateUI()

    def setPlotStyle(self, style='-o'):
        self.plotSettings.style = style
        self.updateUI()

    def updateUI(self):
        self.changePlot(self.currentPlotView)

    def setupCentralWidget(self):
        self.plotTableWidget = PlotAndTable()
        self.predTableWidget = QTableView()
        self.plotTableWidget.addTab(self.predTableWidget, 'Prediction Table')
        layout = QHBoxLayout(self)
        layout.setMenuBar(self.menu)
        layout.addWidget(self.setupSideMenu(), 20)
        layout.addWidget(self.plotTableWidget, 80)

    def setupSideMenu(self):
        sideMenu = QWidget()
        sideMenuLayout = QVBoxLayout()
        # Setting up Display Model Results group
        viewResultsGroup = QGroupBox('Display Model Results')
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Specify number of failures to predict'))
        self.predictPointsTextbox = QLineEdit(str(self.predictPoints))
        layout.addWidget(self.predictPointsTextbox)

        layout.addWidget(QLabel('Choose the type of plot'))
        plotTypeComboBox = QComboBox()
        plotTypeComboBox.addItems(['Cumulative Failures',
                                   'Times between failures',
                                   'Failure Intensity',
                                   'Reliability Growth'])
        plotTypeComboBox.currentIndexChanged.connect(self.changePlot)
        layout.addWidget(plotTypeComboBox)

        layout.addWidget(QLabel('Specify interval length for reliability computation'))
        self.intervalLengthTextbox = QLineEdit(str(self.data.IF.iloc[-1]))
        self.intervalLengthTextbox.textChanged.connect(lambda: self.changePlot(self.currentPlotView))
        layout.addWidget(self.intervalLengthTextbox)

        layout.addWidget(QLabel('Choose one or more sets of model '
                                'results to display'))
        self.modelListWidget = QListWidget()
        self.modelListWidget.addItems([model.name for model in
                                       self.results.values() if model.converged])
        self.modelListWidget.setSelectionMode(
                                QAbstractItemView.MultiSelection)
        self.modelListWidget.itemSelectionChanged.connect(self.updateUI)
        layout.addWidget(self.modelListWidget)
        viewResultsGroup.setLayout(layout)

        # Setting up query results group
        queryResultsGroup = QGroupBox('Query Model Results')
        queryResultsGroupLayout = QVBoxLayout()
        queryResultsGroupLayout.addWidget(QLabel('Specify target reliability'))
        self.targetRelTextbox = QLineEdit('0.9')
        queryResultsGroupLayout.addWidget(self.targetRelTextbox)
        queryResultsGroupLayout.addWidget(QLabel('Specify mission time'))
        self.targetRelTextbox = QLineEdit(str(self.data.IF.iloc[-1]))
        queryResultsGroupLayout.addWidget(self.targetRelTextbox)
        queryResultsGroup.setLayout(queryResultsGroupLayout)

        sideMenuLayout.addWidget(viewResultsGroup)
        sideMenuLayout.addWidget(queryResultsGroup)

        sideMenu.setLayout(sideMenuLayout)
        return sideMenu

    def populateTables(self, fitTableData, predTableData):
        self.fitTable = pd.DataFrame.from_dict(fitTableData)
        self.predTable = pd.DataFrame.from_dict(predTableData, orient='index').T
        self.plotTableWidget.tableWidget.setModel(PandasModel(self.fitTable))
        self.predTableWidget.setModel(PandasModel(self.predTable)) 

    def changePlot(self, index):
        self.currentPlotView = index
        
        if index == self.RELIABILITY_GROWTH:
            self.intervalLengthTextbox.setEnabled(True)
        else:
            self.intervalLengthTextbox.setEnabled(False)
        self.plot.clear()

        if index == self.CUMULATIVE_FAILURES:
            # Cumulative Failures
            self.plot = self.plotSettings.setupPlot(self.plot, title="Cumulative Failures "
                                                    "vs Cumulative Test Time",
                                                    xLabel="Cumulative Test "
                                                    "Time",
                                                    yLabel="Cumulative Failures")
            fitTableData = {'Failure Time': self.data.FT,
                            'Failure Number': self.data.FN}
            predTableData = {'Failure Number': np.array([self.data.FN.iloc[-1]+i+1 
                                                         for i in range(self.predictPoints)])}

            if self.showRawData:
                self.plotSettings.plotType = 'step'
                self.plot = self.plotSettings.addLine(
                                                self.plot,
                                                self.data.FT,
                                                self.data.FN,
                                                label=self.sheetName
                                                )
            self.plot.axvline(x=self.data.FT.iloc[-1], color='black', linestyle='--')
            for i, model in enumerate(self.modelListWidget.selectedItems()):
                modelName = model.text()
                self.plotSettings.plotType = 'plot'
                predFailureTimes, failureNumbers  = self.results[modelName].MVFPlot()
                self.plot = self.plotSettings.addLine(
                                                self.plot,
                                                predFailureTimes,
                                                failureNumbers,
                                                label=modelName)
                fitTableData[modelName + "\nFailure Number"] = failureNumbers[:len(self.data.FN)]
                predTableData[modelName + "\nFailure Times"] = predFailureTimes[len(self.data.FN):]
            self.populateTables(fitTableData, predTableData)
            
        elif index == self.TIMES_BETWEEN_FAILURES:
            # Times between Failures
            self.plot = self.plotSettings.setupPlot(self.plot, title="Interfailure Times vs."
                                                    " Cumulative Test Time",
                                                    xLabel="Cumulative Test Time",
                                                    yLabel="Times between"
                                                    " successive failures")
            fitTableData = {'Failure Time': self.data.FT,
                            'InterFailure Times': self.data.IF}
            predTableData = {'Failure Number': np.array([self.data.FN.iloc[-1]+i+1 
                                                         for i in range(self.predictPoints)])}    
            if self.showRawData:
                self.plotSettings.plotType = 'step'
                self.plot = self.plotSettings.addLine(
                                                self.plot,
                                                self.data.FT,
                                                self.data.IF,
                                                label=self.sheetName
                                                )
            for i, model in enumerate(self.modelListWidget.selectedItems()):
                modelName = model.text()
                self.plotSettings.plotType = 'plot'
                predFailureTimes, MTTF = self.results[modelName].MTTFPlot()
                self.plot = self.plotSettings.addLine(
                                                self.plot,
                                                predFailureTimes,
                                                MTTF,
                                                label=self.results[modelName].name)
                fitTableData[modelName] = MTTF[:len(self.data.FN)]
                predTableData[modelName] = MTTF[len(self.data.FN):]
            self.populateTables(fitTableData, predTableData)
        elif index == self.FAILURE_INTENSITY:
            # Failure Intensity
            self.plot = self.plotSettings.setupPlot(self.plot, title="Failure Intensity vs."
                                                    " Cumulative Test Time",
                                                    xLabel="Cumulative Test Time",
                                                    yLabel="Failure Intensity")
            fitTableData = {'Failure Time': self.data.FT,
                            'Failure Intensity': 1/self.data.IF}
            predTableData = {'Failure Number': np.array([self.data.FN.iloc[-1]+i+1 
                                                         for i in range(self.predictPoints)])}
            if self.showRawData:
                self.plotSettings.plotType = 'step'
                self.plot = self.plotSettings.addLine(
                                                self.plot,
                                                self.data.FT,
                                                1/self.data.IF,
                                                label=self.sheetName)
            for i, model in enumerate(self.modelListWidget.selectedItems()):
                modelName = model.text()
                predFailureTimes, FI = self.results[modelName].FIPlot()
                self.plotSettings.plotType = 'plot'
                self.plot = self.plotSettings.addLine(
                                                self.plot,
                                                predFailureTimes,
                                                FI,
                                                label=self.results[modelName].name)
                fitTableData[modelName] = FI[:len(self.data.FN)]
                predTableData[modelName] = FI[len(self.data.FN):]
            self.populateTables(fitTableData, predTableData)
        elif index == self.RELIABILITY_GROWTH:
            # Reliability growth
            
            self.plot = self.plotSettings.setupPlot(self.plot, title="Reliability growth vs."
                                                    " Cumulative Test Time",
                                                    xLabel="Cumulative Test Time",
                                                    yLabel="Reliability Growth")
            fitTableData = {'Failure Time': self.data.FT}
            predTableData = {'Failure Number': np.array([self.data.FN.iloc[-1]+i+1 
                                                         for i in range(self.predictPoints)])}
            for i, model in enumerate(self.modelListWidget.selectedItems()):
                modelName = model.text()
                predFailureTimes, relGrowth = self.results[modelName].relGrowthPlot(
                                                    float(self.intervalLengthTextbox.text())
                                                    )
                self.plotSettings.plotType = 'plot'
                self.plot = self.plotSettings.addLine(
                                                self.plot,
                                                predFailureTimes,
                                                relGrowth,
                                                label=self.results[modelName].name)
                fitTableData[modelName + "\nReliability"] = relGrowth[:len(self.data.FT)]
                predTableData[modelName + "\nReliability"] = relGrowth[len(self.data.FT):]
            self.populateTables(fitTableData, predTableData)
        self.plot.legend()
        self.plotTableWidget.plotFigure.figure.canvas.draw()
