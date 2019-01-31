import matplotlib.pyplot as plt
from PyQt5.QtCore import QSettings
# from core.helpers import LaplaceTest, AverageTest
from core.dataClass import PandasModel


class PlotSettings:
    def __init__(self):
        self._style = '-o'
        self._plotType = 'step'
        self.markerSize = 3

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        self._style = style

    @property
    def plotType(self):
        return self._plotType

    @plotType.setter
    def plotType(self, plotType):
        self._plotType = plotType

    def generatePlot(self, ax, x, y, title="None", xLabel="X", yLabel="Y"):
        ax.clear()
        ax.grid(True)
        plotMethod = getattr(ax, self.plotType)
        plotMethod(x, y, self.style, markerSize=self.markerSize)
        ax.set_title(title)
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        return ax

    def addLine(self, ax, x, y):
        plotMethod = getattr(ax, self.plotType)
        plotMethod(x, y, self.style, markerSize=self.markerSize)
        return ax
