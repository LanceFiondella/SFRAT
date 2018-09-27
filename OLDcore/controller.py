import pandas as pd
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot


class Controller():
    
    
    def __init__(self):
        
        self.data = Data()

    def setData(self, fname):
        ext = fname[0].split('.')[-1]
        if ext == 'xlsx' or ext == 'xls':
            self.data.import_xls(fname[0])
        elif ext == 'csv':
            self.data.import_csv(fname[0])


    
class Data(QObject):
    multiSheets = pyqtSignal()
    singleSheet = pyqtSignal()
    
    def __init__(self):
        super(Data,self).__init__()
        self.dataFileType = None
    
    @property
    def rawData(self):
        return self._rawData

    @rawData.setter
    def rawData(self, rawData):
        self._rawData = rawData

    @property
    def currentTableIdx(self):
        return self._currentTableIdx
    
    #@pyqtSlot(int)
    @currentTableIdx.setter
    def currentTableIdx(self, idx):
        self._currentTableIdx = idx
    
    def import_xls(self, fname):
        self.rawData = pd.read_excel(fname, sheetname=None)
        self.dataFileType = 'excel'
        if len(self.rawData.keys()) > 1:
            self.sheetNames = list(self.rawData.keys())
            self.multiSheets.emit()
        else:
            self.singleSheet.emit()
        
    def import_csv(self, fname):
        self.rawData = pd.read_csv(fname)
        self.dataFileType = 'csv'
        self.singleSheet.emit()    

    