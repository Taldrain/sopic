#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import Select, AlwaysOK


class BlockingStepStation(Station):
    DISPLAY_NAME = 'a station with blocking step'
    STATION_NAME = 'blocking-step-station'
    STATION_ID = 1

    disable_file_logging = True

    steps = [
        # whatever the output (KO or OK) the next step will always be called
        Select,
        AlwaysOK,
        Select,
    ]

    # all steps in the array returning KO will not block the run
    nonBlockingSteps = [
        'button-select',
    ]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow(BlockingStepStation)
    mainwindow.show()
    sys.exit(app.exec_())
