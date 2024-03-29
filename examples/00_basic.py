#!/usr/bin/env python3

import sys
from PySide6.QtWidgets import QApplication

from sopic import MainWindow, Station

from examples.steps import Select, AlwaysOK, AlwaysKO


class BasicStation(Station):
    STATION_NAME = "basic station"
    STATION_ID = 0
    STATION_VERSION = "1.0.0"

    DEBUG = True

    dag = {
        # will allow to either go to step `foo` or `bar`
        "select": (Select, {"ok": "foo", "ko": "bar"}),
        "foo": (AlwaysOK, []),
        "bar": (AlwaysKO, []),
    }

    start_step_key = "select"


if __name__ == "__main__":
    app = QApplication([])
    MainWindow(BasicStation).show()
    sys.exit(app.exec())
