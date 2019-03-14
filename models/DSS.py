# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 12:48:36 2019

"""
import pandas as pd
import numpy as np
import scipy.optimize

from core.model import Model
from core.rootFind import RootFind


class DSS(Model):
    """
    DSS Model

    """
    name = "Delayed S-shaped"

    def __init__(self, *args, **kwargs):
        """
        Initialize Model
        Keyword Args
        data: Pandas dataframe with all required columns

        n = length of data vector
        tn = nth value of FT vector 
        sumT = summation of FT vector
        """
        super().__init__(*args, **kwargs)
        self.n = len(self.data)
        self.tn = self.data.FT.iloc[-1]
        self.sumT = self.data.FT.sum()
        self.rootFindFunc = RootFind(rootAlgoName=kwargs['rootAlgoName'],
                                     equation=self.MLEeq,
                                     data=self.data)

    def findParams(self, predictPoints):
        """
        Find parameters of the model
        This function gets called for all models regardless of type

        bMLE = value from rootFind with repect to b
        aMLE = value from bMLE with repect to a
        DSSmt = mean value from MVF function
        lambdat = failure intensity value for FI function
        DSSLL = log likelihood value from lnL function
        """
        self.bMLE = self.calcbMLE()
        self.aMLE = self.calcaMLE(self.bMLE)
        self.predict(predictPoints)
        # self.DSSmt = self.MVF(self.bMLE, self.aMLE, self.tn)
        # self.lambdat = self.FI(self.bMLE, self.aMLE, self.tn)
        # self.DSSLL = self.lnL(self.bMLE, self.aMLE, self.DSSmt)
        self.predictedFailureTimes = np.append(self.data.FT, self.predictedFailureTimes)
        self.MVFVal = np.append(self.MVF(self.aMLE,self.bMLE, self.data.FT),self.futureFailures)
        self.FIVal = self.FI(self.aMLE,self.bMLE, np.append(self.data.FT,self.predictedFailureTimes))
        self.MTTFVal = self.MTTF(self.aMLE,self.bMLE, np.append(self.data.FT,self.predictedFailureTimes))

    def predict(self, numOfPoints):
        futureFailures = [self.data.FN.iloc[-1]+i+1 for i in range(numOfPoints)]
        self.predictedFailureTimes = []
        for failure in futureFailures:
            result = scipy.optimize.root(lambda t: failure-self.MVF(self.aMLE, self.bMLE, t), [self.data.FT.iloc[-1]])
            if result.success:
                next_val = result.x[0]
                self.predictedFailureTimes.append(next_val)
        self.predictedFailureTimes = np.array(self.predictedFailureTimes)
        self.futureFailures = np.array(futureFailures)

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

    def lnL(self, a, b):
        """
        Log likelihood equation

        Returns:
            LL value of type float
        """
        firstTerm = self.MVF(a,b,self.tn)
        secondTerm = np.sum(np.log(self.FI(a,b,self.data.FT)))
        return -firstTerm + secondTerm

    def MVF(self, a, b, t):
        """
        Mean Value Function. Used in Cumulative failures
        and estimate remaining faults

        Returns:
            mt value for DSS model of type float
        """
        return a * (1 - np.exp(-b*t) * (1 + b * t))

    def FI(self, a, b, t):
        """
        Failure Intensity

        Returns: 

        """
        return a * np.power(b, 2) * np.exp(-b * t) * t

    def reliability(self, t, interval):
        """
        Reliability function
        """
        firstTerm = self.MVF(self.aMLE,self.bMLE,t+interval)
        secondTerm = self.MVF(self.aMLE,self.bMLE,t)
        return np.exp(-((firstTerm)-(secondTerm)))

    def MTTF(self, a, b, t):
        """
        Mean Time To Failure function
        """
        FailInt = self.FI(a,b,t)
        return 1/FailInt

    def finite_model(self):
        return True

    def MLEeq(self, b):
        """
        Represents MLE equation, used in root finding to find b

        Args:
            b: Type float used to find bhat

        Returns: 
            bhat of type float
        """
        secondTerm = (b * np.power(self.tn, 2)) /(np.exp(b * self.tn) - 1 - b * self.tn)
        return (2/b) - secondTerm - (self.sumT / self.n)                         

    def calcbMLE(self):
        """
        Uses findRoot to find bMLE of type float

        Returns:
            bMLE
        """
        bMLE = self.rootFindFunc.findRoot()
        self.converged = self.rootFindFunc.converged
        return bMLE

    def calcaMLE(self, b):
        """
        Uses bMLE to find aMLE of type float

        Returns:
            aMLE
        """
        aMLE = self.n / (1-(1 + b * self.tn) * np.exp(-b * self.tn))
        return aMLE


if __name__ == "__main__":
    #fname = "model_data.xlsx"
    fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheet_name='SYS1')
    dss = DSS(data=rawData, rootAlgoName='bisect')
    dss.findParams(1)
    print(dss.MVFVal)
    print(dss.MTTFVal)
    print(dss.FIVal)
    # print(dss.aMLE)
    # print(dss.bMLE)