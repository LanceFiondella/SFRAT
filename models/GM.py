import pandas as pd
import numpy as np
import scipy.optimize

from core.model import Model
from core.rootFind import RootFind


class GM(Model):
    """
    Geometric Model


    """
    name = 'Geometric'

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
        self.phiMLE = self.calcphiMLE()
        self.DHat = self.calcDMLE(self.phiMLE)
        self.lnLval = self.lnL(self.DHat, self.phiMLE)
        self.MVFval = self.MVF(self.DHat, self.phiMLE)

    def lnL(self, DHat, phi):
        """
        Calculates Log Likelihood

        Args:
            DHat: DHat value, 
            phi: phi value, usually phiMLE of type float
        Returns:
            Log likelihood as float
        """
        
        iVector = [(i) for i in range(self.n)]
        secondTerm = np.sum(iVector * np.log(phi))
        thirdTerm = (np.power(phi, iVector) * self.data.IF).sum()
        return self.n * np.log(DHat) + secondTerm - (DHat * thirdTerm)

    def MVF(self, DHat, phi):
        """
        Calculates the Mean Value Function (MVF) based on DHat and phi

        Args:
            DHat: DHat value, 
            phi: phi value, usually phiMLE of type float
        Returns:
            MVF values as numpy array
        """
        return -(np.log(1 - (DHat * self.data.IF * np.log(phi))/phi)/np.log(phi))

    def FI(self, N0, phi):
        pass

    def MLEeq(self, phi):
        """
        Represents MLE eqation, used in root finding

        Args:
            N0: First parameter N0 of type float

        Returns:
            Value of MLE equation
        """
        iVector = [(i) for i in range(self.n)]
        rightTerm = self.calcDMLE(phi) * (iVector * np.power(phi, iVector) * self.data.IF).sum()
        leftTerm = np.sum(iVector/phi)
        return leftTerm - rightTerm

    def calcDMLE(self, phi):
        """
        Calculates the Dparam value using phi

        Returns:
            Dparam of type float
        """
        iVector = [i for i in range(self.n)]
        denom = (np.power(phi, iVector) * self.data.IF).sum()
        return (self.n * phi)/denom

    def calcphiMLE(self):
        """
        Calculates the N0MLE using findEndpoints and MLEeq

        Returns:
            N0MLE of type float
        """
        phiMLE = self.rootFindFunc.findRoot()
        return phiMLE

    def reliability(self, fail_num, timeVec):
        pass

    def MTTF(self):
        pass

    def finite_model(self):
        pass


if __name__ == "__main__":
    fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheetname='SYS1')
    gm = GM(rawData, 'ridder')
    gm.run()
