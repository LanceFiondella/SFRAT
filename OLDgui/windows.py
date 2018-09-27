#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author: Venkateswaran Shekar (gv.shekar@gmail.com)
Main window for the tool
"""

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QDialog, QVBoxLayout,\
    QDialogButtonBox, QFileDialog, QTabWidget, QWidget, QTableWidget,\
    QTableWidgetItem, QGridLayout, QPushButton, QHBoxLayout, QHeaderView, QGroupBox,\
    QLabel, QComboBox, QSplitter, QLineEdit, QListView, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QStandardItem, QStandardItemModel
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QT5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from core import controller
from gui.maintabs import MainTab1, MainTab2, MainTab3


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.controller = controller.Controller()
        self.initUI()                       #Initializes UI
        #self.controller.multiSheets.connect(self.mainTabs.mainTab1.showSheets)
        #self.controller.singleSheet.connect(self.mainTabs.mainTab1.hideSheets)
        

    def initUI(self):
        self.statusBar().showMessage('Ready')   #Shows message at the bottom of window
        self.setGeometry(300, 300, 800, 600)    #Size of window
        self.setWindowTitle('SFRAT Python')     #Title
        self.initMenuBar()                      #Initializes menu bar
        self.initMainWindow()                   #Initializes main window
        self.setCentralWidget(self.mainWidget) #Sets the main_widget created in previous function in the center
        self.show()                             #Shows the window

    def initMenuBar(self):
        """
        This function sets up the menu bar with the Open File and Exit actions
        """
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl-Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)

        openProjectAction = QAction('&Open Input File',self)
        openProjectAction.setShortcut('Ctrl-O')
        openProjectAction.setStatusTip('Opens an existing input file')
        openProjectAction.triggered.connect(self.openProject)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openProjectAction)
        fileMenu.addAction(exitAction)
    
    def openProject(self):
        """
        This function start the Opens File Dialog and stores the file name in fname
        """
        fname = QFileDialog.getOpenFileName(self, 'Open File','.', filter='*.xlsx *.csv')
        print(fname)
        if len(fname[0]) > 0:
            self.controller.setData(fname)
            
        
    def initMainWindow(self):
        """
        This function initializes the main window and fills it with a graph plot with random data
        """
        self.mainWidget = QWidget(self)
      
        self.mainTabs = MainTabs(self.controller)
        
        
        layoutfig = QVBoxLayout()
        layoutfig.addWidget(self.mainTabs)
        self.mainWidget.setLayout(layoutfig)


class MainTabs(QTabWidget):
    def __init__(self, controller):
        super(MainTabs,self).__init__()
        self.controller = controller
        self.initTabs()

    def initTabs(self):
        self.mainTab1 = MainTab1(self.controller)
        self.mainTab2 = MainTab2(self.controller)
        self.mainTab3 = MainTab3(self.controller)
        self.addTab(self.mainTab1, 'Select, Analyze and Filter Data')
        self.addTab(self.mainTab2, 'Configure and Apply Models')
        self.addTab(self.mainTab3, 'Query Model Results')
        

