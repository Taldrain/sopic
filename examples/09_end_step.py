#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import Select, PrintSettings, EndButton, StartButton

class EndStepStation(Station):
    DISPLAY_NAME = 'station with end step'
    STATION_NAME = 'end-step-station'
    STATION_ID = 9

    disable_file_logging = True

    steps = [
        Select,
        PrintSettings,
        Select,
    ]

    startStep = StartButton
    endStep = EndButton

    defaultSettings = {
        'random-settings': '42',
    }


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow(EndStepStation)
    mainwindow.show()
    sys.exit(app.exec_())
