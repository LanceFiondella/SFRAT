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

def setup_go():
    fname = "model_data.xlsx"
    dataResults = pd.read_excel(fname, sheet_name='GO_BM_FT')
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


DATA = setup_go()
Results_bHat = []
Results_aHat = []
for i in range(0, len(DATA[0])):
    try:
        Results_bHat.append((DATA[0][i].bHat, DATA[1][i]))
        Results_aHat.append((DATA[0][i].aHat, DATA[2][i]))
    except:
        pass

print(Results_bHat)
print(Results_aHat)
@pytest.mark.parametrize("test_input,expected", Results_bHat)
def test_go_b_hat(test_input, expected):
    mylogger.info('IN TEST')
    assert abs(test_input - expected) < 10 ** -5


@pytest.mark.parametrize("test_input,expected", Results_aHat)
def test_gm_a_hat(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5


def test_name(setup_go):
    assert setup_go.name == "Goel-Okumoto"


'''                                                                                                                                               
def test_jm_n0_mle(setup_jm):                                                                                                                     
    for i in range(0, len(setup_jm[0])):                                                                                                          
        assert abs(setup_jm[0][i].N0MLE - setup_jm[1][i]) < 10**-5                                                                                


def test_jm_phi_mle(setup_jm):                                                                                                                    
    assert abs(setup_jm.phiMLE - 3.4966515966450457e-05) < 10**-5                                                                                 


def test_jm_mvf_last(setup_jm):                                                                                                                   
    assert abs(setup_jm.MVFVal[-1] - 135.516034) < 10**-5                                                                                         


def test_name(setup_jm):                                                                                                                          
    assert setup_jm.name == "Jelinski-Moranda"                                                                                                    
'''