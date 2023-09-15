#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication

from sopic import MainWindow, Station

from examples.steps import StartButton, StoreData, RetrieveData


class StepDataStation(Station):
    STATION_NAME = "step data station"
    STATION_ID = 4
    STATION_VERSION = "1.0.0"

    DEBUG = True

    dag = {
        "start": (StartButton, ["store"]),
        "store": (StoreData, ["retrieve"]),
        "retrieve": (RetrieveData, []),
    }


if __name__ == "__main__":
    app = QApplication([])
    MainWindow(StepDataStation).show()
    sys.exit(app.exec())
