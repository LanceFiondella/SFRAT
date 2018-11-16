import pandas as pd
import numpy as np
import scipy.optimize

from core.model import Model
from core.rootFind import RootFind


class JM(Model):
    """
    Jelinski-Moranda Model


    """
    name = 'Jelinski-Moranda'

    def __init__(self, *args, **kwargs):
        """
        Initialize model

        Keyword Args:
        rootAlgoName: string that identifies root finding function
        """
        super().__init__(*args, **kwargs)
        self.n = len(self.data)
        self.interFailSum = self.data.IF.sum()
        self.rootFindFunc = RootFind(rootAlgoName=kwargs['rootAlgoName'],
                                     equation=self.MLEeq,
                                     data=self.data)

    def findParams(self):
        """
        Find parameters of the model

        This function gets called for all models regardless of type
        """
        self.N0MLE = self.calcN0MLE()
        self.phiMLE = self.calcPhi(self.N0MLE)
        self.MVFVal = self.MVF(self.N0MLE, self.phiMLE)

    def MVF(self, N0, phi):
        """
        Calculates the Mean Value Function (MVF) based on N0 and phi

        Args:
            N0: N0 value, usually N0MLE of type float
            phi: phi value, usually phiMLE of type float
        Returns:
            MVF values as numpy array
        """
        return N0*(1 - np.exp(-phi*self.data.FT))

    def FI(self, N0, phi):
        """
        Calculates Failure Intensity

        Args:
            N0: N0 value, usually N0MLE of type float
            phi: phi value, usually phiMLE of type float
        Returns:
            Failure Intensity as numpy array
        """
        return N0*phi*(np.exp(-phi*self.data.FT))

    def lnL(self, N0, phi):
        """
        Calculates Log Likelihood

        Args:
            N0: N0 value, usually N0MLE of type float
            phi: phi value, usually phiMLE of type float
        Returns:
            Log likelihood as float
        """
        N0Vector = [(N0 - i) for i in range(self.n)]
        secondTerm = np.sum(np.log(N0Vector))
        thirdTerm = (N0Vector * self.data.IF).sum()
        return self.n*np.log(phi) + secondTerm - (phi*thirdTerm)

    def reliability(self, fail_num, timeVec):
        np.exp(-self.phiMLE*(self.N0MLE - (fail_num-1))*timeVec)

    def MTTF(self):
        pass

    def finite_model(self):
        return True

    def MLEeq(self, N0):
        """
        Represents MLE eqation, used in root finding

        Args:
            N0: First parameter N0 of type float

        Returns:
            Value of MLE equation
        """
        rightTerm1 = np.array([(N0 - i) for i in range(self.n)], np.float)
        leftTerm = np.sum(np.reciprocal(rightTerm1))
        rightTermDenom = (self.data.IF.multiply(rightTerm1).sum())
        return leftTerm - ((self.n * self.interFailSum)/(rightTermDenom))

    def calcN0MLE(self):
        """
        Calculates the N0MLE using findEndpoints and MLEeq

        Returns:
            N0MLE of type float
        """
        N0MLE = self.rootFindFunc.findRoot()
        return N0MLE

    def calcPhi(self, N0):
        """
        Calculates the phi based on N0 value

        Args:
            N0: N0 value, usually N0MLE of type float

        Returns:
            Value of phi of type float
        """
        numer = np.sum(np.array([1/(N0 - i) for i in range(self.n)], np.float))
        return numer/self.interFailSum

    def MVF_cont(self, t, N0, phi):
        """
        Point value of Mean value function

        Args:
            t: time at which to calculate MVF
            N0: N0 value, usually N0MLE of type float
            phi: phi value, usually phiMLE of type float

        Returns:
            MVF for time t as float
        """
        return N0*(1-np.exp(-phi*t))


if __name__ == "__main__":
    fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheetname='SYS1')
    jm = JM(rawData, 'ridder')
    jm.run()
