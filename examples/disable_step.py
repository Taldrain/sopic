#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import Select, AlwaysOK


class DisabledStepStation(Station):
    DISPLAY_NAME = 'a station with step disabled by default'
    STATION_NAME = 'disabled-step-station'
    STATION_ID = 2

    disable_file_logging = True

    steps = [
        Select,
        # Disabled by default, can be re-activate in the station
        # with Ctrl-T
        (AlwaysOK, False),
        Select,
    ]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow(DisabledStepStation)
    mainwindow.show()
    sys.exit(app.exec_())
