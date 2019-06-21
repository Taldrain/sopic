#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import Retry, Select

class RetryStepStation(Station):
    DISPLAY_NAME = 'retry step station'
    STATION_NAME = 'retry-step-station'
    STATION_ID = 7

    disable_file_logging = True

    steps = [
        Retry,
        Select,
    ]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow(RetryStepStation)
    mainwindow.show()
    sys.exit(app.exec_())