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
    params = {'a': 0, 'b': 0, 'c': 0}
    rootAlgoName = ''
    converged = False

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
        self.rootAlgoName = kwargs['rootAlgoName']
        self.rootFindFunc = RootFind(rootAlgoName=self.rootAlgoName,
                                     equation=self.MLEeq,
                                     data=self.data)

    def findParams(self, predictPoints):
        """
        Find parameters of the model

        This function gets called for all models regardless of type
        """
        #print(self.data.FT)
        #print(self.n, self.n/sum(self.data.FT), 1.0)
        sol = scipy.optimize.root(self.MLEeq, [self.n, self.n/sum(self.data.FT), 1.0], options={'maxfev':10000})
        #print(sol)
        if sol.success:
            self.converged = True
        self.aMLE, self.bMLE, self.cMLE = sol.x
        self.params['a'] = self.aMLE
        self.params['b'] = self.bMLE
        self.params['c'] = self.cMLE
        self.predict(predictPoints)
        

    def MVF(self, t, params=None):
        """
        Calculates the Mean Value Function (MVF) based on a, b, and c

        Args:
            a: a value, usually aMLE of type float
            b: b value, usually bMLE of type float
            c: c value, usually cMLE of type float
        Returns:
            MVF values as numpy array
        """
        if params is None:
            params = self.params
        a = params['a']
        b = params['b']
        c = params['c']
        return (a*(1-np.exp(-b*t)))/(1+c*np.exp(-b*t))

    def MVFPlot(self):
        return (self.predictedFailureTimes, self.MVFVal[:len(self.predictedFailureTimes)])

    def MTTFPlot(self):
        return (self.predictedFailureTimes, self.MTTFVal[:len(self.predictedFailureTimes)])

    def FIPlot(self):
        return (self.predictedFailureTimes, self.FIVal[:len(self.predictedFailureTimes)])

    def relGrowthPlot(self, interval):
        growth = []
        for t in self.predictedFailureTimes:
            growth.append(self.reliability(t, interval))
        return (self.predictedFailureTimes, growth)

    def predict(self, numOfPoints):
        futureFailures = [self.data.FN.iloc[-1]+i+1 for i in range(numOfPoints)]
        self.predictedFailureTimes = []
        for failure in futureFailures:
            result = scipy.optimize.root(lambda t: failure-self.MVF(t), [self.data.FT.iloc[-1]])
            if result.success:
                next_val = result.x[0]
                self.predictedFailureTimes.append(next_val)
        self.predictedFailureTimes = np.array(self.predictedFailureTimes)
        self.futureFailures = np.array(futureFailures)

        self.MVFVal = np.append(self.MVF(self.data.FT), self.futureFailures)
        self.predictedFailureTimes = np.append(self.data.FT, self.predictedFailureTimes)
        self.FIVal = self.FI(self.predictedFailureTimes)
        self.MTTFVal = self.MTTF(self.predictedFailureTimes)

    def FI(self, t, params=None):
        """
        Calculates Failure Intensity

        Args:
            a: a value, usually aMLE of type float
            b: b value, usually bMLE of type float
            c: c value, usually cMLE of type float
        Returns:
            Failure Intensity as numpy array
        """
        if params is None:
            params = self.params
        a = params['a']
        b = params['b']
        c = params['c']
        return (a*b*(c+1)*np.exp(b*t))/((c+np.exp(b*t))**2)

    def lnL(self, params=None):
        if params is None:
            params = self.params
        a = params['a']
        b = params['b']
        c = params['c']
        aMLE = self.n/((1-np.exp(-b*self.tn))/(1+c*np.exp(-b*self.tn)))
        firstTerm = (aMLE*(1-np.exp(-b*self.tn)))/(1+c*np.exp(-b*self.tn))
        secondTerm = self.n*np.log(a)+self.n*np.log(b)+self.n*np.log(1+c)
        thirdTerm = np.sum(np.log(c+np.exp(b*self.data.FT)))                        
        return -firstTerm + secondTerm + b*self.sumT - 2*thirdTerm

    def reliability(self, t, interval):  #Check with Shekar
        """
        Represents the reliability growth equation

        Args:
            oper_time: Mission time denoted as Delta -  This is a user specified input
            timeVec: Failure time vector

        Returns:
            Reliability growth for the specified Operation/Mission time
        """
        firstTerm = (self.aMLE*(1-np.exp(-self.bMLE*(interval+t))))/(1+self.cMLE*np.exp(-self.bMLE*(interval+t)))
        secondTerm = (self.aMLE*(1-np.exp(-self.bMLE*t)))/(1+self.cMLE*np.exp(-self.bMLE*t))
        return np.exp(-((firstTerm)-(secondTerm)))

    def MTTF(self, t, params=None):
        if params is None:
            params = self.params
        a = params['a']
        b = params['b']
        c = params['c'] 
        FailInt = (a*b*(c+1)*np.exp(b*t))/((c+np.exp(b*t))**2)
        return 1/FailInt

    def finite_model(self):
        return True

    def MLEeq(self, x):
        """
        Represents MLE eqation, used in root finding

        Args:
            N0: First parameter N0 of type float

        Returns:
            Value of MLE equation
        """
        a, b, c = x
        aNr = 1-np.exp(b*self.tn)
        aDr = c+np.exp(b*self.tn)
        aEq = (self.n/a) + (aNr/aDr)

        if (c+np.exp(b*self.tn))**2 == 0:
            print("denom 0 for {} {} {}".format(a, b, c))
        bFirstPart = (-a*(1+c)*self.tn*np.exp(b*self.tn))/((c+np.exp(b*self.tn))**2)
        bSecondPart = np.sum((1/b)-((2*self.data.FT*np.exp(b*self.data.FT))/(c+np.exp(b*self.data.FT))) + self.data.FT)
        bEq = bFirstPart + bSecondPart

        cFirstPart = a*(-1+np.exp(b*self.tn))/((c+np.exp(b*self.tn))**2)
        cSecondPart = np.sum((-2/(c+np.exp(b*self.data.FT))) + (1/(1+c)))        
        cEq = cFirstPart + cSecondPart
        return [aEq, bEq, cEq]

if __name__ == "__main__":
    #fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheet_name='NASA1')
    iss = ISS(data=rawData, rootAlgoName='newton')
    iss.findParams(1)
    print(iss.MTTFPlot())
    print(iss.MTTFVal)
    #print(iss.MLEeq([61.7598, 0.0462066, 67.507]))
