#This is a template model
# it doesnt pay any attention to the data provided
# it just returns a linear regression from
# the first point to the last point

import pandas as pd
import numpy as np

class NullModel():
    def __init__(self):
        self.name = "No Model"

    def crunch(self, data):
        out = pd.DataFrame({"X": np.array([np.nan, np.nan]),\
        "Y": np.array([np.nan, np.nan])})
        return out
