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
		self.addWidget(self.button1)
		self.addWidget(self.button2)
		self.addStretch(1)

	def b1Pressed(self):
		QMessageBox.about(self, "You Pressed Button 1", "Dont Push me bro")



























#
