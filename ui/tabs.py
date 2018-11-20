from ui.tab import Tab
from core.graphSettings import GraphSettings

import logging as log
from core.helpers import *

import numpy as np

class DataTab(Tab):
    CUMULATIVE = 0
    TBF = 1
    FINTENSITY = 2
    def __init__(self, container):
        super().__init__(container, Tab.DATA_TAB)
        self.graphMode = DataTab.CUMULATIVE

    def updateGraph(self):
        self.plot.clear()
        self.data = self.container.data.getData()
        if self.graphSettings.showTrend == GraphSettings.DATA:
            if self.graphSettings.dataMode == GraphSettings.CUMULATIVE:
                # plot data
                # if only plotting points use plot
                if self.graphSettings.viewStyle == GraphSettings.POINTS:
                    self.plot.plot(self.data["FT"], self.data["FN"],\
                    self.graphSettings.viewStyleToPointStyle(), markersize=3)
                else:
                    # if plotting lines use step
                    self.plot.step(self.data["FT"], self.data["FN"],\
                    self.graphSettings.viewStyleToPointStyle(), markersize=3)

                # labels
                self.plot.set_title("Cumulative Failures")
                self.plot.set_xlabel("Cumulative Time (s)")
                self.plot.set_ylabel("Number of Failures")
                self.plot.grid(True)

            elif self.graphSettings.dataMode == DataTab.TBF:
                if self.graphSettings.viewStyle == GraphSettings.POINTS:
                    self.plot.plot(self.data["CT"], self.data["IF"] ,\
                    self.graphSettings.viewStyleToPointStyle(), markersize=3)

                else:
                    # if plotting lines use step
                    self.plot.step(self.data["CT"], self.data["IF"] ,\
                    self.graphSettings.viewStyleToPointStyle(), markersize=3)

                # labels
                self.plot.set_title("Interfailure Time")
                self.plot.set_xlabel("Cumulative Time (s)")
                self.plot.set_ylabel("Time Between Sucessive Failures (s)")
                self.plot.grid(True)

            elif self.graphSettings.dataMode == DataTab.FINTENSITY:
                if self.graphSettings.viewStyle == GraphSettings.POINTS:
                    self.plot.plot(self.data["CT"], 1 / self.data["IF"] ,\
                    self.graphSettings.viewStyleToPointStyle(), markersize=3)

                else:
                    # if plotting lines use step
                    self.plot.step(self.data["CT"], 1 / self.data["IF"] ,\
                    self.graphSettings.viewStyleToPointStyle(), markersize=3)

                # labels
                self.plot.set_title("Failure Intensity")
                self.plot.set_xlabel("Cumulative Time (s)")
                self.plot.set_ylabel("Number of Failures per Unit Time")
                self.plot.grid(True)

        elif self.graphSettings.showTrend == GraphSettings.TREND:
            if self.graphSettings.test == GraphSettings.LAPLACE:
                t = LaplaceTest(self.container.data.getData())
                self.plot.step(t['FN'], t['LT'])
                # labels
                self.plot.set_title("Laplace Trend Test")
                self.plot.set_xlabel("Failure Number")
                self.plot.set_ylabel("Laplace Statistic")
                self.plot.grid(True)
            elif self.graphSettings.test == GraphSettings.RAA:
                t = AverageTest(self.container.data.getData())
                self.plot.step(t['FN'], t['RA'])
                # labels
                self.plot.set_title("Running Average Trend Test")
                self.plot.set_xlabel("Failure Number")
                self.plot.set_ylabel("Running Average of Interfailure Time")
                self.plot.grid(True)

        self.plot.figure.canvas.draw()

    def updateSheets(self):
        self.sideMenu.updateSheets()


class ModelTab(Tab):
    def __init__(self, container):
        super().__init__(container, Tab.MODEL_TAB)

    def updateGraph(self):
        pass
