import pytest
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from models.JM import JM
import pandas as pd


def setup_jm():
    fname = "model_data.xlsx"
    dataResults = pd.read_excel(fname, sheet_name ='JM_BM_Results')
    sheets = dataResults['Data set'].to_numpy()
    N0 = dataResults['N0'].to_numpy()
    Phi = dataResults['Phi'].to_numpy()

    jm_list = []

    #When Creating a instance of a model class, the DATA class is needed. For some datasets, the 'IF' column is missing which causes an error

    for sheet in ['SYS1', 'SYS2', 'SYS3']:
        rawData = pd.read_excel(fname, sheet_name = sheet)
        jm = JM(data=rawData, rootAlgoName='bisect')
        jm.findParams(0)
        jm_list.append(jm)
    return [jm_list, N0, Phi]



DATA = setup_jm()
Results_N0MLE = []
Results_PhiMLE = []
for i in range(0, len(DATA[0])):
    Results_N0MLE.append((DATA[0][i].N0MLE, DATA[1][i]))
    Results_PhiMLE.append((DATA[0][i].phiMLE, DATA[2][i]))



@pytest.mark.parametrize("test_input,expected", Results_N0MLE)
def test_jm_n0_mle(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5


@pytest.mark.parametrize("test_input,expected", Results_PhiMLE)
def test_jm_phi_mle(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5



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