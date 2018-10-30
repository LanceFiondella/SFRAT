
import pandas as pd
import numpy as np

class Data:
    def __init__(self, data):
        self.setData(data)

    def setData(self, data):
        # failure time
        if not 'FT' in data:
               data['FT'] = data['IF']
               for i in range(1,len(data)):
                   data['FT'][i] += data['FT'][i-1]

        # inter failure time
        elif not 'IF' in data:
            data['IF'] = data['FT']
            for i in range(len(data)-1,0,-1):
                data['IF'][i] -= data['IF'][i-1]
        self.data = data

        # cumulative time used for plotting
        if not "CT" in data:
            data["CT"] = data["FN"]
            data["CT"][0] = 0
            for i in range(1, len(data)):
                data["CT"][i] = data["CT"][i - 1] + data["IF"][i]

    def getIF(self):
        return self.data["IF"]

    def getFT(self):
        return self.data["FT"]

    def getFN(self):
        return self.data["FN"]

    def getCT(self):
        return self.data["CT"]

    def getData(self):
        return self.data
