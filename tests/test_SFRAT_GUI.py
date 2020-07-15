import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
### Changes the curretnt working directory so the imports Work
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import ui.mainWindow

'''Testing the SFRAT GUI'''

form = ui.mainWindow.MainWindow()

def test_defaults():
    ''' Test the GUI in it's defaul state'''
    assert form.title == 'SFRAT'
    assert form.left == 10
    assert form.top == 10
    assert form.width == 1080
    assert form.height == 720



