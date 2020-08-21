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
import pandas as pd


app = QApplication(sys.argv)

class SFRATtest(unittest.TestCase):
    '''Testing the SFRAT GUI'''
    def setUp(self):
        """Creating the GUI"""
        self.form = ui.mainWindow.MainWindow()
        print(self.form.data.sheetNames)

        self.allitems_default_sheetSelect = [self.form._main.sideMenu.sheetSelect.itemText(i) for i in
                    range(self.form._main.sideMenu.sheetSelect.count())]
        self.allitems_default_viewMode = [self.form._main.sideMenu.viewMode.itemText(i) for i in
                    range(self.form._main.sideMenu.viewMode.count())]

        xl = pd.ExcelFile('model_data.xlsx')
        self.sheets = len(xl.sheet_names)
    def test_default_dimesions(self):
        ''' Test the GUI in it's default state (Dimesions)'''
        self.assertEqual(self.form.title,'SFRAT')
        self.assertEqual(self.form.left,10)
        self.assertEqual(self.form.top,10)
        self.assertEqual(self.form.width,1080)
        self.assertEqual(self.form.height,720)

    def test_default_tab1_sheet_select(self):
        ''' Test the default value for sheet dropdown menu (Tab 1)'''
        self.assertEqual(len(self.form.data.sheetNames),1)
        #Check to make sure the dropdown menu is empty
        self.assertEqual(len(self.allitems_default_sheetSelect),0)

    def test_default_tab1_failure_data_view_mode(self):
        ''' Test the default value for failure data view mode dropdown menu (Tab 1)'''
        self.assertEqual(len(self.allitems_default_viewMode), 3)
        self.assertEqual(self.allitems_default_viewMode[0],"Cumulative")
        self.assertEqual(self.allitems_default_viewMode[1], "Time Between Failures")
        self.assertEqual(self.allitems_default_viewMode[2], "Failure Intensity")


    def test_default_tab1_future_failure_predictions(self):
        ''' Test the default value for future failure text box (Tab 1)'''
        self.assertEqual(self.form._main.sideMenu.futurePredictionsInput.text(),"1")

    def test_default_tab1_model_select(self):
        ''' Test that by default none of the models are selected (Tab 1)'''
        #No items should be selected by defult
        self.assertEqual(len(self.form._main.sideMenu.modelListWidget.selectedItems()),0)
        #There are by default 6 standard models
        self.assertEqual(self.form._main.sideMenu.modelListWidget.count(),6)

    def test_default_tab1_root_find_select(self):
        ''' Test that by default none of the root find options are selected (Tab 1)'''
        self.assertEqual(len(self.form._main.sideMenu.algoListWidget.selectedItems()), 0)

        self.assertEqual(self.form._main.sideMenu.algoListWidget.count(), 6)
    def test_import(self):
        ''' Testing importing file type'''
        self.form.data.importFile('model_data.xlsx')
        self.form.importFileSignal.emit()
        self.assertEqual(len(self.form.data.sheetNames), self.sheets)


if __name__ == "__main__":
    unittest.main()