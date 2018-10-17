import os

__all__ = []

dirname = os.path.dirname(os.path.realpath(__file__))

for file in os.listdir(dirname):
    # if the file is a python script add the
    if file.endswith(".py") and file != "__init__.py" and file != "Models.py":
        __all__.append(file[:-3])
