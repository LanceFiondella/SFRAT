import pandas as pd
import numpy as np
import scipy.optimize

from core.model import Model
from core.rootFind import RootFind


class ISS(Model):
    """
    Inflexion S-shaped Model


    """
    name = 'Inflexion S-shaped'

    def __init__(self, *args, **kwargs):
        """
        Initialize model

        Keyword Args:
        rootAlgoName: string that identifies root finding function
        """
        super().__init__(*args, **kwargs)
        self.n = len(self.data)
        self.tn = self.data.FT.iloc[-1] 
        self.sumT = self.data.FT.sum()
        self.rootFindFunc = RootFind(rootAlgoName=kwargs['rootAlgoName'],
                                     equation=self.MLEeq,
                                     data=self.data)

    def findParams(self): #Check with Shekar
        """
        Find parameters of the model

        This function gets called for all models regardless of type
        """
        self.aMLE = self.calcaMLE()
        self.bMLE = self.calcbMLE()
        self.cMLE = self.calccMLE()
        self.MVFVal = self.MVF(self.aMLE, self.bMLE, self.cMLE)
        self.FIVal = self.FI(self.aMLE, self.bMLE, self.cMLE)
        self.MTTFVal = self.MTTF(self.aMLE, self.bMLE, self.cMLE)
        self.RelVal = self.reliability(self.aMLE, self.bMLE, self.cMLE, fail_num, timeVec) 

    def MVF(self, a, b, c):
        """
        Calculates the Mean Value Function (MVF) based on a, b, and c

        Args:
            a: a value, usually aMLE of type float
            b: b value, usually bMLE of type float
            c: c value, usually cMLE of type float
        Returns:
            MVF values as numpy array
        """
        return (a*(1-np.exp(-b*self.data.FT)))/(1+c*np.exp(-b*self.data.FT))

    def FI(self, a, b, c):
        """
        Calculates Failure Intensity

        Args:
            a: a value, usually aMLE of type float
            b: b value, usually bMLE of type float
            c: c value, usually cMLE of type float
        Returns:
            Failure Intensity as numpy array
        """
        return (a*b*(c+1)*np.exp(b*self.data.FT))/((c+np.exp(b*self.data.FT))**2)

    def lnL(self, a, b, c):
        """
        Calculates Log Likelihood

        Args:
            a: a value, usually aMLE of type float
            b: b value, usually bMLE of type float
            c: c value, usually cMLE of type float
        Returns:
            Log likelihood as float
        """
        firstTerm = (a*(1-np.exp(-b*self.tn)))/(1+c*np.exp(-b*self.tn))
        secondTerm = self.n*np.log(a)+self.n*np.log(b)+self.n*np.log(1+c)
        thirdTerm = np.sum(np.log(1+np.exp(b*self.data.FT)))                        
        return -firstTerm + secondTerm + b*self.sumT - 2*thirdTerm

    def reliability(self, opertime, timeVec):  #Check with Shekar
        """
        Represents the reliability growth equation

        Args:
            oper_time: Mission time denoted as Delta -  This is a user specified input
            timeVec: Failure time vector

        Returns:
            Reliability growth for the specified Operation/Mission time
        """

        firstTerm = (self.aMLE*(1-np.exp(-self.bMLE*(opertime+timeVec))))/(1+self.cMLE*np.exp(-self.bMLE*(opertime+timeVec)))
        secondTerm = (self.aMLE*(1-np.exp(-self.bMLE*timeVec)))/(1+self.cMLE*np.exp(-self.bMLE*timeVec))
        np.exp(-((firstTerm)-(secondTerm)))
        return 

    def MTTF(self):  #Check with Shekar #This is for TBF plot on Tab 2
        return pd.reciprocal(self.FIVal)

    def finite_model(self): 
        return True

    def MLEeq(self, N0):    #Check with Shekar
        """
        Represents MLE eqation, used in root finding

        Args:
            N0: First parameter N0 of type float

        Returns:
            Value of MLE equation
        """
        

        return 

    def calcaMLE(self): 
        """
        Defines the MLE of a based on b and c values (to be called in the MLE_eq function)

        Returns:
            Value of a of type float
        """
        secondTerm = (self.n/(((1-np.exp(-b*self.tn)))/(1+c*np.exp(-b*self.tn))))  
        return a - secondTerm   

    def calcbMLE(self):
        """
        Defines the MLE of b to be called in the MLE_eq function

        Returns:
            bMLE of type float
        """
        firstTerm = (-a*(1+c)*self.tn*np.exp(b*self.tn))/((c+np.exp(b*self.tn))**2)
        secondTerm = np.sum((1/b)-((2*self.data.FT*np.exp(b*self.data.FT))/(c+np.exp(b*self.data.FT))) + self.data.FT)
        return b - (firstTerm + secondTerm)

    def calccMLE(self):
        """
        Defines the MLE of 'c' to be called in the MLE_eq function

        Returns:
            cMLE of type float
        """
        firstTerm = (a*(-1+np.exp(b*self.tn))/((c+np.exp(b*self.tn))**2))
        secondTerm = np.sum((-2/(c+np.exp(b*self.data.FT))) + (1/(1+c)))
        return c - (firstTerm+secondTerm)

    def MVF_cont(self, t, a, b, c):
        """
        Point value of Mean value function

        Args:
            t: time at which to calculate MVF
            a: a value, usually aMLE of type float
            b: b value, usually bMLE of type float
            c: c value, usually cMLE of type float

        Returns:
            MVF for time t as float
        """
        return (a*(1-np.exp(-b*t)))/(1+c*np.exp(-b*t))


if __name__ == "__main__":
    fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheetname='SS4')
    iss = ISS(rawData, 'newton')
    iss.findParams()
