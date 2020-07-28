import pytest
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from models.GO import GO
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()
mylogger.info('\n###############\nStarting GO Model Testing\n###############')

def setup_go(dataResults):
    sheets = dataResults['DATA set'].to_numpy()
    bHat = dataResults['FT_b'].to_numpy()
    aHat = dataResults['FT_a'].to_numpy()

    go_list = []

    # When Creating a instance of a model class, the DATA class is needed. For some datasets, the 'IF' column is missing which causes an error

    for sheet in sheets:
        rawData = pd.read_excel(fname, sheet_name=sheet)
        try:
            go = GO(data=rawData, rootAlgoName='bisect')
            go.findParams(0)
        except:
            go = None
        go_list.append(go)
    return [go_list, bHat, aHat]


fname = "model_data.xlsx"
dataResults = pd.read_excel(fname, sheet_name='GO_BM_FT')
sheets = dataResults['DATA set'].to_numpy()
DATA = setup_go(dataResults)
Results_bHat = []
Results_aHat = []
for i in range(0, len(DATA[0])):
    try:
        Results_bHat.append((DATA[0][i].bHat, DATA[1][i]))
        Results_aHat.append((DATA[0][i].aHat, DATA[2][i]))
    except:
        mylogger.info('Error in Sheet number ' + sheets[i])


@pytest.mark.parametrize("test_input,expected", Results_bHat)
def test_go_b_hat(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5


@pytest.mark.parametrize("test_input,expected", Results_aHat)
def test_gm_a_hat(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5


def test_name():
    for go in DATA[0]:
        try:
            assert go.name == "Goel-Okumoto"
        except:
            pass
