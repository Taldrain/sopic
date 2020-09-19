#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QLabel, QLineEdit, QApplication

from sopic.station import Station
from sopic.gui import MainWindow, MainSettingsDialog

from examples.steps import Select, PrintSettings


class SettingsStation(Station):
    DISPLAY_NAME = "station with settings"
    STATION_NAME = "settings-station"
    STATION_ID = 3

    disableFileLogging = True

    steps = [
        Select,
        PrintSettings,
        Select,
    ]

    defaultSettings = {
        "random-settings": "42",
    }


class SettingsDialog(MainSettingsDialog):
    textWidget = None

    # Required
    # Initialize the gui
    def initUI(self):
        self.textWidget = QLineEdit()
        self.textWidget.textChanged.connect(self.handleText)

        self.widgets = [
            [QLabel("Random setting: "), self.textWidget],
        ]

    # Required
    # Reset the fields with the data from `self.settings`
    def initValues(self):
        self.textWidget.setText(self.settings["random-settings"])

    def handleText(self):
        self.cbUpdateSettings("random-settings", self.textWidget.text())


if __name__ == "__main__":
    Q_APP = QApplication(sys.argv)
    MainWindow(SettingsStation, SettingsDialog).show()
    sys.exit(Q_APP.exec_())
