import pytest
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from models.WEI import WEI
from tests.ModelTesting.dataClass import Data
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

mylogger.info('\n###############\nStarting Weibull Model Testing\n###############')

def setup_wei(Systemdata):
    fname = "model_data.xlsx"
    dataResults = pd.read_excel(fname, sheet_name='Weibull')
    aMLE = dataResults['a (MLE)'].to_numpy()
    bMLE = dataResults['b (MLE)'].to_numpy()
    cMLE = dataResults['c (MLE)'].to_numpy()

    WEI_list = []

    for sheet in Systemdata.sheetNames:
        rawData = Systemdata.dataSet[sheet]
        try:
            wei = WEI(data=rawData, rootAlgoName='bisect')
            wei.findParams(0)
        except:
            pass
        WEI_list.append(wei)
    return [WEI_list, aMLE, bMLE, cMLE]

fname = "model_data.xlsx"
Systemdata = Data()
Systemdata.importFile(fname)
DATA = setup_wei(Systemdata)
Results_aMLE = []
Results_bMLE = []
Results_cMLE = []
for i in range(0, len(DATA[0])):
    try:
        Results_aMLE.append((DATA[0][i].aMLE, DATA[1][i],Systemdata.sheetNames[i]))
        Results_bMLE.append((DATA[0][i].bMLE, DATA[2][i],Systemdata.sheetNames[i]))
        Results_cMLE.append((DATA[0][i].cMLE, DATA[3][i],Systemdata.sheetNames[i]))
    except:
        mylogger.info('Error in Sheet number ' + Systemdata.sheetNames[i])


@pytest.mark.parametrize("test_input,expected,SheetName", Results_aMLE)
def test_wei_a_mle(test_input, expected,SheetName):
    assert abs(test_input - expected) < 10 ** -5


@pytest.mark.parametrize("test_input,expected,SheetName", Results_bMLE)
def test_wei_b_mle(test_input, expected,SheetName):
    assert abs(test_input - expected) < 10 ** -5

@pytest.mark.parametrize("test_input,expected,SheetName", Results_cMLE)
def test_wei_c_mle(test_input, expected,SheetName):
    assert abs(test_input - expected) < 10 ** -5

def test_name():
    for wei in DATA[0]:
        try:
            assert wei.name == "Weibull"
        except:
            pass