import pytest
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from models.DSS import DSS
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

mylogger.info('\n###############\nStarting DSS Model Testing\n###############')

def setup_dss(dataResults):
    sheets = dataResults['Data.set'].to_numpy()
    aMLE = dataResults['DSS (aMLEs)'].to_numpy()
    bMLE = dataResults['DSS (bMLEs)'].to_numpy()

    DSS_list = []

    for sheet in sheets:
        rawData = pd.read_excel(fname, sheet_name=sheet)
        try:
            dss = DSS(data=rawData, rootAlgoName='bisect')
            dss.findParams(0)
        except:
            dss = None
        DSS_list.append(dss)
    return [DSS_list, aMLE, bMLE]

fname = "model_data.xlsx"
dataResults = pd.read_excel(fname, sheet_name='DSS')
sheets = dataResults['Data.set'].to_numpy()
DATA = setup_dss(dataResults)
Results_aMLE = []
Results_bMLE = []
for i in range(0, len(DATA[0])):
    try:
        Results_aMLE.append((DATA[0][i].aMLEs, DATA[1][i]))
        Results_bMLE.append((DATA[0][i].bMLEs, DATA[2][i]))
    except:
        mylogger.info('Error in Sheet number ' + sheets[i])


@pytest.mark.parametrize("test_input,expected", Results_aMLE)
def test_gm_d_mle(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5


@pytest.mark.parametrize("test_input,expected", Results_bMLE)
def test_gm_phi_mle(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5


def test_name():
    for dss in DATA[0]:
        try:
            assert dss.name == "Delayed S-shaped"
        except:
            pass