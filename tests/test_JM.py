import pytest
import pandas as pd
import logging
import os,sys,inspect
### Changes the curretnt working directory so the imports Work
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from models.JM import JM


logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()


def setup_jm(dataResults):
    """
    Reads in the expected data for the JM BM results for each excel sheet.
    Creates an instance of the JM Class for each sheet with the data
    :return:
    a list containing 3 lists
    1) a list of JM instances
    2) a list of expected N0
    3) a list of expected Phi
    """
    sheets = dataResults['Data set'].to_numpy()
    N0 = dataResults['N0'].to_numpy()
    Phi = dataResults['Phi'].to_numpy()

    jm_list = []

    #When Creating a instance of a model class, the DATA class is needed. For some datasets, the 'IF' column is missing which causes an error

    for sheet in sheets:
        rawData = pd.read_excel(fname, sheet_name = sheet)
        try:
            jm = JM(data=rawData, rootAlgoName='bisect')
            jm.findParams(0)
        except:
            jm = None
        jm_list.append(jm)
    return [jm_list, N0, Phi]


'''
create tuples that would be ran each as individual test 
'''
fname = "model_data.xlsx"
dataResults = pd.read_excel(fname, sheet_name='JM_BM_Results')
sheets = dataResults['Data set'].to_numpy()
DATA = setup_jm(dataResults)
Results_N0MLE = []
Results_PhiMLE = []
for i in range(0, len(DATA[0])):
    try:
        Results_N0MLE.append((DATA[0][i].N0MLE, DATA[1][i]))
        Results_PhiMLE.append((DATA[0][i].phiMLE, DATA[2][i]))
    except:
        mylogger.info('Error in Sheet number ' + sheets[i])




@pytest.mark.parametrize("test_input,expected", Results_N0MLE)
def test_jm_n0_mle(test_input, expected):

    assert abs(test_input - expected) < 10 ** -5


@pytest.mark.parametrize("test_input,expected", Results_PhiMLE)
def test_jm_phi_mle(test_input, expected):
    assert abs(test_input - expected) < 10 ** -5

def test_name():
    for jm in DATA[0]:
        try:
            assert jm.name == "Jelinski-Moranda"
        except:
            pass


