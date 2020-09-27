import pytest
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from models.WEI import WEI
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

mylogger.info('\n###############\nStarting Weibull Model Testing\n###############')

def setup_wei(dataResults):
    sheets = dataResults['Weibull'].to_numpy()
    aMLE = dataResults['a (MLE)'].to_numpy()
    bMLE = dataResults['b (MLE)'].to_numpy()
    cMLE = dataResults['c (MLE)'].to_numpy()

    WEI_list = []

    for sheet in sheets:
        rawData = pd.read_excel(fname, sheet_name=sheet)
        try:
            wei = WEI(data=rawData, rootAlgoName='bisect')
            wei.findParams(0)
        except:
            wei = None
        WEI_list.append(wei)
    return [WEI_list, aMLE, bMLE, cMLE]

fname = "model_data.xlsx"
dataResults = pd.read_excel(fname, sheet_name='Weibull')
sheets = dataResults['Weibull'].to_numpy()
DATA = setup_wei(dataResults)
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
def test_wei_a_mle(test_input, expected):
    mylogger.info("****************************")
    mylogger.info(test_input)
    mylogger.info(expected)
    assert abs(test_input - expected) < 10 ** -5


@pytest.mark.parametrize("test_input,expected", Results_bMLE)
def test_wei_b_mle(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5

@pytest.mark.parametrize("test_input,expected", Results_cMLE)
def test_wei_c_mle(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5

def test_name():
    for wei in DATA[0]:
        try:
            assert wei.name == "Weibull"
        except:
            pass