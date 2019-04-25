#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import Select, AlwaysOK

print("==> ", Select.STEP_NAME)

class StepSkippedStation(Station):
    DISPLAY_NAME = 'station with step skipped on fail'
    STATION_NAME = 'step-skipped-station'

    STATION_ID = 4

    disable_file_logging = True

    steps = [
        Select,
        Select,
        # If one of the previous steps has failed, the step will be skipped,
        # even if the previous steps is not blocking
        AlwaysOK,
        Select,
    ]

    nonBlockingSteps = [
        Select.STEP_NAME,
    ]

    stepsSkippedOnPreviousFail = [
        AlwaysOK.STEP_NAME,
    ]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow(StepSkippedStation)
    mainwindow.show()
    sys.exit(app.exec_())
