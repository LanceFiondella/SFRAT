
import pandas as pd
import numpy as np
import logging as log
from PyQt5 import QtCore, QtGui
import os.path


class Data:
    def __init__(self):
        """
        Class that stores input data
        This class will handle data import using: Data.importFile(filename)
        Dataframes will be stored as a dictionary.
        With sheet names as keys and pandas DataFrame as values
        This class will keep track of the currently selected sheet
        and will return that sheet when getData() method is called
        """
        self.sheetNames = ['None']
        self._currentSheet = 0
        self.dataSet = {'None': None}

    @property
    def currentSheet(self):
        return self._currentSheet

    @currentSheet.setter
    def currentSheet(self, index):
        if index < len(self.sheetNames) and index >= 0:
            self._currentSheet = index
        else:
            self._currentSheet = 0

    def setData(self, dataSet):
        """
        Processes raw sheet data into data required by models
        Args:
            dataSet: Dictionary of raw data imported in importFile()
        """
        for sheet, data in dataSet.items():
            if 'FT' in data or 'IF' in data:
                dataSet[sheet] = self.processFT(data)
            elif 'FC' in data or 'CFC' in data:
                dataSet[sheet] = self.processFC(data)
        self.dataSet = dataSet

    def processFT(self, data):
        """
        Processes raw FT data to fill in any gaps
        Args:
            data: Raw pandas dataframe
        Returns:
            data: Processed pandas dataframe
        """
        # failure time
        if 'FT' not in data:
            data["FT"] = data["IF"].cumsum()

        # inter failure time
        elif 'IF' not in data:
            data['IF'] = data['FT'].diff()
            data['IF'].iloc[0] = data['FT'].iloc[0]

        if 'FN' not in data:
            data['FN'] = pd.Series([i+1 for i in range(data['FT'].size)])
        return data

    def processFC(self, data):
        """
        Processes raw FC data to fill in any gaps
        Args:
            data: Raw pandas dataframe
        Returns:
            data: Processed pandas dataframe
        """
        if 'FC' not in data:
            data['FC'] = data['CFC'].diff()
            data['FC'][0] = data['CFC'][0]
        elif 'CFC' not in data:
            data['CFC'] = data['FC'].cumsum()
        if 'T' not in data:
            data['T'] = pd.Series([i+1 for i in range(data['FC'].size)])
        FTData = pd.DataFrame()
        FT = []
        for i, fc in enumerate(data['FC']):
            if fc != 0:
                if i == 0:
                    fails = np.array([(j+0.5)*float(data['T'][i]) /
                                     float(fc) for j in range(int(fc))])
                    for fail in fails:
                        FT.append(fail)
                elif i > 0:
                    fails = np.array([(j+0.5)*float(data['T'][i] -
                                      data['T'][i-1]) /
                                     float(fc) for j in range(int(fc))])
                    for fail in fails:
                        FT.append(data['T'][i]+fail)
        FTData['FT'] = pd.Series(FT)
        data = self.processFT(FTData)
        return data

    def getData(self):
        """
        Returns dataframe corresponding to the currentSheet index
        """
        return self.dataSet[self.sheetNames[self._currentSheet]]

    def getDataModel(self):
        """
        Returns PandasModel for the current dataFrame to be displayed
        on a QTableWidget
        """
        return PandasModel(self.getData())

    def importFile(self, fname):
        """
        Imports data file
        Args:
            fname : File name of csv or excel file
        """
        self.filename, fileExtension = os.path.splitext(fname)
        if fileExtension == ".csv":
            data = {}
            data['None'] = pd.read_csv(fname)
        else:
            data = pd.read_excel(fname, sheet_name=None)
        self.sheetNames = list(data.keys())
        self._currentSheet = 0
        self.setData(data)


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.values[index.row()][index.column()]
                ))
        return QtCore.QVariant()

    def headerData(self, section, QtOrientation, role=QtCore.Qt.DisplayRole):
        if (QtOrientation == QtCore.Qt.Horizontal and
           role == QtCore.Qt.DisplayRole):
            columnNames = list(self._data)
            return QtCore.QVariant(str(columnNames[section]))
        return QtCore.QVariant()
