from PyQt5.QtWidgets import QWidget, QProgressBar, QLabel, QVBoxLayout,\
                            QTabWidget, QTableView
from PyQt5.QtCore import QThread, pyqtSignal

# Matplotlib Imports
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, \
                                    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class ComputeWidget(QWidget):
    results = pyqtSignal(dict)

    def __init__(self, modelsToRun, algoToRun, data, predictPoints, parent=None):
        super(ComputeWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, len(modelsToRun))
        self.label = QLabel()
        self.label.setText("Computing results, Models completed: ")

        layout.addWidget(self.label)
        layout.addWidget(self.progressBar)
        self.setWindowTitle("Processing")
        self.computeTask = TaskThread(modelsToRun, algoToRun, data, predictPoints)
        self.computeTask.modelFinished.connect(self.modelFinished)
        self.computeTask.taskFinished.connect(self.onFinished)
        self.computeTask.start()
        self.show()

    def onFinished(self, result):
        self.results.emit(result)
        self.close()

    def modelFinished(self):
        self.progressBar.setValue(self.progressBar.value() + 1)


class TaskThread(QThread):
    taskFinished = pyqtSignal(dict)
    modelFinished = pyqtSignal()

    def __init__(self, modelsToRun, algoToRun, data, predictPoints):
        super().__init__()
        self.modelsToRun = modelsToRun
        self.algoToRun = algoToRun
        self.data = data
        self.predictPoints = predictPoints

    def run(self):
        result = {}
        for model in self.modelsToRun:
            m = model(data=self.data.getData(), rootAlgoName=self.algoToRun)
            m.findParams(self.predictPoints)
            result[m.name] = m
            self.modelFinished.emit()
        self.taskFinished.emit(result)


class PlotAndTable(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setupPlotTab()
        self.setupTableTab()

    def setupPlotTab(self):
        # Creating plot widget
        self.plotWidget = QWidget()
        # Creating plot layout
        plotLayout = QVBoxLayout()
        self.figure = Figure(tight_layout={"pad": 2.0})
        self.plotFigure = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(self.plotFigure, self.plotWidget)
        plotLayout.addWidget(self.plotFigure, 1)
        plotLayout.addWidget(toolbar)
        self.plotWidget.setLayout(plotLayout)
        self.addTab(self.plotWidget, 'Plot')

    def setupTableTab(self):
        self.tableWidget = QTableView()
        self.addTab(self.tableWidget, 'Table')
