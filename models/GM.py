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

    def findParams(self, predictPoints):
        """
        Find parameters of the model

        This function gets called for all models regardless of type
        """
        self.phiMLE = self.calcphiMLE()
        self.DHat = self.calcDMLE(self.phiMLE)
        self.lnLVal = self.lnL(self.DHat, self.phiMLE)
        self.predict(predictPoints)
        self.MVFVal = np.append(self.MVF(self.DHat, self.phiMLE, self.data.FT), self.futureFailures)
        self.predictedFailureTimes = np.append(self.data.FT, self.predictedFailureTimes)

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
        secondTerm = np.sum(np.multiply(iVector, np.log(phi)))
        thirdTerm = (np.power(phi, iVector) * self.data.IF).sum()
        return self.n * np.log(DHat) + secondTerm - (DHat * thirdTerm)

    def MVF(self, DHat, phi, t):
        """
        Calculates the Mean Value Function (MVF) based on DHat and phi

        Args:
            DHat: DHat value, 
            phi: phi value, usually phiMLE of type float
        Returns:
            MVF values as numpy array
        """
        return -(np.log(1 - (DHat * t * np.log(phi))/phi)/np.log(phi))

    def MVFPlot(self):
        return (self.predictedFailureTimes,
                self.MVFVal[:len(self.predictedFailureTimes)])

    def relGrowthPlot(self, interval):
        growth = []
        for t in self.predictedFailureTimes:
            growth.append(self.reliability(t, interval))
        return (self.predictedFailureTimes, growth)

    def predict(self, numOfPoints):
        futureFailures = [self.data.FN.iloc[-1]+i+1 for i in range(numOfPoints)]
        self.predictedFailureTimes = []
        for failure in futureFailures:
            result = scipy.optimize.root(lambda t: failure-self.MVF(self.DHat, self.phiMLE, t), [self.data.FT.iloc[-1]])
            if result.success:
                next_val = result.x[0]
                self.predictedFailureTimes.append(next_val)
        self.predictedFailureTimes = np.array(self.predictedFailureTimes)
        self.futureFailures = np.array(futureFailures)

    def FI(self, N0, phi):
        pass

    def MLEeq(self, phi):
        """
        Represents MLE equation, used in root finding

        Args:
            N0: First parameter N0 of type float

        Returns:
            Value of MLE equation
        """
        iVector = [i for i in range(self.n)]
        rightTerm = (self.calcDMLE(phi) *
                     (iVector * np.power(phi, iVector) * self.data.IF).sum())
        leftTerm = np.sum(np.divide(iVector, phi))
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

    def reliability(self, t, interval):
        return np.exp(-1.0 *
                      (self.MVF(self.DHat, self.phiMLE, t + interval) -
                       self.MVF(self.DHat, self.phiMLE, t))
                      )

    def MTTF(self):
        pass

    def finite_model(self):
        pass


if __name__ == "__main__":
    fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheetname='SYS1')
    gm = GM(rawData, 'ridder')
    gm.run()
