from os.path import exists, dirname, realpath
from setuptools import setup, find_packages
import sys
setup(
    # Qt5 regularly drops support for older osx versions, so you might
    # want to use an older version of PyQt5. See also:
    # http://doc.qt.io/QtForDeviceCreation/qtee-changelog.html#boot-to-qt-5-9-6
    # For instance, to support osx 10.10, use:
    # install_requires=["pyqt5<5.10"],
    install_requires=["pyqt5<5.10"],
    setup_requires=['pytest-runner'],
    tests_require=["pytest", "pytest-qt"],
    platforms=['ALL'],
    )