# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 10:48:32 2019

"""

import pandas as pd
import numpy as np
from scipy.misc import derivative
from core.model import Model
from core.rootFind import RootFind
from scipy import optimize

class WEI(Model):
    name = "Weibull"

    def __init__(self, *args, **kwargs):
        """
        Initialize Model
        Keyword Args
        data: Pandas dataframe with all required columns
        
        n = length of data vector
        tn = nth value of FT vector 
        sumT = summation of FT vector
        a0 = initial estimate for a variable
        b0 = initial estimate for b variable
        c0 = initial estimate for c variable
        """
        super().__init__(*args, **kwargs)
        self.n = len(self.data)
        self.tn = self.data.FT[self.n]
        self.sumT = self.data.FT.sum()
        self.rootFindFunc = RootFind(rootAlgoName=kwargs['bisect'],
                                     equation=self.MLEeqB,
                                     data=self.data)
        self.a0 = self.n
        self.b0 = self.n / self.sumT
        self.c0 = 1
        
    def findParams(self):
        """
        Find parameters of the model
        This function gets called for all models regardless of type
        
        self.MLE = aMLE, bMLE, cMLE in list form
        self.MVFvalue = Mean Value Function value
        self.lambdat = Failure Intensity value
        self.lnLvalue = Log likelihood value.
        """
        self.MLE = optimize.fsolve(self.calcMLEs, (self.a0, self.b0, self.c0), maxfev = 10000)
        self.MVFvalue = self.MVF(self.MLE[0], self.MLE[1], self.MLE[2], self.tn)
        self.lambdat = self.FI(self.MLE[0], self.zMLE[1], self.MLE[2], self.tn)
        self.lnLvalue = self.lnL(self.MLE[0], self.MLE[1], self.MLE[2], self.tn)

    def lnL(self, a , b, c, t):
        """
        Log likelihood equation. Used to calculate AIC
        
        """
        Vector = [i for i in range(self.n)]
        term1 = self.MVF(a, b, c, t)
        term2 = np.log(self.FI(a, b, c, self.data.FT[Vector])).sum()
        return -term1 + term2

    def MVF(self, a, b, c, t):
        """
        Mean Value Function. Used in Cumulative failures
        and estimate remaining faults
        """
        return a * (1 - np.exp(-b * np.power(t, c)))

    def FI(self, a, b, c, t):
        """
        Failure Intensity
        
        """
        return a * b * c * np.exp(-b * np.power(t, c)) * np.power(t, -1 +c)

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
        
        """
        pass
    
    def calcMLEs(self, x):
        """
        Uses findRoot to find bMLE of type float
        
        Returns:
            All MLE equations of type float in a list
        """
        (a, b, c) = x 
        Vector = [i for i in range(self.n)]
        sumi1 = ((1 / b) - ((self.data.FT[Vector]) ** c)).sum()
        sumi2 = ((1 / c) - (((self.data.FT[Vector]) ** c) * np.log(self.data.FT[Vector]) * b) + np.log(self.data.FT[Vector])).sum()
        aMLE = -1 + np.exp(-b * (self.tn ** c)) + (self.n / a)
        bMLE = (-a * (self.tn ** c) * np.exp(-b * (self.tn ** c))) + sumi1
        cMLE = (-b * a * (self.tn ** c) * np.exp(-b * (self.tn ** c)) * np.log(self.tn)) + sumi2
        return [aMLE, bMLE, cMLE]
    


    