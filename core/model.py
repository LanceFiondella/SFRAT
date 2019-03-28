from abc import ABC, abstractmethod, abstractproperty


class Model(ABC):

    def __init__(self, *args, **kwargs):
        """
        Initialize Model

        Keyword Args
        data: Pandas dataframe with all required columns
        """
        self.data = kwargs['data']
    ###############################################
    #Properties/Members all models must implement#
    ##############################################
    @abstractproperty
    def name(self):
        """
        Name of a model as a string
        """
        return 'Generic Model'

    @abstractproperty
    def converged(self):
        """
        Boolean value that indicates whether the model has converged
        Must be set after parameters are calculated
        """
        return True

    @abstractproperty
    def rootAlgoName(self):
        """
        Algorithm name to calculate the roots of the MLE equations
        """
        return 'newton'

    @abstractproperty
    def finite_model(self):
        """
        Boolean to indicate if a model is finite
        """
        return True

    @abstractproperty
    def params(self):
        """
        Dictionary to indicate the parameters of a model
        Key: Parameter name
        Value: Float value 
        """
        return {'dummy': 0}

    #################################################
    #Methods that must be implemented by all models#
    ################################################
    @abstractmethod
    def findParams(self):
        """
        Find parameters of the model

        This function gets called for all models regardless of type
        """
        pass

    @abstractmethod
    def predict(self, numOfPoints):
        """
        Function used to trigger the prediction of future failures
        based on the calculated MLEs of the model parameters
        """
        pass

    @abstractmethod
    def reliability(self, t, interval):
        """
        Reliability equation. Generally of the form e^-(MVF(t+interval) - MVF(t))
        """
        pass

    @abstractmethod
    def lnL(self):
        """
        Log likelihood equation. Used to calculate AIC
        """
        pass

    @abstractmethod
    def MVF(self):
        """
        Mean Value Function. Used in Cumulative failures
        and estimate remaining faults
        """
        pass

    ################################################################
    # Functions for plotting and table generation. Must return a   # 
    # tuple of vectors representing the x and y axes generally of  # 
    # the form ([x0, x1,..., xn], [y0, y1,...,yn])                 #
    ################################################################
    @abstractmethod
    def MVFPlot(self):
        """
        Reliability function
        """
        pass

    @abstractmethod
    def MTTFPlot(self):
        """
        Mean Time To Failure function
        """
        pass

    @abstractmethod
    def FIPlot(self):
        pass

    @abstractmethod
    def relGrowthPlot(self):
        pass
