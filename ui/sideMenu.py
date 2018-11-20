from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import logging as log
import os

import numpy as np
import pandas as pd

import models
from core.graphSettings import GraphSettings

from core.dataClass import Data


class SideMenu(QVBoxLayout):
    DATA_MENU = 0
    MODEL_MENU = 1
    def __init__(self, container, mainWindow, menuStyle):
        super().__init__()
        self.container = container
        self.filename = "No File Opened"
        self.menuStyle = menuStyle
        self.mainWindow = mainWindow

        self.initUI()

    def initUI(self):
        if self.menuStyle == self.DATA_MENU:
            self.dataUI()
        elif self.menuStyle == self.MODEL_MENU:
            self.modelUI()

    def dataUI(self):

        self.addWidget(QLabel("Select Sheet"))

        self.sheetSelect = QComboBox()
        self.sheetSelect.addItems(self.mainWindow.sheets)
        self.addWidget(self.sheetSelect)

        self.addWidget(QLabel("Failure Data View Mode"))
        self.viewMode = QComboBox()
        self.viewMode.addItems(["Cumulative", "Time Between Failures", \
        "Failure Intensity"])
        self.addWidget(self.viewMode)

        self.testSelect = QComboBox()
        self.testSelect.addItems(["Laplace Test", "Running Average Test"])
        self.addWidget(self.testSelect)

        # signals
        self.viewMode.currentIndexChanged.connect(self.viewModeChanged)
        self.sheetSelect.currentIndexChanged.connect(self.sheetChanged)
        self.testSelect.currentIndexChanged.connect(self.testChanged)

        self.addStretch(1)



    def modelUI(self):
        self.button1 = QPushButton("This is the ")
        self.button2 = QPushButton("Model Menu")
        self.modelSelect = QComboBox()

        # add models to model select
        # get a list of all models by name
        modelList = sorted(models.modelList.keys())
        # insert the null model at index 0 so it's at the top
        self.modelSelect.addItems(modelList)

        # signals
        self.modelSelect.currentIndexChanged.connect(self.modelChanged)

        self.addWidget(self.button1)
        self.addWidget(self.button2)
        self.addWidget(self.modelSelect)
        self.addStretch(1)

    def modelChanged(self):
        selected = self.modelSelect.currentText()
        log.info("Model Changed to " + selected)
        self.container.model = self.models.models[selected]
        self.container.updateGraph()

    def viewModeChanged(self):
        log.info("Changed View mode to" + self.viewMode.currentText())
        if self.viewMode.currentText() == "Cumulative":
            m = GraphSettings.CUMULATIVE
        elif self.viewMode.currentText() == "Time Between Failures":
            m = GraphSettings.TBF
        elif self.viewMode.currentText() == "Failure Intensity":
                m = GraphSettings.FINTENSITY

        self.mainWindow.dataTab.graphSettings.dataMode = m
        self.mainWindow.updateGraphs()

    def sheetChanged(self):
        if self.sheetSelect.currentText() != "No Sheets" \
        and len(self.mainWindow.sheets) > 1 \
        and self.sheetSelect.currentText(): # this is to ignore the update from clear
            self.mainWindow.data = Data(self.mainWindow.fullDataSet[\
            self.sheetSelect.currentText()])
            self.mainWindow.updateGraphs()



    # update any display that relies on data from outside the class
    def updateSheets(self):
        log.info("Updating Sheets")
        self.sheetSelect.clear()
        self.sheetSelect.addItems(self.mainWindow.sheets)

    def testChanged(self):
        if self.testSelect.currentText() == "Laplace Test":
            self.mainWindow.dataTab.graphSettings.test = GraphSettings.LAPLACE
        elif self.testSelect.currentText() == "Running Average Test":
            self.mainWindow.dataTab.graphSettings.test = GraphSettings.RAA
        self.mainWindow.updateGraphs()















#
