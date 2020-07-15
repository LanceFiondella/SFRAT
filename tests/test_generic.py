import pytest
import os, sys, inspect
from core.model import Model
from core.dataClass import Data
import models
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()
mylogger.info('\n###############\nStarting Generic Testing\n###############')


"""
ISSUES: models.modelList is displaying the correct contents for some reason. It works when tested in the console but not on this script
"""



#DATA SETUP
def setup_data():
    return Data()

sample_data = setup_data()
sample_data.importFile("model_data.xlsx")


#Model List Setup
print(models.modelList.values())
sample_models = []
for values in models.modelList.values():
    sample_models.append(values(data=pd.read_excel("model_data.xlsx"), rootAlgoName='bisect'))

print(sample_models)


#Testing data class property types
def test_data_sheets():
    assert type(sample_data.sheetNames) is list
    for sheet in sample_data.sheetNames:
        assert type(sheet) is str


def test_data_current_sheet():
    assert type(sample_data._currentSheet) is int

"""
def test_data_dataSet():
    assert type(sample_data.dataSet) is dict
    for key, value in sample_data.dataSet:
        assert type(key) is str
"""


#Testing model property types
def test_models_names():
    assert type(sample_models[0].name) is str


def test_models_params():
    for model in sample_models:
        assert type(model.params) is dict
        for key, value in model.params:
            assert type(key) is str
            assert type(value) is float

def test_models_root_name():
    for model in sample_models:
        assert type(model.rootAlgoName) is str

def test_models_coverged():
    for model in sample_models:
        assert type(model.converged) is bool

#Testing functions in models
def test_models_findParams():
    for model in sample_models:
        assert 'findParams' in dir(model)
