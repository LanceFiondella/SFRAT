import pytest
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from models.ISS import ISS
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

mylogger.info('\n###############\nStarting ISS Model Testing\n###############')

def setup_iss(dataResults):
    sheets = dataResults['ISS Model'].to_numpy()
    aMLE = dataResults['a (MLE)'].to_numpy()
    bMLE = dataResults['b (MLE)'].to_numpy()
    cMLE = dataResults['c (MLE)'].to_numpy()

    #aMLE=round(aMLE,1)
    #bMLE=round(bMLE,1)
    #cMLE=round(cMLE,1)

    ISS_list = []

    for sheet in sheets:
        rawData = pd.read_excel(fname, sheet_name=sheet)
        try:
            iss = ISS(data=rawData, rootAlgoName='bisect')
            iss.findParams(0)
        except:
            iss = None
        ISS_list.append(iss)
    return [ISS_list, aMLE, bMLE, cMLE]

fname = "model_data.xlsx"
dataResults = pd.read_excel(fname, sheet_name='ISS')
sheets = dataResults['ISS Model'].to_numpy()
DATA = setup_iss(dataResults)
Results_aMLE = []
Results_bMLE = []
Results_cMLE = []
for i in range(0, len(DATA[0])):
    try:
        Results_aMLE.append((DATA[0][i].aMLE, DATA[1][i]))
        Results_bMLE.append((DATA[0][i].bMLE, DATA[2][i]))
        Results_cMLE.append((DATA[0][i].cMLE, DATA[3][i]))
    except:
        mylogger.info('Error in Sheet number ' + sheets[i])


@pytest.mark.parametrize("test_input,expected", Results_aMLE)
def test_iss_a_mle(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5


@pytest.mark.parametrize("test_input,expected", Results_bMLE)
def test_iss_b_mle(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5

@pytest.mark.parametrize("test_input,expected", Results_cMLE)
def test_iss_c_mle(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5

def test_name():
    for iss in DATA[0]:
        try:
            assert iss.name == "ISS"
        except:
            pass