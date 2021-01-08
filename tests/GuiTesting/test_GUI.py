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
from SFRAT import SFRAT
import pandas as pd
import pyautogui
import time





app = QApplication(sys.argv)

class SFRATtest(unittest.TestCase):
    '''Testing the SFRAT GUI'''
    def setUp(self):
        '''Creating the GUI'''
        self.form = SFRAT()
    def test_defaults(self):
        ''' Test the GUI in it's default state (Dimesions)'''
        self.assertEqual(self.form.windowTitle(),"SFRAT")
        self.assertEqual(self.form.width(),750)
        self.assertEqual(self.form.height(),750)
        self.assertEqual(self.form.menuFile.title(),"File")
        self.assertEqual(self.form.menuSelect_Sheet.title(),"Select Sheet")
        self.assertEqual(self.form.menuMode.title(),"Mode")
        self.assertEqual(self.form.menuViewAD.title(),"View")


    def test_AnalyzeDataTab(self):
        '''testing Data Analysis tab'''
        self.plotTableswitching(self.form.analyzeTab)
        self.importingExcel()
        self.form.actionCF.trigger()
        self.form.actionPlot_Points.trigger()
        self.form.actionPlot_Lines.trigger()
        self.form.plotStartIndex = 120
        self.form.plotStopIndex= 130
        self.form.redrawPlot()
        self.assertEqual(self.form.plotStartIndex, 120)
        self.form.actionTBF.trigger()
        self.assertEqual(self.form.plotStopIndex, 130)
        self.form.actionFI.trigger()
        self.form.actionLap.trigger()
        self.form.actionArith.trigger()



    def test_ApplyModelsTab(self):
        '''Testing Apply Models Tab'''
        self.form.show()
        self.plotTableswitching(self.form.modelTab)
        self.importingExcel()
        self.form.actionApplyModels.trigger()
        self.form.actionPlot_Points.trigger()
        self.form.actionPlot_Lines.trigger()
        self.form.actionPlot_Both.trigger()
        #self.ApplyModelsShowShapes()
        self.form.actionCF.trigger()
        self.form.actionTBF.trigger()
        self.form.actionFI.trigger()
        self.form.actionPlotRel.trigger()
        #self.form.actionSelFFC = ?     #Select future fail count
        #self.form.actionSelFFD = ?     #select future fail duration
        for i in range(1, len(self.form.curFileData.keys())):
            self.form.switchSheet(force=list(self.form.curFileData.keys())[i])
            self.ApplyModelsShowShapes()
        #app.exec_()


    def test_sheetselection(self):
        '''Testing sheet selction after importing excel spreadsheet'''
        self.importingExcel()
        for i in self.form.menuSelect_Sheet.actions():
            i.trigger()
            self.assertEqual(i.text() , list(self.form.curFileData.keys())[self.form.menuSelect_Sheet.actions().index(i)])




    def plotTableswitching(self,TabQwidget):
        self.importingExcel()
        TabQwidget.setCurrentIndex(1)
        TabQwidget.setCurrentIndex(0)
        self.importCSV()
        TabQwidget.setCurrentIndex(1)
        TabQwidget.setCurrentIndex(0)



    def importingExcel(self):
        fileName = "example_failure_data_sets.xlsx"
        self.form.curFilePath = fileName
        self.form.convertFileData(pd.read_excel(fileName, sheet_name=None, engine='openpyxl'))
        self.form.listModels()
        self.form.updateSheetSelect(self.form.curFileData)
        self.form.menuSelect_Sheet.menuAction().setVisible(True)
        self.form.switchSheet(force=list(self.form.curFileData.keys())[0])  # pick 1st sheet

    def importCSV(self):
        fileName = "example_failure_data_sets.csv"
        self.form.curFilePath = fileName
        self.form.convertFileData({"Sheet": pd.read_csv(fileName)})
        self.form.updateSheetSelect(self.form.curFileData)
        self.form.menuSelect_Sheet.menuAction().setVisible(False)
        self.form.statusBar.clearMessage()
        self.form.switchSheet(force=list(self.form.curFileData.keys())[0])  # pick 1st sheet

    def ApplyModelsShowShapes(self):
        # modelActions[] List that contains each Model in menuViewAM
        for i in range(6):
            self.form.modelActions[i].trigger()
            pyautogui.press('esc')


if __name__ == "__main__":
    unittest.main()
    