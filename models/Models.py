import os
import importlib
from . import *

class Models:
    models = {}
    def __init__(self):
        dirname = os.path.dirname(os.path.realpath(__file__))

        for file in os.listdir(dirname):
            # if the file is a python script add the
            if file.endswith(".py") and file != "__init__.py" \
            and file != "Models.py":
                # import the module
#                importlib.import_module("models." + file[:-3])
                # create an instance of the class
                self.models[file[:-3]] = \
                eval("%s.%s()" % (file[:-3], file[:-3]))
