from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import logging as log




class SideMenu(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.button1 = QPushButton("This is the ")
        self.button2 = QPushButton("Side Menu")

        self.button1.clicked.connect(self.b1Pressed)
        self.button2.clicked.connect(self.b2Pressed)

        self.addWidget(self.button1)
        self.addWidget(self.button2)
        self.addStretch(1)

    def b1Pressed(self):
        log.info("Side Menu B1 Pressed! Doing what b1 does")
    def b2Pressed(self):
        log.info("Side Menu B2 Pressed! Doing what b2 does")



























#
