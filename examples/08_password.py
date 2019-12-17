#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QLabel, QLineEdit, QApplication

from sopic.station import Station
from sopic.gui import MainWindow, MainSettingsDialog

from examples.steps import Select, PrintSettings

class PasswordStation(Station):
    DISPLAY_NAME = 'station with password'
    STATION_NAME = 'password-station'
    STATION_ID = 8

    disableFileLogging = True

    # Should be set from an environment variable
    adminPassword = "sopic"

    steps = [
        Select,
        PrintSettings,
        Select,
    ]

    defaultSettings = {
        'random-settings': '42',
    }


class SettingsDialog(MainSettingsDialog):
    def initUI(self):
        self.textWidget = QLineEdit()
        self.textWidget.textChanged.connect(self.handleText)

        self.widgets = [
            [QLabel("Random setting: "), self.textWidget],
        ]

    # Required
    # Reset the fields with the data from `self.settings`
    def initValues(self):
        self.textWidget.setText(self.settings['random-settings'])

    def handleText(self):
        self.cbUpdateSettings('random-settings', self.textWidget.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow(PasswordStation, SettingsDialog)
    mainwindow.show()
    sys.exit(app.exec_())
