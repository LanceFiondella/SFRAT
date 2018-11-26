
import pandas as pd
import numpy as np
import logging as log


class Data:
    def __init__(self, data):
        self.setData(data)

    def setData(self, data):
        if 'FT' in data or 'IF' in data:
            self.processFT(data)
        elif 'FC' in data or 'CFC' in data:
            log.info(data)
            self.processFC(data)
        
    def processFT(self, data):
        # failure time
        if 'FT' not in data:
            data["FT"] = data["IF"].cumsum()

        # inter failure time
        elif 'IF' not in data:
            data['IF'] = data['FT'].diff()
            data['IF'].iloc[0] = data['FT'].iloc[0]

        if 'FN' not in data:
            data['FN'] = pd.Series([i+1 for i in range(data['FT'].size)])
        self.data = data
            

    def processFC(self, data):
        if 'FC' not in data:
            data['FC'] = data['CFC'].diff()
            data['FC'][0] = data['CFC'][0]
        elif 'CFC' not in data:
            data['CFC'] = data['FC'].cumsum()
        
        if 'T' not in data:
            data['T'] = pd.Series([i+1 for i in range(data['FC'].size)])
        
        FTData = pd.DataFrame()
        FT = []
        for i, fc in enumerate(data['FC']):
            if fc != 0:
                if i == 0:
                    fails = np.array([(j+0.5)*float(data['T'][i])/float(fc) for j in range(fc)])
                    for fail in fails:
                        FT.append(fail)
                elif i > 0:
                    fails = np.array([(j+0.5)*float(data['T'][i] - data['T'][i-1])/float(fc) for j in range(fc)])
                    for fail in fails:
                        FT.append(data['T'][i]+fail)
                

        FTData['FT'] = pd.Series(FT)
        self.processFT(FTData)



            



    def getIF(self):
        return self.data["IF"]

    def getFT(self):
        return self.data["FT"]

    def getFN(self):
        return self.data["FN"]

    def getData(self):
        return self.data
