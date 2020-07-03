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
    params = {'phi': 0, 'D': 0}
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
        self.interFailSum = self.data.IF.sum()
        self.rootAlgoName = kwargs['rootAlgoName']
        self.rootFindFunc = RootFind(rootAlgoName=self.rootAlgoName,
                                     equation=self.MLEeq,
                                     data=self.data,
                                     initialEstimate=len(self.data)/self.data.FT.sum())

    def findParams(self, predictPoints):
        """
        Find parameters of the model

        This function gets called for all models regardless of type
        """
        self.phiMLE = self.calcphiMLE()
        self.DMLE = self.calcDMLE(self.phiMLE)
        self.params['phi'] = self.phiMLE
        self.params['D'] = self.DMLE
        self.lnLVal = self.lnL()
        self.predict(predictPoints)

    def lnL(self, params=None): #Verified
        """
        Calculates Log Likelihood

        Args:
            DHat: DHat value, 
            phi: phi value, usually phiMLE of type float
        Returns:
            Log likelihood as float
        """
        if params is None:
            params = self.params

        firstTerm = self.n*np.log(params['D'])
        secondTerm = np.sum(np.array([(i-1)*np.log(params['phi']) for i in range(1,1+self.n)],np.float))
        thirdTerm = np.sum(np.array([(np.power(params['phi'],i)/params['phi'])*self.data.IF[i-1] for i in range(1,1+self.n)],np.float))
        return firstTerm + secondTerm - (params['D'] * thirdTerm)

    def MVF(self, t, params=None):
        """
        Calculates the Mean Value Function (MVF) based on DHat and phi

        Args:
            DHat: DHat value, 
            phi: phi value, usually phiMLE of type float
        Returns:
            MVF values as numpy array
        """
        if params is None:
            params = self.params
        return -(np.log(1 - (params['D'] * t * np.log(params['phi']))/params['phi'])/np.log(params['phi']))

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
            result = scipy.optimize.root(lambda t: failure-self.MVF(t), [self.data.FT.iloc[-1]])
            if result.success:
                next_val = result.x[0]
                self.predictedFailureTimes.append(next_val)
        self.predictedFailureTimes = np.array(self.predictedFailureTimes)
        self.futureFailures = np.array(futureFailures)

        self.MVFVal = np.append(self.MVF(self.data.FT), self.futureFailures)
        self.predictedFailureTimes = np.append(self.data.FT, self.predictedFailureTimes)
        self.MTTFVal = self.MTTF(np.append(self.data.FN, self.futureFailures))
        self.FIVal = self.FI(self.predictedFailureTimes)

    def FI(self, failureTimes, params=None):
        if params is None:
            params = self.params
        
        return params['D']/(params['phi']-params['D']*failureTimes*np.log(params['phi']))

    def MLEeq(self, phi): #Verified
        """
        Represents MLE equation, used in root finding

        Args:
            phi: 

        Returns:
            Value of MLE equation
        """
        firstTerm = np.sum(np.array([(i-1)/phi for i in range(1,1+self.n)],np.float))
        secondTerm = np.sum(np.array([(i-1)*(np.power(phi, i)/(np.power(phi, 2)))*self.data.IF[i-1] for i in range(1,1+self.n)], np.float))
        DMLE = (phi*self.n)/(np.sum(np.array([np.power(phi,i)*self.data.IF[i-1] for i in range(1,1+self.n)],np.float)))
        return firstTerm - (DMLE*secondTerm)

    def calcDMLE(self, phi): #Verified
        """
        Calculates the Dparam value using phi

        Returns:
            Dparam of type float
        """
        denom = np.sum(np.array([np.power(phi,i)*self.data.IF[i-1] for i in range(1,1+self.n)],np.float))
        return (phi*self.n)/denom

    def calcphiMLE(self):
        """
        Calculates the N0MLE using findEndpoints and MLEeq

        Returns:
            N0MLE of type float
        """
        phiMLE = self.rootFindFunc.findRoot()
        self.converged = self.rootFindFunc.converged
        return phiMLE

    def reliability(self, t, interval):
        return np.exp(-1.0 *
                      (self.MVF(t + interval) -
                       self.MVF(t))
                      )

    def MTTF(self, failureNumbers, params=None):
        if params is None:
            params = self.params
        
        FailInt = self.FI(failureNumbers, params=params)
        return 1/FailInt

    def finite_model(self):
        return False


if __name__ == "__main__":
    fname = "model_data.xlsx"
    rawData = pd.read_excel(fname, sheet_name='SYS1')
    gm = GM(data = rawData, rootAlgoName= 'ridder')
    #gm.run()
    gm.findParams(1)
    print(gm.MVFVal)
    
