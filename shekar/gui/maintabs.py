from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QDialog, QVBoxLayout,\
    QDialogButtonBox, QFileDialog, QTabWidget, QWidget, QTableWidget,\
    QTableWidgetItem, QGridLayout, QPushButton, QHBoxLayout, QHeaderView, QGroupBox,\
    QLabel, QComboBox, QSplitter, QLineEdit, QListView, QCheckBox

from PyQt5.QtGui import QStandardItem, QStandardItemModel
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QT5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot



class MainTab1(QWidget):
    def __init__(self, controller):
        super(MainTab1,self).__init__()
        self.controller = controller
        layout = QHBoxLayout()
        #Defining left panel
        self.leftPanel = QWidget()
        leftPanelLayout = self.leftPanelLayoutGenerator()
        self.leftPanel.setLayout(leftPanelLayout)
        
        #Defining right panel
        self.rightPanel = PlotTableTab('Plot', 'Data and Trend Test Table')
        
        #Adding splitter between widgets
        splitter = QSplitter()
        splitter.addWidget(self.leftPanel)
        splitter.addWidget(self.rightPanel)
        layout.addWidget(splitter)

        self.setLayout(layout)

    def leftPanelLayoutGenerator(self):
        leftPanelLayout = QVBoxLayout()

        self.chooseSheetLabel = QLabel('Choose the data sheet to view')
        self.sheetOptions = QComboBox()
        #self.sheetOptions.activated.connect(self.controller.data.currentTableIdx)
        self.sheetOptions.activated.connect(self.drawPlot)

        chooseViewLabel = QLabel('Choose a view of the failure data')
        self.viewOptions = QComboBox()
        self.viewOptions.addItems(['Cumulative Failures', 'Times Between Failures', 'Failure Intensity'])

        choosePlotLabel = QLabel('Choose plot type')
        self.plotOptions = QComboBox()
        self.plotOptions.addItems(['Points and Lines', 'Points only', 'Lines only'])

        chooseDataLabel = QLabel('Plot Data or Trend Test?')
        self.dataOptions = QComboBox()
        self.dataOptions.addItems(['Data', 'Trend test'])

        chooseRelGrowthLabel = QLabel('Does data show reliability growth?')
        self.relGrowthOptions = QComboBox()
        self.relGrowthOptions.addItems(['Laplace Test', 'Running Arithmetic Average'])

        laplaceLabel = QLabel('Specify the confidence interval for the Laplace test')
        self.laplaceValue = QLineEdit()
        
        leftPanelLayout.addWidget(self.chooseSheetLabel)
        leftPanelLayout.addWidget(self.sheetOptions)
        leftPanelLayout.addWidget(chooseViewLabel)
        leftPanelLayout.addWidget(self.viewOptions)
        leftPanelLayout.addWidget(choosePlotLabel)
        leftPanelLayout.addWidget(self.plotOptions)
        leftPanelLayout.addWidget(chooseDataLabel)
        leftPanelLayout.addWidget(self.dataOptions)
        leftPanelLayout.addWidget(chooseRelGrowthLabel)
        leftPanelLayout.addWidget(self.relGrowthOptions)
        leftPanelLayout.addWidget(laplaceLabel)
        leftPanelLayout.addWidget(self.laplaceValue)
        leftPanelLayout.addStretch(2)

        self.chooseSheetLabel.hide()
        self.sheetOptions.hide()

        return leftPanelLayout

    def showSheets(self):
        self.sheetOptions.addItems(self.controller.sheetNames)
        self.chooseSheetLabel.show()
        self.sheetOptions.show()

    def hideSheets(self):
        self.chooseSheetLabel.hide()
        self.sheetOptions.hide()

    @pyqtSlot(int)
    def drawPlot(self, idx):
        print('Drawing Plot')
        sheetName = self.controller.sheetNames[idx]
        print("Sheet name: {}".format(sheetName))
        self.rightPanel.ax.clear()
        self.rightPanel.ax.step(self.controller.raw_data[sheetName]['FT'], self.controller.raw_data[sheetName]['FN'] )
        #self.rightPanel.ax.show()



class MainTab2(QWidget):
    def __init__(self, controller):
        super(MainTab2, self).__init__()
        self.controller = controller
        self.initTab()
        self.populateAvailModels()

    def initTab(self):
        #Defining left panel
        layout = QHBoxLayout()
        self.leftPanel = QWidget()
        leftPanelLayout = self.leftPanelLayoutGenerator()
        self.leftPanel.setLayout(leftPanelLayout)
        
        #Defining right panel
        self.rightPanel = PlotTableTab('Model Result Plot', 'Model Result Table')
        
        #Adding splitter between widgets
        splitter = QSplitter()
        splitter.addWidget(self.leftPanel)
        splitter.addWidget(self.rightPanel)
        layout.addWidget(splitter)

        self.setLayout(layout)

    def leftPanelLayoutGenerator(self):
        leftPanelLayout = QVBoxLayout()
        numFailLabel = QLabel('Specify the number of predicted failures')
        self.numFail = QLineEdit()
        chooseModelLabel = QLabel('Choose one or more models to run')
        self.modelView = QListView()
        self.runModelButton = QPushButton('Run Selected Models')
        runGroup = QGroupBox('Configure and Run models')
        runGroupLayout = QVBoxLayout()
        runGroupLayout.addWidget(numFailLabel)
        runGroupLayout.addWidget(self.numFail)
        runGroupLayout.addWidget(chooseModelLabel)
        runGroupLayout.addWidget(self.modelView)
        runGroupLayout.addWidget(self.runModelButton)
        runGroup.setLayout(runGroupLayout)
        
        displayGroup = QGroupBox('Display Model Results')
        displayGroupLayout = QVBoxLayout()
        chooseModelLabel = QLabel('Choose one or more models to display')
        self.displayModelView = QListView()
        choosePlotLabel = QLabel('Choose the type of plot for model results')
        self.plotType = QComboBox()
        self.plotType.addItems(['Cumulative Failures', 'Times Between Failures', 'Failure Intensity', 'Reliability Growth'])
        enterDurationLabel = QLabel('Enter the duration for which the model result curves\n should extend beyond the last prediction point')
        self.duration = QLineEdit()
        self.rawDataCheck = QCheckBox('Show raw data on plot')
        choosePlotOptionsLabel = QLabel('Choose plot type')
        self.plotOptions = QComboBox()
        self.plotOptions.addItems(['Points and Lines', 'Points only', 'Lines only'])

        displayGroupLayout.addWidget(chooseModelLabel)
        displayGroupLayout.addWidget(self.displayModelView)
        displayGroupLayout.addWidget(choosePlotLabel)
        displayGroupLayout.addWidget(self.plotType)
        displayGroupLayout.addWidget(enterDurationLabel)
        displayGroupLayout.addWidget(self.duration)
        displayGroupLayout.addWidget(self.rawDataCheck)
        displayGroupLayout.addWidget(choosePlotOptionsLabel)
        displayGroupLayout.addWidget(self.plotOptions)

        displayGroup.setLayout(displayGroupLayout)

        leftPanelLayout.addWidget(runGroup)
        leftPanelLayout.addWidget(displayGroup)

        return leftPanelLayout

    def populateAvailModels(self, modelNames=[]):
        #Temporary, must be removed 
        modelNames = ['Delayed S-Shape', 'Geometric', 'Goel-Okumoto', 'Jelinski-Moranda', 'Weibull']
        self.itemModel = QStandardItemModel()
        for model in modelNames:
            item = QStandardItem(model)
            item.setCheckable(True)
            item.setEditable(False)
            #item.setSelectable(True)
            self.itemModel.appendRow(item)
        self.modelView.setModel(self.itemModel)
        self.modelView.clicked.connect(self.checkIfClicked)

    def checkIfClicked(self, idx):
        print("clicked!")
        item = self.itemModel.item(idx.row())
        print(item.checkState())
        if item.checkState() == 0:
            item.setCheckState(2)
        else:
            item.setCheckState(0)


class MainTab3(QWidget):
    def __init__(self, controller):
        super(MainTab3, self).__init__()
        self.controller = controller
        self.initTab()

    def initTab(self):
        layout = QHBoxLayout()
        self.leftPanel = QWidget()
        leftPanelLayout = self.leftPanelLayoutGenerator()
        self.leftPanel.setLayout(leftPanelLayout)

        self.rightPanel = QWidget()
        rightPanelLayout = self.rightPanelLayoutGenerator()
        self.rightPanel.setLayout(rightPanelLayout)

        splitter = QSplitter()
        splitter.addWidget(self.leftPanel)
        splitter.addWidget(self.rightPanel)
        layout.addWidget(splitter)
        self.setLayout(layout)


    def leftPanelLayoutGenerator(self):
        leftPanelLayout = QVBoxLayout()
        chooseModelLabel = QLabel('Choose one or more model results to display')
        self.modelView = QListView()
        numFailLabel = QLabel('Specify the number of failures that are to be observed')
        self.numFail = QLineEdit()
        addTimeLabel = QLabel('Specify amount of additional time for which the software will run')
        self.addTime = QLineEdit()
        reliabilityLabel = QLabel('Specify the desired reliability')
        self.reliability = QLineEdit()
        intervalLabel = QLabel('Specify the length of the interval for which the reliabilty will be computed')
        self.interval = QLineEdit()
        fileOutputLabel = QLabel('Select the format of output file')
        self.fileOutput = QComboBox()
        self.fileOutput.addItems(['CSV', 'PDF'])
        self.saveButton = QPushButton('Save Model Predictions')

        leftPanelLayout.addWidget(chooseModelLabel)
        leftPanelLayout.addWidget(self.modelView)
        leftPanelLayout.addWidget(numFailLabel)
        leftPanelLayout.addWidget(self.numFail)
        leftPanelLayout.addWidget(addTimeLabel)
        leftPanelLayout.addWidget(self.addTime)
        leftPanelLayout.addWidget(reliabilityLabel)
        leftPanelLayout.addWidget(self.reliability)
        leftPanelLayout.addWidget(intervalLabel)
        leftPanelLayout.addWidget(self.interval)
        leftPanelLayout.addWidget(fileOutputLabel)
        leftPanelLayout.addWidget(self.fileOutput)
        leftPanelLayout.addWidget(self.saveButton)

        return leftPanelLayout

    def rightPanelLayoutGenerator(self):
        rightPanelLayout = QVBoxLayout()
        self.table = QTableWidget(10, 10)
        rightPanelLayout.addWidget(self.table)

        return rightPanelLayout




class PlotTableTab(QTabWidget):
    """
    This Widget can be used in all the tabs because they contain a plot on the first tab and table on the second
    """
    def __init__(self, plotName, tableName):
        super(PlotTableTab,self).__init__()
        #Setup figure
        self.plot = QWidget()
        fig = plt.figure()
        self.canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(self.canvas, self.plot)
        self.ax = fig.add_subplot(111)
        self.ax.legend()
        self.ax.set_xlabel("Dummy")
        self.ax.set_ylabel("Dummy")
        plt.grid(True)
        plt.tight_layout()
        self.canvas.draw()
        layoutfig = QVBoxLayout()
        layoutfig.addWidget(toolbar)
        layoutfig.addWidget(self.canvas, 1)
        
        self.plot.setLayout(layoutfig)
        self.addTab(self.plot, plotName)

        #Setup table
        self.table = QTableWidget(10, 10)
        
        self.addTab(self.table, tableName)