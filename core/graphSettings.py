import matplotlib.pyplot as plt
from PyQt5.QtCore import QSettings
from core.helpers import LaplaceTest, AverageTest

class GraphSettings:
    POINTS = 0
    LINES = 1
    BOTH = 2

    CUMULATIVE = 0
    TBF = 1         #Time between failures
    FINTENSITY = 2

    DATA = 0
    TREND = 1

    LAPLACE = 0
    RAA = 1

    def __init__(self):
        self.settings = QSettings('NSF Career', 'SFRAT')
        self.graphSettings = {}
        self.graphSettings['viewStyle'] = GraphSettings.BOTH
        self.graphSettings['dataMode'] = GraphSettings.CUMULATIVE
        self.graphSettings['showTrend'] = GraphSettings.DATA
        self.graphSettings['test'] = GraphSettings.LAPLACE
        self.settings.setValue('graphSettings', self.graphSettings)
        
        del self.settings

        self.viewStyle = GraphSettings.BOTH
        self.dataMode = GraphSettings.CUMULATIVE
        self.showTrend = GraphSettings.DATA
        self.test = GraphSettings.LAPLACE
        self.markerSize = 3

    # convert view style to matlplot lib graph syntax
    def viewStyleToPointStyle(self):
        if self.viewStyle == GraphSettings.LINES:
            return "-"
        elif self.viewStyle == GraphSettings.POINTS:
            return "o"
        elif self.viewStyle == GraphSettings.BOTH:
            return "-o"

    def generatePlot(self, plot, data):
        """
            Generate plot 

            This function returns a matplotlib Axes object based on current 
            view and settings. The function should be called in Tab.updateGraph()

            Args:
                plot: Axes object to be modified
                data: Pandas dataframe with the required columns
            Returns:
                plot: Modifed Axes object with current settings
        """
        data = data.getData()
        if self.showTrend == GraphSettings.DATA:
            if self.dataMode == GraphSettings.CUMULATIVE:
                plot = self.drawPlot(plot, data["FT"], data["FN"], 
                                     title="Cumulative Failures",
                                     xLabel="Cumulative Time (s)",
                                     yLabel="Number of Failures")
            elif self.dataMode == GraphSettings.TBF:
                plot = self.drawPlot(plot, data["FT"], data["IF"], 
                                     title="Interfailure Time",
                                     xLabel="Cumulative Time (s)",
                                     yLabel="Time Between Successive Failures (s)")
            elif self.dataMode == GraphSettings.FINTENSITY:
                plot = self.drawPlot(plot, data["FT"], 1/data["IF"], 
                                     title="Failure Intensity",
                                     xLabel="Cumulative Time (s)",
                                     yLabel="Number of Failures per Unit Time")
        elif self.showTrend == GraphSettings.TREND:
            if self.test == GraphSettings.LAPLACE:
                t = LaplaceTest(data)
                plot = self.drawPlot(plot, t["FN"], t["LT"], 
                                     title="Laplace Trend Test",
                                     xLabel="Failure Number",
                                     yLabel="Laplace Statistic")
            elif self.test == GraphSettings.RAA:
                t = AverageTest(data)
                plot = self.drawPlot(plot, t["FN"], t["RA"], 
                                     title="Running Average Trend Test",
                                     xLabel="Failure Number",
                                     yLabel="Running Average of Interfailure Time")
        plot.grid(True)
        return plot


    def drawPlot(self, plot, x, y, title="Dummy", xLabel="X-Axis", yLabel="Y-Axis"):
        """
        Draw the plot

        This function modifies the Axes object to draw the appropriate plot.
        Called in GraphSettings.generatePlot()

        Args:
            plot: Axes object to be modified
            x : Vector for the x-axis
            y : Vector for the y-axis
        Keyword Args:
            title : Title for the plot
            xLabel : Label for the x-axis
            yLabel : Label for the y-axis

        """
        if self.viewStyle == GraphSettings.POINTS:
            plottingFunction = plot.plot
        else:
            plottingFunction = plot.step
        
        plottingFunction(x, y, self.viewStyleToPointStyle(), markerSize=self.markerSize)
        plot.set_title(title)
        plot.set_xlabel(xLabel)
        plot.set_ylabel(yLabel)
        return plot
