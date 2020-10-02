import pytest
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from models.DSS import DSS
from core.dataClass import Data
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

mylogger.info('\n###############\nStarting DSS Model Testing\n###############')

def setup_dss(Systemdata):
    fname = "model_data.xlsx"
    dataResults = pd.read_excel(fname, sheet_name='DSS')
    aMLE = dataResults['DSS (aMLEs)'].to_numpy()
    bMLE = dataResults['DSS (bMLEs)'].to_numpy()

    DSS_list = []

    for sheet in Systemdata.sheetNames:
        rawData = Systemdata.dataSet[sheet]
        try:
            dss = DSS(data=rawData, rootAlgoName='bisect')
            dss.findParams(0)
        except:
            pass
        DSS_list.append(dss)
    return [DSS_list, aMLE, bMLE]

fname = "model_data.xlsx"
Systemdata = Data()
Systemdata.importFile(fname)
DATA = setup_dss(Systemdata)
Results_aMLE = []
Results_bMLE = []
for i in range(0, len(DATA[0])):
    try:
        Results_aMLE.append((DATA[0][i].aMLE, DATA[1][i],Systemdata.sheetNames[i]))
        Results_bMLE.append((DATA[0][i].bMLE, DATA[2][i],Systemdata.sheetNames[i]))
    except:
        mylogger.info('Error in Sheet number ' + Systemdata.sheetNames[i])


@pytest.mark.parametrize("test_input,expected,SheetName", Results_aMLE)
def test_dss_a_mle(test_input, expected,SheetName):
    print("\n DSS A MLE " + SheetName)
    assert abs(test_input - expected) < 10 ** -5


@pytest.mark.parametrize("test_input,expected,SheetName", Results_bMLE)
def test_dss_b_mle(test_input, expected,SheetName):
    print("\n WEI B MLE " + SheetName)
    assert abs(test_input - expected) < 10 ** -5


def test_name():
    for dss in DATA[0]:
        try:
            assert dss.name == "Delayed S-shaped"
        except:
            pass