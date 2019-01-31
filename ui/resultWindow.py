from PyQt5.QtWidgets import QMainWindow, QMenuBar, QHBoxLayout, QWidget,\
                            QGroupBox, QListWidget, QAbstractItemView,\
                            QVBoxLayout, QLabel, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvas,\
                     NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
# from core.graphSettings import GraphSettings
from core.graphSettings import PlotSettings
from ui.commonWidgets import PlotAndTable


class ResultWindow(QWidget):
    def __init__(self, results, parent=None):
        super(ResultWindow, self).__init__(parent)
        self.results = results
        # self.graphSettings = GraphSettings()
        self.plotSettings = PlotSettings()

        self.setupWindow()
        self.show()

    def setupWindow(self):
        self.setWindowTitle('Result Window')
        # self.menu = self.menuBar()
        self.menu = QMenuBar(self)
        self.menu.addMenu('Plot')
        # self.setCentralWidget(self.setupCentralWidget())
        self.setupCentralWidget()
        self.plot = self.plotTableWidget.plotFigure.figure.subplots()
        self.updateUI()

    def updateUI(self):
        self.plot.clear()
        self.plotSettings.plotType = 'step'
        self.plot = self.plotSettings.generatePlot(self.plot,
                                                   self.results[0].data['FT'],
                                                   self.results[0].data['FN'],
                                                   title="Cumulative Failures "
                                                   "vs Cumulative Test Time",
                                                   xLabel="Cumulative Test "
                                                   "Time",
                                                   yLabel="Cumulative Failures"
                                                   )

        for i, model in enumerate(self.modelListWidget.selectedItems()):
            model_name = model.text()
            self.plotSettings.plotType = 'plot'
            self.plot = self.plotSettings.addLine(self.plot,
                                                  self.results[i].data['FT'],
                                                  self.results[i].MVFVal)
        self.plotTableWidget.plotFigure.figure.canvas.draw()

    def setupCentralWidget(self):
        self.plotTableWidget = PlotAndTable()
        layout = QHBoxLayout(self)
        layout.setMenuBar(self.menu)
        layout.addWidget(self.setupSideMenu(), 20)
        layout.addWidget(self.plotTableWidget, 80)

    def setupSideMenu(self):
        layout = QVBoxLayout()
        viewResultsGroup = QGroupBox('Display Model Results')
        layout.addWidget(QLabel('Choose one or more sets of model '
                                'results to display'))
        self.modelListWidget = QListWidget()
        self.modelListWidget.addItems([model.name for model in
                                       self.results])
        self.modelListWidget.setSelectionMode(
                                QAbstractItemView.ExtendedSelection)
        self.modelListWidget.itemSelectionChanged.connect(self.updateUI)
        layout.addWidget(self.modelListWidget)
        layout.addWidget(QLabel('Choose the type of plot'))
        plotTypeComboBox = QComboBox()
        plotTypeComboBox.addItems(['Cumulative Failures',
                                   'Times between failures',
                                   'Failure Intensity',
                                   'Reliability Growth'])
        layout.addWidget(plotTypeComboBox)
        viewResultsGroup.setLayout(layout)
        viewResultsGroup.setLayout(layout)
        return viewResultsGroup
