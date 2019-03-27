from abc import ABC, abstractmethod, abstractproperty
from ui.commonWidgets import ComputeWidget
import numpy as np
import models as md


class ModelEval(ABC):
    name = 'Base Model Eval'
    def __init__(self):
        pass

    @abstractmethod
    def eval(self, *args, **kwargs):
        """Function called to evaluate models"""
        pass


class AIC(ModelEval):
    name = "Akaike Information Criterion"
    def __init__(self):
        pass        

    def eval(self, *args, **kwargs):
        modelList = args[0]
        evalResults = {}
        for model in modelList:
            evalResults[model.name] = 2*len(model.params) - 2*model.lnL()
        return evalResults


class PSSE(ModelEval):
    name = "Predictive sum of squares error"

    def __init__(self):
        pass

    def eval(self, *args, **kwargs):
        modelList = args[0]
        percent = kwargs['psse']
        evalResults = {}
        
        for model in modelList:
            reducedDataLength = int(percent * len(model.data))
            reducedData = model.data.iloc[:reducedDataLength]
            remainingData = model.data.iloc[reducedDataLength:]
            algoName = model.rootAlgoName
            reducedModel = md.modelList[type(model).__name__](data=reducedData, rootAlgoName=algoName)
            reducedModel.findParams(0)
            if reducedModel.converged:
                mvf = reducedModel.MVF(remainingData.FT)
                i = np.array([i+1 for i in range(reducedDataLength, len(model.data))])
                evalResults[model.name] = np.sum(np.square(mvf - i))
            else:
                evalResults[model.name] = None
        return evalResults
