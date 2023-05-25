#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import StartButton, PrintSettings, GetSettings, End


class SettingsStation(Station):
    STATION_NAME = "settings-station"
    STATION_ID = 1
    STATION_VERSION = "1.0.0"

    DEBUG = True

    dag = {
        'start': (StartButton, ['print']),
        'print': (PrintSettings, ['get']),
        'get': (GetSettings, ['end']),
        'end': (End, []),
    }

    default_settings = {
        "random-settings": { "value": 42, "label": "A random settings" },
        "read-only": { "value": 12, "label": "Read-only settings", "edit": False },
        "no-label": { "value": "hello" },
    }


if __name__ == "__main__":
    app = QApplication([])
    MainWindow(SettingsStation).show()
    sys.exit(app.exec())