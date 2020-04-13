#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import Select, AlwaysOK, AlwaysKO

class BasicStation(Station):
    DISPLAY_NAME = 'basic station'
    STATION_NAME = 'basic-station'
    STATION_ID = 0

    disableFileLogging = True

    steps = [
        Select,
        AlwaysOK,
        # This step will always return KO,
        # the next step will always be skipped
        AlwaysKO,
        # Never called
        Select,
        Select,
    ]

if __name__ == '__main__':
    Q_APP = QApplication(sys.argv)
    MainWindow(BasicStation).show()
    sys.exit(Q_APP.exec_())
