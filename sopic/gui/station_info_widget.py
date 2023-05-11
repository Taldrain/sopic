from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt


class StationInfoWidget(QWidget):
    def __init__(self, version):
        super().__init__()

        version_label = QLabel("Version: " + version)
        version_label.setAlignment(Qt.AlignRight)

        layout = QHBoxLayout()
        layout.addWidget(version_label)

        self.setLayout(layout)
