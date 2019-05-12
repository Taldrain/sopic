#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import StoreData, RetrieveData, Select

class StepDataStation(Station):
    DISPLAY_NAME = 'step data station'
    STATION_NAME = 'step-data-station'
    STATION_ID = 6

    disable_file_logging = True

    steps = [
        StoreData,
        RetrieveData,
        Select,
    ]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow(StepDataStation)
    mainwindow.show()
    sys.exit(app.exec_())
