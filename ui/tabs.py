from ui.tab import Tab

class DataTab(Tab):
    def __init__(self, container):
        super().__init__(container, Tab.DATA_TAB)

    def updateGraph(self):
        pass


class ModelTab(Tab):
    def __init__(self, container):
        super().__init__(container, Tab.MODEL_TAB)

    def updateGraph(self):
        pass
