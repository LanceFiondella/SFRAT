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
        print(self.form.data.sheetNames)
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
        AllItems = [self.form.data.sheetNames.itemText(i) for i in range(self.form.data.sheetNames.count())]

    def test_default_tab1_failure_data_view_mode(self):
        ''' Test the default value for failure data view mode dropdown menu (Tab 1)'''
        pass

    def test_default_tab1_future_failure_predictions(self):
        ''' Test the default value for future failure text box (Tab 1)'''
        pass

    def test_default_tab1_model_select(self):
        ''' Test that by default none of the models are selected (Tab 1)'''
        pass

    def test_default_tab1_root_find_select(self):
        ''' Test that by default none of the root find options are selected (Tab 1)'''
        pass

    def test_import(self):
        ''' Testing importing file type'''
        self.form.data.importFile('model_data.xlsx')
        self.form.importFileSignal.emit()
        self.assertEqual(len(self.form.data.sheetNames), 37)


if __name__ == "__main__":
    unittest.main()