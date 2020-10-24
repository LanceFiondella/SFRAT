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
import SFRAT
import pandas as pd
import pyautogui
import time





app = QApplication(sys.argv)

class SFRATtest(unittest.TestCase):
    '''Testing the SFRAT GUI'''
    def setUp(self):
        '''Creating the GUI'''
        self.form = SFRAT.SFRAT()

    def test_defaults(self):
        ''' Test the GUI in it's default state (Dimesions)'''
        self.assertEqual(self.form.windowTitle(),"SFRAT")
        self.assertEqual(self.form.width(),750)
        self.assertEqual(self.form.height(),750)
        self.assertEqual(self.form.menuFile.title(),"File")
        self.assertEqual(self.form.menuSelect_Sheet.title(),"Select Sheet")
        self.assertEqual(self.form.menuMode.title(),"Mode")
        self.assertEqual(self.form.menuViewAD.title(),"View")

    def test_ExcelImporting(self):
        self.form.show()
        filename = "example_failure_data_sets.xlsx"
        command = 'echo ' + filename.strip() + '| clip'
        os.system(command)
        #self.form.menuFile.exec_()
        pyautogui.hotkey('ctrl','o')
        pyautogui.hotkey('ctrl', 'v')


        app.exec_()



if __name__ == "__main__":
    unittest.main()
