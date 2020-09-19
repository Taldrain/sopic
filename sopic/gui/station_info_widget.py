from PyQt5.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt


class StationInfoWidget(QWidget):
    def __init__(self, version, parent=None):
        super().__init__(parent)

        versionLabel = QLabel("Version: " + version)
        versionLabel.setAlignment(Qt.AlignRight)

        hlayout = QHBoxLayout()
        hlayout.addWidget(versionLabel)

        self.setLayout(hlayout)
