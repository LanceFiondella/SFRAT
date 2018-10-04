from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import logging as log




class TopMenu(QHBoxLayout):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.button1 = QPushButton("This is the ")
		self.button2 = QPushButton("Top Menu")
		self.addWidget(self.button1)
		self.addWidget(self.button2)



























#
