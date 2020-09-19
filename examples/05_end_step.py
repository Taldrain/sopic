#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import Select, AlwaysOK, End


class EndStepStation(Station):
    DISPLAY_NAME = "end step station"
    STATION_NAME = "end-step-station"
    STATION_ID = 5

    disableFileLogging = True

    steps = [
        Select,
        AlwaysOK,
        End,
    ]


if __name__ == "__main__":
    Q_APP = QApplication(sys.argv)
    MainWindow(EndStepStation).show()
    sys.exit(Q_APP.exec_())
