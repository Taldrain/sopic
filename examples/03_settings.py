#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QLabel, QLineEdit, QApplication

from sopic.station import Station
from sopic.gui import MainWindow, MainSettingsDialog

from examples.steps import Select, PrintSettings

class SettingsStation(Station):
    DISPLAY_NAME = 'station with settings'
    STATION_NAME = 'settings-station'
    STATION_ID = 3

    disable_file_logging = True

    steps = [
        Select,
        PrintSettings,
        Select,
    ]

    defaultSettings = {
        'random-settings': '42',
    }


class SettingsDialog(MainSettingsDialog):
    # Required
    # Initialize the gui
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
    mainwindow = MainWindow(SettingsStation, SettingsDialog)
    mainwindow.show()
    sys.exit(app.exec_())
