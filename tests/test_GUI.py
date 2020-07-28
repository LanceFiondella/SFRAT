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


app = QApplication(sys.argv)

class SFRATtest(unittest.TestCase):
    '''Testing the SFRAT GUI'''
    def setUp(self):
        """Creating the GUI"""
        self.form = ui.mainWindow.MainWindow()
    def test_defaults(self):
        ''' Test the GUI in it's defaul state'''
        self.assertEqual(self.form.title,'SFRAT')
        self.assertEqual(self.form.left,10)
        self.assertEqual(self.form.top,10)
        self.assertEqual(self.form.width,1080)
        self.assertEqual(self.form.height,720)



if __name__ == "__main__":
    unittest.main()