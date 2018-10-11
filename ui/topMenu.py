from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import logging as log


class TopMenu(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # create top menu buttons
        self.button1 = QPushButton("This is the ")
        self.button2 = QPushButton("Top Menu")

        # add onClick event handling
        self.button1.clicked.connect(self.b1Pressed)
        self.button2.clicked.connect(self.b2Pressed)

        # add to the menu
        self.addWidget(self.button1)
        self.addWidget(self.button2)

    def b1Pressed(self):
        log.info("Top Menu B1 Pressed! Doing what b1 does")

    def b2Pressed(self):
        log.info("Top Menu B2 Pressed! Doing what b2 does")
























#
