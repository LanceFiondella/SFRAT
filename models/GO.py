import pandas as pd
import numpy as np
import scipy.optimize

from core.model import Model
from core.rootFind import RootFind


class GO(Model):
    """
    Goel-Okumoto Model

    """
    name = 'Goel-Okumoto'

    def __init__(self, *args, **kwargs):
        """
        Initialize model

        Keyword Args:
        rootAlgoName: string that identifies root finding function
        """
        super().__init__(*args, **kwargs)
        self.n = len(self.data)
        self.tn = self.data.FT[-1]
        self.sumT = self.data.FT.sum()
        # self.interFailSum = self.data.IF.sum()
        self.rootFindFunc = RootFind(rootAlgoName=kwargs['rootAlgoName'],
                                     equation=self.MLEeq,
                                     data=self.data)

    def findParams(self):
        """
        Find parameters of the model

        This function gets called for all models regardless of type
        """
        self.bHat = self.calcbHatMLE()
        self.aHat = self.calcaHatMLE(self.bHat)
        self.GOmvf = self.MVF(self.aHat, self.bHat, self.data.FT)
        self.GOfi = self.FI(self.aHat, self.bHat, self.data.FT)
        self.lnLval = self.lnL()

    def MVF(self, a, b, t):
        """
        Calculates the Mean Value Function (MVF) based on N0 and phi

        Args:
            a: number of latent faults, of type float
            b: fault detection rate, of type float
            t: failure time, of type float
        Returns:
            MVF values as float
        """
        return a * (1 - np.exp(-b * t))

    def FI(self, a, b, t):
        """
        Calculates Failure Intensity

        Args:
            a: number of latent faults, of type float
            b: fault detection rate, of type float
            t: failure time, of type float
        Returns:
            Failure Intensity as float
        """
        return a * b * np.exp(-b * t)

    def lnL(self):
        """
        Calculates Log Likelihood

        Returns:
            Log likelihood as float value
        """
        rightTerm = np.sum((np.log(self.FI(self.data.FT[i])) for i in range(self.n)))
        return -1 * (self.MVF(self.tn)) + rightTerm

    def MTTF(self):
        pass

    def finite_model(self):
        return True

    def MLEeq(self, b):
        """
        Represents MLE eqation, used in root finding

        Args:
            b: First parameter b of type float

        Returns:
            Value of MLE equation (bHat)
        """
        return ( self.n * self.tn * np.exp(-b * self.tn) ) / ( 1 - np.exp(-b * self.tn) ) + self.sumT - self.n / b

    def calcaHatMLE(self, b):
        """
        Calculates a parameter (the number of latent faults)

        Args:
            b: Parameter b (fault detection rate) of type float

        Returns:
            aHat of type float
        """
        return self.n / (1 - np.exp(-b * self.tn))

    def calcbHatMLE(self):
        """
        Calculates the MLE for the number of initial faults

        Returns:
            bHat of type float
        """
        bHat = self.rootFindFunc.findRoot()
        return bHat

if __name__ == "__main__":
    fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheetname='SYS1')
    go = GO(rawData, 'ridder')
    go.findParams()
