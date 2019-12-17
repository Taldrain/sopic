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

    disableFileLogging = True

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
    Q_APP = QApplication(sys.argv)
    MainWindow(EndStepStation).show()
    sys.exit(Q_APP.exec_())
