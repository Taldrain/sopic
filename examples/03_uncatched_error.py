#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication

from sopic import MainWindow, Station

from examples.steps import StartButton, SimulateError, Uncatched, Catched


class UncatchedException(Station):
    STATION_NAME = "blocking step station"
    STATION_ID = 3
    STATION_VERSION = "1.0.0"

    DEBUG = True

    dag = {
        "start": (StartButton, ["error"]),
        "error": (SimulateError, {"ko": "catched", "_err": "uncatched"}),
        "catched": (Catched, []),
        "uncatched": (Uncatched, []),
    }


if __name__ == "__main__":
    app = QApplication([])
    MainWindow(UncatchedException).show()
    sys.exit(app.exec())
