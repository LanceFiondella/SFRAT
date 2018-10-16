from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import logging as log




class SideMenu(QVBoxLayout):
    def __init__(self, container):
        super().__init__()
        self.initUI()
        self.container = container

    def initUI(self):
        self.button1 = QPushButton("This is the ")
        self.button2 = QPushButton("Side Menu")
        self.fileOpenButton = QPushButton("Open A File!")

        self.button1.clicked.connect(self.b1Pressed)
        self.button2.clicked.connect(self.b2Pressed)
        self.fileOpenButton.clicked.connect(self.fileOpenPressed)

        self.addWidget(self.button1)
        self.addWidget(self.button2)
        self.addWidget(self.fileOpenButton)
        self.addStretch(1)

    def b1Pressed(self):
        log.info("Side Menu B1 Pressed! Doing what b1 does")

    def b2Pressed(self):
        log.info("Side Menu B2 Pressed! Doing what b2 does")

    def fileOpenPressed(self):
        # open a file dialog
        files = QFileDialog.getOpenFileName(
            self.container, 'Open profile', "",
            filter=('Data Files (*.csv *.xls *.xlsx)'))
        if files[0]:
            log.info("Opening:" + files[0])
























#
