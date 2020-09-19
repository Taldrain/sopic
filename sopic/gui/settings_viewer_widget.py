from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


def formatLabel(key, value):
    return "" + key + ": " + value


class SettingsViewerWidget(QWidget):
    def __init__(self, station, parent=None):
        super().__init__(parent)

        self.labels = {}
        self.station = station

        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignTop)
        settings = self.station.settings

        for key, value in settings.items():
            self.labels[key] = QLabel(formatLabel(key, value))

        for key, label in self.labels.items():
            vlayout.addWidget(label)

        self.setLayout(vlayout)

    def refresh(self):
        settings = self.station.settings

        for key, value in settings.items():
            self.labels[key].setText(formatLabel(key, value))
