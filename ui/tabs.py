from ui.tab import Tab
from core.graphSettings import GraphSettings

class DataTab(Tab):
    CUMULATIVE = 0
    TBF = 1
    FINTENSITY = 2
    def __init__(self, container):
        super().__init__(container, Tab.DATA_TAB)
        self.graphMode = DataTab.CUMULATIVE

    def updateGraph(self):
        self.plot.clear()
        self.data = self.container.data

        if self.graphMode == DataTab.CUMULATIVE:
            # plot data
            # if onlp plotting poitns use plot
            if self.graphSettings.viewStyle == GraphSettings.POINTS:
                self.plot.plot(self.data["FT"], self.data["FN"],\
                self.graphSettings.viewStyleToPointStyle(), markersize=3)
            else:
                # if plotting lines use step
                self.plot.step(self.data["FT"], self.data["FN"],\
                self.graphSettings.viewStyleToPointStyle(), markersize=3)

            # labels
            self.plot.set_title("Number of Failures vs. Time ")
            self.plot.set_xlabel("Cumulative Time (s)")
            self.plot.set_ylabel("Number of Failures")
            self.plot.grid(True)

        elif self.graphMode == DataTab.TBF:
            pass


        self.plot.figure.canvas.draw()


class ModelTab(Tab):
    def __init__(self, container):
        super().__init__(container, Tab.MODEL_TAB)

    def updateGraph(self):
        pass
