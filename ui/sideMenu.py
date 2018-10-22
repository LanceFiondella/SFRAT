from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import logging as log
import os

import numpy as np
import pandas as pd

from models import Models


class SideMenu(QVBoxLayout):
    DATA_MENU = 0
    MODEL_MENU = 1
    def __init__(self, container, menuStyle):
        super().__init__()
        self.container = container
        self.filename = "No File Opened"
        self.models = Models.Models()
        self.menuStyle = menuStyle

        self.initUI()

    def initUI(self):
        if self.menuStyle == self.DATA_MENU:
            self.dataUI()
        elif self.menuStyle == self.MODEL_MENU:
            self.modelUI()

    def dataUI(self):
        self.button1 = QPushButton("This is the ")
        self.button2 = QPushButton("Data Menu")

        # signals

        self.addWidget(self.button1)
        self.addWidget(self.button2)
        self.addStretch(1)


    def modelUI(self):
        self.button1 = QPushButton("This is the ")
        self.button2 = QPushButton("Model Menu")
        self.fileOpenButton = QPushButton("Open A File!")
        self.modelSelect = QComboBox()

        # add models to model select
        # get a list of all models by name
        modelList = sorted(self.models.models.keys())
        # insert the null model at index 0 so it's at the top
        modelList.remove("No Model")
        modelList.insert(0, "No Model")
        self.modelSelect.addItems(modelList)

        # signals
        self.fileOpenButton.clicked.connect(self.fileOpenPressed)
        self.modelSelect.currentIndexChanged.connect(self.modelChanged)

        self.addWidget(self.button1)
        self.addWidget(self.button2)
        self.addWidget(self.fileOpenButton)
        self.addWidget(self.modelSelect)
        self.addStretch(1)


    def fileOpenPressed(self):
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
            self.container.updateGraph()


    def modelChanged(self):
        selected = self.modelSelect.currentText()
        log.info("Model Changed to " + selected)
        self.container.model = self.models.models[selected]
        self.container.updateGraph()
























#
