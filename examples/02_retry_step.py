#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import StartButton, Retry, End


class RetryStepStation(Station):
    STATION_NAME = "retry-step-station"
    STATION_ID = 2
    STATION_VERSION = "1.0.0"

    DEBUG = True

    dag = {
        'start': (StartButton, ['retry']),
        'retry': (Retry, ['end']),
        'end': (End, []),
    }


if __name__ == "__main__":
    app = QApplication([])
    MainWindow(RetryStepStation).show()
    sys.exit(app.exec())
