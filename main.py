#!/usr/bin/env python3

import argparse # to handle command line arguments
from PyQt5.QtWidgets import QApplication # for UI
from PyQt5.QtCore import Qt # for UI
import logging as log # to handle debug output
import sys

from ui.mainWindow import *


def main():
    log.info("Hello From Main")

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser(description='Software Reliablity Tool')
    parser.add_argument("-v", '--verbose', action='store_true')

    args = parser.parse_args()

    if args.verbose:
    # if using verbose output set logging to display level and message
    # print anything level debug or higher
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Using Verbose output.")
    else:
    # if not using verbose output only brint errors and warnings
    log.basicConfig(format="%(levelname)s: %(message)s")

    main()














    #
