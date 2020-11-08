import pandas as pd
import numpy as np
import scipy.optimize

from core.model import Model
from core.rootFind import RootFind


class WEI(Model):
    name = "Weibull"
    params = {'a': 0, 'b': 0, 'c': 0}
    rootAlgoName = ''
    converged = False

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
        
        self.MLE = aMLE, bMLE, cMLE in list form
        self.MVFvalue = Mean Value Function value
        self.lambdat = Failure Intensity value
        self.lnLvalue = Log likelihood value.
        """
        sol = scipy.optimize.root(self.MLEeq, [self.n, self.n/sum(self.data.FT), 1.0], options={'maxfev':10000})
        #print(sol)
        self.aMLE, self.bMLE, self.cMLE = sol.x
        self.params['a'] = self.aMLE
        self.params['b'] = self.bMLE
        self.params['c'] = self.cMLE
        if sol.success:
            self.converged = True
        self.predict(predictPoints)
        

    def MVF(self, t, params=None):
        """
        Mean Value Function. Used in Cumulative failures
        and estimate remaining faults
        """
        if params is None:
            params = self.params
        a = params['a']
        b = params['b']
        c = params['c']
        return a * (1 - np.exp(-b * np.power(t, c)))

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
        Failure Intensity
        
        """
        if params is None:
            params = self.params
        a = params['a']
        b = params['b']
        c = params['c']
        return a * b * c * np.exp(-b * np.power(t, c)) * np.power(t, -1 +c)

    def lnL(self, params=None):
        """
        Log likelihood equation. Used to calculate AIC
        
        """
        if params is None:
            params = self.params
        a = params['a']
        b = params['b']
        c = params['c']
        term1 = self.MVF(self.tn, params=params)
        term2 = sum(np.log(self.FI(self.data.FT, params=params)))
        return -term1 + term2

    def reliability(self,t, interval):
        """
        Reliability function
        """
        firstTerm = self.MVF(t+interval)
        secondTerm = self.MVF(t)
        return np.exp(-((firstTerm)-(secondTerm)))

    def MTTF(self, t, params=None):
        """
        Mean Time To Failure function
        """
        if params is None:
            params = self.params
        a = params['a']
        b = params['b']
        c = params['c']
        FailInt = self.FI(t, params=params)
        return 1/FailInt

    def finite_model(self):
        return True

    def MLEeq(self,x):
        """
        Uses findRoot to find bMLE of type float
        
        Returns:
            All MLE equations of type float in a list
        """
        a, b, c = x 
        aMLE = (self.n/a) - (1 - np.exp(-b * np.power(self.tn,c)))
        bMLE = -a*np.power(self.tn,c)*np.exp(-b *np.power(self.tn,c))+ sum((1-b*np.power(self.data.FT,c))/(b))
        cMLE = -a*b*np.power(self.tn,c)*np.log(self.tn)*np.exp(-b*np.power(self.tn,c)) + (self.n/c) + sum(np.log(self.data.FT)-b*np.log(self.data.FT)*np.power(self.data.FT,c))
        return [aMLE, bMLE, cMLE]

if __name__ == "__main__":
    #fname = "model_data.xlsx"
    fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheet_name='SYS1')
    Wei = WEI(data=rawData, rootAlgoName='newton')
    Wei.findParams(1)
    #print(Wei.MVFVal)
    print(Wei.MTTFVal)
    print(Wei.predictedFailureTimes)
    print(Wei.MVFVal)
    #print(iss.MLEeq([61.7598, 0.0462066, 67.507]))

