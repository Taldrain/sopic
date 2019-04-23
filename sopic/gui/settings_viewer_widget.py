from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

class SettingsViewerWidget(QWidget):
    def __init__(self, station, parent = None):
        super().__init__(parent)

        self.labels = {}
        self.station = station

        self.init_gui()

    def format_label(self, key, value):
        return '' + key + ': ' + value

    def init_gui(self):
        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignTop)
        settings = self.station.settings

        for key, value in settings.items():
            self.labels[key] = QLabel(self.format_label(key, value))

        for key, label in self.labels.items():
            vlayout.addWidget(label)

        self.setLayout(vlayout)


    def slot_update(self):
        settings = self.station.settings

        for key, value in settings.items():
            self.labels[key].setText(self.format_label(key, value))
