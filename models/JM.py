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

    def findParams(self, predictPoints):
        """
        Find parameters of the model

        This function gets called for all models regardless of type
        """
        self.N0MLE = self.calcN0MLE()
        self.phiMLE = self.calcPhi(self.N0MLE)
        self.predict(predictPoints)
        self.MVFVal = np.append(self.MVF(self.N0MLE, self.phiMLE, self.data.FT), self.futureFailures)
        self.predictedFailureTimes = np.append(self.data.FT, self.predictedFailureTimes)
        self.MTTFVal = self.MTTF(self.N0MLE, self.phiMLE, np.append(self.data.FN, self.futureFailures))
        self.FIVal = self.FI(self.N0MLE, self.phiMLE, self.predictedFailureTimes)

    def MVF(self, N0, phi, t):
        """
        Calculates the Mean Value Function (MVF) based on N0 and phi

        Args:
            N0: N0 value, usually N0MLE of type float
            phi: phi value, usually phiMLE of type float
            t: time, can be vector or point value
        Returns:
            MVF values as point value or array depending on t
        """
        return N0*(1 - np.exp(-phi*t))

    def MVFPlot(self):
        return (self.predictedFailureTimes,
                self.MVFVal[:len(self.predictedFailureTimes)])

    def MTTFPlot(self):
        return (self.predictedFailureTimes,
                self.MTTFVal[:len(self.predictedFailureTimes)])

    def FIPlot(self):
        return (self.predictedFailureTimes,
                self.FIVal[:len(self.predictedFailureTimes)])

    def relGrowthPlot(self, interval):
        growth = []
        for t in self.predictedFailureTimes:
            growth.append(self.reliability(t, interval))
        return (self.predictedFailureTimes, growth)

    def predict(self, numOfPoints):
        futureFailures = [self.data.FN.iloc[-1]+i+1 for i in range(numOfPoints)]
        self.predictedFailureTimes = []
        for failure in futureFailures:
            result = scipy.optimize.root(lambda t: failure-self.MVF(self.N0MLE, self.phiMLE, t), [self.data.FT.iloc[-1]])
            if result.success:
                next_val = result.x[0]
                self.predictedFailureTimes.append(next_val)
        self.predictedFailureTimes = np.array(self.predictedFailureTimes)
        self.futureFailures = np.array(futureFailures)

    #def timeToTargetRel(self, reliability, interval):
    #    result = scipy.optimize.

    def FI(self, N0, phi, failureTimes):
        """
        Calculates Failure Intensity

        Args:
            N0: N0 value, usually N0MLE of type float
            phi: phi value, usually phiMLE of type float
        Returns:
            Failure Intensity as numpy array
        """
        return N0*phi*(np.exp(-phi*failureTimes))

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

    def reliability(self, t, interval):
        return np.exp(-1.0 *
                      (self.MVF(self.N0MLE, self.phiMLE, t + interval) -
                       self.MVF(self.N0MLE, self.phiMLE, t))
                      )

    def MTTF(self, N0, phi, failureNumbers):
        IFTimes = 1 / (phi * (N0 - failureNumbers))
        return IFTimes

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
        self.converged = self.rootFindFunc.converged
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


if __name__ == "__main__":
    fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheet_name='SYS1')
    jm = JM(rawData, 'ridder')
    jm.run()
