#!/usr/bin/env python3

import sys
from PySide6 import QtWidgets

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import Select, PrintSettings, GetSettings


class SettingsStation(Station):
    STATION_NAME = "settings-station"
    STATION_ID = 3
    STATION_VERSION = "0.0.1"

    DEBUG = True

    dag = {
        'start': (Select, {'ok': 'print', 'ko': 'end'}),
        'print': (PrintSettings, ['get']),
        'get': (GetSettings, ['end']),
        'end': (Select, []),
    }

    default_settings = {
        "random-settings": { "value": 42, "label": "A random settings" },
        "read-only": { "value": 12, "label": "Read-only settings", "edit": False },
        "no-label": { "value": "hello" },
    }


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    MainWindow(SettingsStation).show()
    sys.exit(app.exec())
