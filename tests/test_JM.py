import unittest
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from models.JM import JM
import pandas as pd


class JMTest(unittest.TestCase):

    def setUp(self):
        fname = "model_data.xlsx"
        rawData = pd.read_excel(fname, sheet_name='SYS1')
        self.jm = JM(data=rawData, rootAlgoName='bisect')
        self.jm.findParams(0)

    def test_NOMLE(self):
        self.assertLess(abs(self.jm.N0MLE - 141.902891867), 10**-5)

    def test_PHIMLE(self):
        self.assertLess(abs(self.jm.phiMLE - 3.4966515966450457e-05), 10**-5)


if __name__ == '__main__':
    unittest.main()
