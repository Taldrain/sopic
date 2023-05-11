#!/usr/bin/env python3

import sys
from PySide6 import QtWidgets

from sopic.station import Station
from sopic.gui import MainWindow

from examples.steps import Select, AlwaysOK, AlwaysKO


class BasicStation(Station):
    STATION_NAME = "basic station"
    STATION_ID = 0
    STATION_VERSION = "0.0.2"

    DEBUG = True

    dag = {
        # will allow to either go to `foo` or `bar`
        'start': (Select, {'ok': 'foo', 'ko': 'bar'}),
        'foo': (AlwaysOK, ['end']),
        'bar': (AlwaysKO, ['end']),
        'end': (Select, []),
    }

    start_step_key = 'start'


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    MainWindow(BasicStation).show()
    sys.exit(app.exec())
