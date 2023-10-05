#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication

from sopic import MainWindow, Station
from sopic.gui.settings_widgets import number_widget, bool_widget, combobox_widget

from examples.steps import StartButton, PrintSettings, GetSettings

class SettingsStation(Station):
    STATION_NAME = "custom-settings-widget-station"
    STATION_ID = 1
    STATION_VERSION = "1.0.0"

    DEBUG = True

    dag = {
        "start": (StartButton, ["print"]),
        "print": (PrintSettings, ["get"]),
        "get": (GetSettings, []),
    }

    # the widget key allow to use specific widgets for the settings
    default_settings = {
        "random-settings": {
            "value": "foo",
            "label": "A random settings",
        },
        "int-settings": {
            "value": 42,
            "label": "A random int settings",
            "widget": number_widget
        },
        "bool-settings": {
            "value": True,
            "label": "A random bool settings",
            "widget": bool_widget
        },
        "combobox-settings": {
            "value": "lorem",
            "values": ["lorem", "ipsum", "dolor", "sit", "amet"],
            "label": "A random combobox settings",
            "widget": combobox_widget
        }
    }


if __name__ == "__main__":
    app = QApplication([])
    MainWindow(SettingsStation).show()
    sys.exit(app.exec())
