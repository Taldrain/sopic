#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication

from sopic import MainWindow, Station

from examples.steps import StartButton, Retry


class RetryStepStation(Station):
    STATION_NAME = "retry-step-station"
    STATION_ID = 2
    STATION_VERSION = "1.0.0"

    DEBUG = True

    dag = {
        "start": (StartButton, ["retry"]),
        "retry": (Retry, []),
    }


if __name__ == "__main__":
    app = QApplication([])
    MainWindow(RetryStepStation).show()
    sys.exit(app.exec())
