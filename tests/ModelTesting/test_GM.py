import pytest
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from tests.ModelTesting.dataClass import Data
from models.GM import GM
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

mylogger.info('\n###############\nStarting GM Model Testing\n###############')

def setup_gm(Systemdata):
    """
    Reads in the expected data for the GM BM results for each excel sheet.
    Creates an instance of the JM Class for each sheet with the data
    :return:
    a list containing 3 lists
    1) a list of GM instances
    2) a list of expected N0
    3) a list of expected Phi
    """
    fname = "model_data.xlsx"
    dataResults = pd.read_excel(fname, sheet_name='GM_BM_Results')
    D0 = dataResults['D0'].to_numpy()
    Phi = dataResults['Phi'].to_numpy()

    gm_list = []

    # When Creating a instance of a model class, the DATA class is needed. For some datasets, the 'IF' column is missing which causes an error

    for sheet in Systemdata.sheetNames:
        rawData = Systemdata.dataSet[sheet]
        try:
            gm = GM(data=rawData, rootAlgoName='bisect')
            gm.findParams(0)
        except:
            pass
        gm_list.append(gm)
    return [gm_list, D0, Phi]


fname = "model_data.xlsx"
Systemdata = Data()
Systemdata.importFile(fname)
DATA = setup_gm(Systemdata)
Results_DMLE = []
Results_PhiMLE = []
for i in range(0, len(DATA[0])):
    try:
        Results_DMLE.append((DATA[0][i].DMLE, DATA[1][i],Systemdata.sheetNames[i]))
        Results_PhiMLE.append((DATA[0][i].phiMLE, DATA[2][i],Systemdata.sheetNames[i]))
    except:
        mylogger.info('Error in Sheet number ' + Systemdata.sheetNames[i])


@pytest.mark.parametrize("test_input,expected,SheetName", Results_DMLE)
def test_gm_d_mle(test_input, expected,SheetName):
    assert abs(test_input - expected) < 1


@pytest.mark.parametrize("test_input,expected,SheetName", Results_PhiMLE)
def test_gm_phi_mle(test_input, expected,SheetName):
    assert abs(test_input - expected) < 1


def test_name():
    for gm in DATA[0]:
        try:
            assert gm.name == "Geometric"
        except:
            pass

