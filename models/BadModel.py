#This is a template model
# it doesnt pay any attention to the data provided
# it just returns a linear regression from
# the first point to the last point

import pandas as pd
import numpy as np

class BadModel:
    # init should take no arguments
    # try to limit the processing nessisary in init to keep load time low
    name = "Bad Model"
    def __init__(self):
        pass
    # this is the function called by the UI to get the graph of the model
    # this should take one argument in the form of a pandas DataFrame
    # this will have 3 colums called FN, FT, IF
    # this should return a DataFrame with 2 colums titled X and Y
    def crunch(self, data):
        m =  data["FN"].iloc[-1] - data["FN"][0]
        m /= data["FT"].iloc[-1] - data["FT"][0]
        out = pd.DataFrame({
        "X": np.linspace(0, data["FT"].iloc[-1], 100),
        "Y": m * np.linspace(0, data["FT"].iloc[-1], 100),
        })
        return out
