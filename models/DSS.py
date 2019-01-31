# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 12:48:36 2019

"""
import pandas as pd
import numpy as np
import scipy.optimize
from scipy.misc import derivative
from core.model import Model
from core.rootFind import RootFind


class DSS(Model):
    """
    DSS Model

    """
    name = "Delayed S-Shaped"

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

    def findParams(self):
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
        self.DSSmt = self.MVF(self.bMLE, self.aMLE)
        self.lambdat = self.FI(self.bMLE, self.aMLE, self.tn)
        self.DSSLL = self.lnL(self.bMLE, self.aMLE, self.DSSmt)

    def lnL(self, b, a, mt):
        """
        Log likelihood equation

        Returns:
            LL value of type float
        """
        Vector = [i for i in range(self.n)]
        term = np.log(self.FI(b, a, self.data.FT[Vector])).sum()
        return -mt + term

    def MVF(self, b, a):
        """
        Mean Value Function. Used in Cumulative failures
        and estimate remaining faults

        Returns:
            mt value for DSS model of type float
        """
        return a * (1 - np.exp(-b * self.tn) * (1 + b * self.tn))

    def FI(self, b, a, t):
        """
        Failure Intensity

        Returns: 

        """
        return a * np.power(b, 2) * np.exp(-b * t) * t

    def reliability(self):
        """
        Reliability function
        """
        pass

    def MTTF(self):
        """
        Mean Time To Failure function
        """
        pass

    def finite_model(self):
        pass

    def MLEeq(self, b):
        """
        Represents MLE equation, used in root finding to find b

        Args:
            b: Type float used to find bhat

        Returns: 
            bhat of type float
        """
        return ((2/b) - ((b * np.power(self.tn, 2)) /
                         (np.exp(b * self.tn) - 1 - b * self.tn)) -
                         (self.sumT / self.n))

    def calcbMLE(self):
        """
        Uses findRoot to find bMLE of type float

        Returns:
            bMLE
        """
        bMLE = self.rootFindFunc.findRoot()
        return bMLE

    def calcaMLE(self, b):
        """
        Uses bMLE to find aMLE of type float

        Returns:
            aMLE
        """
        aMLE = self.n / (1-(1 + b * self.tn) * np.exp(-b * self.tn))
        return aMLE
