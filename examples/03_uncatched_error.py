#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import StartButton, End, SimulateError


class UncatchedException(Station):
    STATION_NAME = "blocking step station"
    STATION_ID = 3
    STATION_VERSION = "1.0.0"

    DEBUG = True

    dag = {
        'start': (StartButton, ['error']),
        'error': (SimulateError, {'ok': 'end', 'ko': 'end', '_err': 'end'}),
        'end': (End, []),
    }


if __name__ == "__main__":
    app = QApplication([])
    MainWindow(UncatchedException).show()
    sys.exit(app.exec())
