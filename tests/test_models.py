import pytest
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from models.JM import JM
import pandas as pd


@pytest.fixture
def import_data():
    fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheet_name='SYS1')
    return rawData


@pytest.fixture
def setup_jm(import_data):
    jm = JM(data=import_data, rootAlgoName='bisect')
    jm.findParams(0)
    return jm


def test_jm_n0_mle(setup_jm):
    assert abs(setup_jm.N0MLE - 141.902891867) < 10**-5


def test_jm_phi_mle(setup_jm):
    assert abs(setup_jm.phiMLE - 3.4966515966450457e-05) < 10**-5


def test_jm_mvf_last(setup_jm):
    assert abs(setup_jm.MVFVal[-1] - 135.516034) < 10**-5


def test_name(setup_jm):
    assert setup_jm.name == "Jelinski-Moranda"
