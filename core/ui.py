# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 750)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("core/favicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.evalResults = QtWidgets.QFrame(self.centralwidget)
        self.evalResults.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.evalResults.setFrameShadow(QtWidgets.QFrame.Raised)
        self.evalResults.setObjectName("evalResults")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.evalResults)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.modelEvalTable = QtWidgets.QTableWidget(self.evalResults)
        self.modelEvalTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.modelEvalTable.setObjectName("modelEvalTable")
        self.modelEvalTable.setColumnCount(0)
        self.modelEvalTable.setRowCount(0)
        self.gridLayout_8.addWidget(self.modelEvalTable, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.evalResults, 0, 3, 1, 1)
        self.applyModels = QtWidgets.QFrame(self.centralwidget)
        self.applyModels.setStyleSheet("border:0")
        self.applyModels.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.applyModels.setFrameShadow(QtWidgets.QFrame.Raised)
        self.applyModels.setObjectName("applyModels")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.applyModels)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.modelTab = QtWidgets.QTabWidget(self.applyModels)
        self.modelTab.setObjectName("modelTab")
        self.plotModelTab = QtWidgets.QWidget()
        self.plotModelTab.setObjectName("plotModelTab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.plotModelTab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.modelTab.addTab(self.plotModelTab, "")
        self.dataModelTab = QtWidgets.QWidget()
        self.dataModelTab.setObjectName("dataModelTab")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.dataModelTab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.modelTable = QtWidgets.QTableWidget(self.dataModelTab)
        self.modelTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.modelTable.setObjectName("modelTable")
        self.modelTable.setColumnCount(0)
        self.modelTable.setRowCount(0)
        self.gridLayout_7.addWidget(self.modelTable, 0, 0, 1, 1)
        self.modelTab.addTab(self.dataModelTab, "")
        self.gridLayout_5.addWidget(self.modelTab, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.applyModels, 0, 1, 1, 1)
        self.analyzeData = QtWidgets.QFrame(self.centralwidget)
        self.analyzeData.setEnabled(True)
        self.analyzeData.setMouseTracking(False)
        self.analyzeData.setAutoFillBackground(False)
        self.analyzeData.setStyleSheet("border:0")
        self.analyzeData.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.analyzeData.setFrameShadow(QtWidgets.QFrame.Raised)
        self.analyzeData.setObjectName("analyzeData")
        self.gridLayout = QtWidgets.QGridLayout(self.analyzeData)
        self.gridLayout.setObjectName("gridLayout")
        self.analyzeTab = QtWidgets.QTabWidget(self.analyzeData)
        self.analyzeTab.setObjectName("analyzeTab")
        self.plotTab = QtWidgets.QWidget()
        self.plotTab.setObjectName("plotTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.plotTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.analyzeTab.addTab(self.plotTab, "")
        self.plotData = QtWidgets.QWidget()
        self.plotData.setObjectName("plotData")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.plotData)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.dataTable = QtWidgets.QTableWidget(self.plotData)
        self.dataTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.dataTable.setObjectName("dataTable")
        self.dataTable.setColumnCount(0)
        self.dataTable.setRowCount(0)
        self.gridLayout_4.addWidget(self.dataTable, 0, 0, 1, 1)
        self.analyzeTab.addTab(self.plotData, "")
        self.gridLayout.addWidget(self.analyzeTab, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.analyzeData, 0, 0, 1, 1)
        self.modelResults = QtWidgets.QFrame(self.centralwidget)
        self.modelResults.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.modelResults.setFrameShadow(QtWidgets.QFrame.Raised)
        self.modelResults.setObjectName("modelResults")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.modelResults)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.queryTable = QtWidgets.QTableWidget(self.modelResults)
        self.queryTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.queryTable.setObjectName("queryTable")
        self.queryTable.setColumnCount(0)
        self.queryTable.setRowCount(0)
        self.gridLayout_9.addWidget(self.queryTable, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.modelResults, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 31))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSelect_Sheet = QtWidgets.QMenu(self.menuFile)
        self.menuSelect_Sheet.setObjectName("menuSelect_Sheet")
        self.menuMode = QtWidgets.QMenu(self.menubar)
        self.menuMode.setObjectName("menuMode")
        self.menuViewAD = QtWidgets.QMenu(self.menubar)
        self.menuViewAD.setObjectName("menuViewAD")
        self.menuViewAM = QtWidgets.QMenu(self.menubar)
        self.menuViewAM.setObjectName("menuViewAM")
        self.menuViewQ = QtWidgets.QMenu(self.menubar)
        self.menuViewQ.setObjectName("menuViewQ")
        self.menuViewE = QtWidgets.QMenu(self.menubar)
        self.menuViewE.setObjectName("menuViewE")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAnalyzeData = QtWidgets.QAction(MainWindow)
        self.actionAnalyzeData.setCheckable(True)
        self.actionAnalyzeData.setObjectName("actionAnalyzeData")
        self.actionApplyModels = QtWidgets.QAction(MainWindow)
        self.actionApplyModels.setCheckable(True)
        self.actionApplyModels.setObjectName("actionApplyModels")
        self.actionModelResults = QtWidgets.QAction(MainWindow)
        self.actionModelResults.setCheckable(True)
        self.actionModelResults.setObjectName("actionModelResults")
        self.actionEvaluateModels = QtWidgets.QAction(MainWindow)
        self.actionEvaluateModels.setCheckable(True)
        self.actionEvaluateModels.setObjectName("actionEvaluateModels")
        self.actionCF = QtWidgets.QAction(MainWindow)
        self.actionCF.setCheckable(True)
        self.actionCF.setChecked(True)
        self.actionCF.setObjectName("actionCF")
        self.actionTBF = QtWidgets.QAction(MainWindow)
        self.actionTBF.setCheckable(True)
        self.actionTBF.setObjectName("actionTBF")
        self.actionFI = QtWidgets.QAction(MainWindow)
        self.actionFI.setCheckable(True)
        self.actionFI.setObjectName("actionFI")
        self.actionPlot_Points = QtWidgets.QAction(MainWindow)
        self.actionPlot_Points.setCheckable(True)
        self.actionPlot_Points.setObjectName("actionPlot_Points")
        self.actionPlot_Lines = QtWidgets.QAction(MainWindow)
        self.actionPlot_Lines.setCheckable(True)
        self.actionPlot_Lines.setObjectName("actionPlot_Lines")
        self.actionPlot_Both = QtWidgets.QAction(MainWindow)
        self.actionPlot_Both.setCheckable(True)
        self.actionPlot_Both.setChecked(True)
        self.actionPlot_Both.setObjectName("actionPlot_Both")
        self.actionPlot_Data = QtWidgets.QAction(MainWindow)
        self.actionPlot_Data.setObjectName("actionPlot_Data")
        self.actionLap = QtWidgets.QAction(MainWindow)
        self.actionLap.setCheckable(True)
        self.actionLap.setObjectName("actionLap")
        self.actionLapConf = QtWidgets.QAction(MainWindow)
        self.actionLapConf.setCheckable(False)
        self.actionLapConf.setObjectName("actionLapConf")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionPlot_Running_Average = QtWidgets.QAction(MainWindow)
        self.actionPlot_Running_Average.setObjectName("actionPlot_Running_Average")
        self.actionPlot_Laplace_Trend_Test = QtWidgets.QAction(MainWindow)
        self.actionPlot_Laplace_Trend_Test.setObjectName("actionPlot_Laplace_Trend_Test")
        self.actionArith = QtWidgets.QAction(MainWindow)
        self.actionArith.setCheckable(True)
        self.actionArith.setObjectName("actionArith")
        self.actionStartIndex = QtWidgets.QAction(MainWindow)
        self.actionStartIndex.setObjectName("actionStartIndex")
        self.actionStopIndex = QtWidgets.QAction(MainWindow)
        self.actionStopIndex.setObjectName("actionStopIndex")
        self.actionSelFFC = QtWidgets.QAction(MainWindow)
        self.actionSelFFC.setObjectName("actionSelFFC")
        self.actionSelFFD = QtWidgets.QAction(MainWindow)
        self.actionSelFFD.setObjectName("actionSelFFD")
        self.actionRun_Models = QtWidgets.QAction(MainWindow)
        self.actionRun_Models.setObjectName("actionRun_Models")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setCheckable(True)
        self.action.setObjectName("action")
        self.actionShow_Geometric = QtWidgets.QAction(MainWindow)
        self.actionShow_Geometric.setCheckable(True)
        self.actionShow_Geometric.setObjectName("actionShow_Geometric")
        self.actionShow_Goel_Ukumoto = QtWidgets.QAction(MainWindow)
        self.actionShow_Goel_Ukumoto.setCheckable(True)
        self.actionShow_Goel_Ukumoto.setObjectName("actionShow_Goel_Ukumoto")
        self.actionShow_Jelinski_Moranda = QtWidgets.QAction(MainWindow)
        self.actionShow_Jelinski_Moranda.setCheckable(True)
        self.actionShow_Jelinski_Moranda.setObjectName("actionShow_Jelinski_Moranda")
        self.actionShow_Weibull = QtWidgets.QAction(MainWindow)
        self.actionShow_Weibull.setCheckable(True)
        self.actionShow_Weibull.setObjectName("actionShow_Weibull")
        self.actionShowPlotData = QtWidgets.QAction(MainWindow)
        self.actionShowPlotData.setCheckable(True)
        self.actionShowPlotData.setChecked(True)
        self.actionShowPlotData.setObjectName("actionShowPlotData")
        self.actionModelPlaceholder = QtWidgets.QAction(MainWindow)
        self.actionModelPlaceholder.setVisible(False)
        self.actionModelPlaceholder.setObjectName("actionModelPlaceholder")
        self.actionShowPlotDataEnd = QtWidgets.QAction(MainWindow)
        self.actionShowPlotDataEnd.setCheckable(True)
        self.actionShowPlotDataEnd.setChecked(True)
        self.actionShowPlotDataEnd.setObjectName("actionShowPlotDataEnd")
        self.actionPlot_Points_2 = QtWidgets.QAction(MainWindow)
        self.actionPlot_Points_2.setCheckable(True)
        self.actionPlot_Points_2.setObjectName("actionPlot_Points_2")
        self.actionPlot_Lines_2 = QtWidgets.QAction(MainWindow)
        self.actionPlot_Lines_2.setCheckable(True)
        self.actionPlot_Lines_2.setObjectName("actionPlot_Lines_2")
        self.actionPlot_Both_2 = QtWidgets.QAction(MainWindow)
        self.actionPlot_Both_2.setCheckable(True)
        self.actionPlot_Both_2.setObjectName("actionPlot_Both_2")
        self.actionCF_2 = QtWidgets.QAction(MainWindow)
        self.actionCF_2.setCheckable(True)
        self.actionCF_2.setChecked(True)
        self.actionCF_2.setObjectName("actionCF_2")
        self.actionTBF_2 = QtWidgets.QAction(MainWindow)
        self.actionTBF_2.setCheckable(True)
        self.actionTBF_2.setObjectName("actionTBF_2")
        self.actionFI_2 = QtWidgets.QAction(MainWindow)
        self.actionFI_2.setCheckable(True)
        self.actionFI_2.setObjectName("actionFI_2")
        self.actionPlotRel = QtWidgets.QAction(MainWindow)
        self.actionPlotRel.setCheckable(True)
        self.actionPlotRel.setObjectName("actionPlotRel")
        self.actionSelRel = QtWidgets.QAction(MainWindow)
        self.actionSelRel.setVisible(False)
        self.actionSelRel.setObjectName("actionSelRel")
        self.actionQueryPlaceholder = QtWidgets.QAction(MainWindow)
        self.actionQueryPlaceholder.setVisible(False)
        self.actionQueryPlaceholder.setObjectName("actionQueryPlaceholder")
        self.actionSpecFC = QtWidgets.QAction(MainWindow)
        self.actionSpecFC.setObjectName("actionSpecFC")
        self.actionSpecRuntime = QtWidgets.QAction(MainWindow)
        self.actionSpecRuntime.setObjectName("actionSpecRuntime")
        self.actionDesRel = QtWidgets.QAction(MainWindow)
        self.actionDesRel.setObjectName("actionDesRel")
        self.actionSpecRelInt = QtWidgets.QAction(MainWindow)
        self.actionSpecRelInt.setObjectName("actionSpecRelInt")
        self.actionEvalPlaceholder = QtWidgets.QAction(MainWindow)
        self.actionEvalPlaceholder.setVisible(False)
        self.actionEvalPlaceholder.setObjectName("actionEvalPlaceholder")
        self.actionPSSEpct = QtWidgets.QAction(MainWindow)
        self.actionPSSEpct.setObjectName("actionPSSEpct")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuSelect_Sheet.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport)
        self.menuMode.addAction(self.actionAnalyzeData)
        self.menuMode.addAction(self.actionApplyModels)
        self.menuMode.addAction(self.actionModelResults)
        self.menuMode.addAction(self.actionEvaluateModels)
        self.menuViewAD.addAction(self.actionCF)
        self.menuViewAD.addAction(self.actionTBF)
        self.menuViewAD.addAction(self.actionFI)
        self.menuViewAD.addAction(self.actionLap)
        self.menuViewAD.addAction(self.actionArith)
        self.menuViewAD.addSeparator()
        self.menuViewAD.addAction(self.actionLapConf)
        self.menuViewAD.addSeparator()
        self.menuViewAD.addAction(self.actionPlot_Points)
        self.menuViewAD.addAction(self.actionPlot_Lines)
        self.menuViewAD.addAction(self.actionPlot_Both)
        self.menuViewAD.addSeparator()
        self.menuViewAD.addAction(self.actionStartIndex)
        self.menuViewAD.addAction(self.actionStopIndex)
        self.menuViewAM.addAction(self.actionModelPlaceholder)
        self.menuViewAM.addSeparator()
        self.menuViewAM.addAction(self.actionCF_2)
        self.menuViewAM.addAction(self.actionTBF_2)
        self.menuViewAM.addAction(self.actionFI_2)
        self.menuViewAM.addAction(self.actionPlotRel)
        self.menuViewAM.addSeparator()
        self.menuViewAM.addAction(self.actionSelRel)
        self.menuViewAM.addSeparator()
        self.menuViewAM.addAction(self.actionSelFFC)
        self.menuViewAM.addAction(self.actionSelFFD)
        self.menuViewAM.addSeparator()
        self.menuViewAM.addAction(self.actionPlot_Points_2)
        self.menuViewAM.addAction(self.actionPlot_Lines_2)
        self.menuViewAM.addAction(self.actionPlot_Both_2)
        self.menuViewAM.addSeparator()
        self.menuViewAM.addAction(self.actionShowPlotData)
        self.menuViewAM.addAction(self.actionShowPlotDataEnd)
        self.menuViewQ.addAction(self.actionQueryPlaceholder)
        self.menuViewQ.addSeparator()
        self.menuViewQ.addAction(self.actionSpecFC)
        self.menuViewQ.addAction(self.actionSpecRuntime)
        self.menuViewQ.addAction(self.actionDesRel)
        self.menuViewQ.addAction(self.actionSpecRelInt)
        self.menuViewE.addAction(self.actionEvalPlaceholder)
        self.menuViewE.addSeparator()
        self.menuViewE.addAction(self.actionPSSEpct)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())
        self.menubar.addAction(self.menuViewAD.menuAction())
        self.menubar.addAction(self.menuViewAM.menuAction())
        self.menubar.addAction(self.menuViewQ.menuAction())
        self.menubar.addAction(self.menuViewE.menuAction())

        self.retranslateUi(MainWindow)
        self.modelTab.setCurrentIndex(0)
        self.analyzeTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SFRAT"))
        self.modelTab.setTabText(self.modelTab.indexOf(self.plotModelTab), _translate("MainWindow", "Plot"))
        self.modelTab.setTabText(self.modelTab.indexOf(self.dataModelTab), _translate("MainWindow", "Data"))
        self.analyzeTab.setTabText(self.analyzeTab.indexOf(self.plotTab), _translate("MainWindow", "Plot"))
        self.analyzeTab.setTabText(self.analyzeTab.indexOf(self.plotData), _translate("MainWindow", "Data"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSelect_Sheet.setTitle(_translate("MainWindow", "Select Sheet"))
        self.menuMode.setTitle(_translate("MainWindow", "Mode"))
        self.menuViewAD.setTitle(_translate("MainWindow", "View"))
        self.menuViewAM.setTitle(_translate("MainWindow", "View"))
        self.menuViewQ.setTitle(_translate("MainWindow", "View"))
        self.menuViewE.setTitle(_translate("MainWindow", "View"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionAnalyzeData.setText(_translate("MainWindow", "Analyze Data"))
        self.actionApplyModels.setText(_translate("MainWindow", "Apply Models"))
        self.actionModelResults.setText(_translate("MainWindow", "Model Results"))
        self.actionEvaluateModels.setText(_translate("MainWindow", "Evaluate Models"))
        self.actionCF.setText(_translate("MainWindow", "Cumulative Failures"))
        self.actionTBF.setText(_translate("MainWindow", "Time Between Failures"))
        self.actionFI.setText(_translate("MainWindow", "Failure Intensity"))
        self.actionPlot_Points.setText(_translate("MainWindow", "Plot: Points"))
        self.actionPlot_Lines.setText(_translate("MainWindow", "Plot: Lines"))
        self.actionPlot_Both.setText(_translate("MainWindow", "Plot: Both"))
        self.actionPlot_Data.setText(_translate("MainWindow", "Plot: Data"))
        self.actionLap.setText(_translate("MainWindow", "Laplace Test"))
        self.actionLapConf.setText(_translate("MainWindow", "Laplace Confidence"))
        self.actionExport.setText(_translate("MainWindow", "Export..."))
        self.actionExport.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionPlot_Running_Average.setText(_translate("MainWindow", "Plot: Running Average"))
        self.actionPlot_Laplace_Trend_Test.setText(_translate("MainWindow", "Plot: Laplace Trend Test"))
        self.actionArith.setText(_translate("MainWindow", "Running Average"))
        self.actionStartIndex.setText(_translate("MainWindow", "Plot: Edit Start Index"))
        self.actionStopIndex.setText(_translate("MainWindow", "Plot: Edit Stop Index"))
        self.actionSelFFC.setText(_translate("MainWindow", "Select Future Fail Count"))
        self.actionSelFFD.setText(_translate("MainWindow", "Select Future Fail Duration"))
        self.actionRun_Models.setText(_translate("MainWindow", "Run Models"))
        self.action.setText(_translate("MainWindow", "Show S-Shape"))
        self.actionShow_Geometric.setText(_translate("MainWindow", "Show Geometric"))
        self.actionShow_Goel_Ukumoto.setText(_translate("MainWindow", "Show Goel-Ukumoto"))
        self.actionShow_Jelinski_Moranda.setText(_translate("MainWindow", "Show Jelinski-Moranda"))
        self.actionShow_Weibull.setText(_translate("MainWindow", "Show Weibull"))
        self.actionShowPlotData.setText(_translate("MainWindow", "Show Data on Plot"))
        self.actionModelPlaceholder.setText(_translate("MainWindow", "placeholder"))
        self.actionShowPlotDataEnd.setText(_translate("MainWindow", "Show Data End on Plot"))
        self.actionPlot_Points_2.setText(_translate("MainWindow", "Plot: Points"))
        self.actionPlot_Lines_2.setText(_translate("MainWindow", "Plot: Lines"))
        self.actionPlot_Both_2.setText(_translate("MainWindow", "Plot: Both"))
        self.actionCF_2.setText(_translate("MainWindow", "Cumulative Failures"))
        self.actionTBF_2.setText(_translate("MainWindow", "Time Between Failures"))
        self.actionFI_2.setText(_translate("MainWindow", "Failure Intensity"))
        self.actionPlotRel.setText(_translate("MainWindow", "Reliability"))
        self.actionSelRel.setText(_translate("MainWindow", "Select Reliability Interval"))
        self.actionQueryPlaceholder.setText(_translate("MainWindow", "modelSeparator"))
        self.actionSpecFC.setText(_translate("MainWindow", "Specify Failure Count"))
        self.actionSpecRuntime.setText(_translate("MainWindow", "Specify Additional Runtime"))
        self.actionDesRel.setText(_translate("MainWindow", "Specify Desired Reliability"))
        self.actionSpecRelInt.setText(_translate("MainWindow", "Specify Reliability Interval"))
        self.actionEvalPlaceholder.setText(_translate("MainWindow", "modelPlaceholder"))
        self.actionPSSEpct.setText(_translate("MainWindow", "Specify PSSE Percent"))
