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
        log.info(type(self.plot))
        self.plot.clear()
        self.plot = self.graphSettings.generatePlot(self.plot, self.container.data)
        self.plot.figure.canvas.draw()

    def updateSheets(self):
        self.sideMenu.updateSheets()


class ModelTab(Tab):
    def __init__(self, container):
        super().__init__(container, Tab.MODEL_TAB)

    def updateGraph(self):
        pass
