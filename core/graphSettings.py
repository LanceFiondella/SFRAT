

class GraphSettings:
    POINTS = 0
    LINES = 1
    BOTH = 2

    CUMULATIVE = 0
    TBF = 1
    FINTENSITY = 2

    DATA = 0
    TREND = 1

    def __init__(self):
        self.viewStyle = GraphSettings.BOTH
        self.dataMode = GraphSettings.CUMULATIVE
        self.showTrend = GraphSettings.DATA
    # convert view style to matlplot lib graph syntax
    def viewStyleToPointStyle(self):
        if self.viewStyle == GraphSettings.LINES:
            return "-"
        elif self.viewStyle == GraphSettings.POINTS:
            return "o"
        elif self.viewStyle == GraphSettings.BOTH:
            return "-o"
