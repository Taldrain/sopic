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

    disable_file_logging = True

    # Should be set from an environment variable
    admin_password = "sopic"

    steps = [
        Select,
        PrintSettings,
        Select,
    ]

    defaultSettings = {
        'random-settings': '42',
    }


class SettingsDialog(MainSettingsDialog):
    def init_gui(self):
        self.init_widgets()

        self.widgets = [
            [ QLabel("Random setting: "), self.text_widget ],
        ]

    def init_widgets(self):
        self.text_widget = QLineEdit()
        self.text_widget.textChanged.connect(self.slot_text)

    # Required
    # Reset the fields with the data from `self.settings`
    def init_values(self):
        self.text_widget.setText(self.settings['random-settings'])

    def slot_text(self):
        self.cbUpdateSettings('random-settings', self.text_widget.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow(PasswordStation, SettingsDialog)
    mainwindow.show()
    sys.exit(app.exec_())
