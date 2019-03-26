from abc import ABC, abstractmethod, abstractproperty


class Model(ABC):
    name = "Generic Model"
    converged = False
    params = {}

    def __init__(self, *args, **kwargs):
        """
        Initialize Model

        Keyword Args
        data: Pandas dataframe with all required columns
        """
        self.data = kwargs['data']

    @abstractmethod
    def findParams(self):
        """
        Find parameters of the model

        This function gets called for all models regardless of type
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

    @abstractmethod
    def FI(self):
        """
        Failure Intensity
        """
        pass

    @abstractmethod
    def reliability(self):
        """
        Reliability function
        """
        pass

    @abstractmethod
    def MTTF(self):
        """
        Mean Time To Failure function
        """
        pass

    @abstractproperty
    def finite_model(self):
        pass
