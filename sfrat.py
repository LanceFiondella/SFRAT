#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from gui import windows
from PyQt5.QtCore import Qt
import os

"""
This file starts the program
"""

if __name__ == '__main__':
    os.environ["QT_SCALE_FACTOR"] = "1.0"
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    window = windows.MainWindow()
    sys.exit(app.exec_())
