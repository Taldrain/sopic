from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QColor

COLOR_DEFAULT = QColor(0, 0, 0, 0)
COLOR_PROGRESS = QColor(252, 252, 103)
COLOR_OK = QColor(73, 229, 76)
COLOR_KO = QColor(249, 72, 72)
COLOR_SKIPPED = QColor(128, 128, 128)


class StepStatusWidget(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)

        self.setAutoFillBackground(True)

        self.label = QLabel(name)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.label)

        self.setLayout(hlayout)

    def changeBackgroundColor(self, color):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def statusReset(self):
        self.changeBackgroundColor(COLOR_DEFAULT)

    def statusOK(self):
        self.changeBackgroundColor(COLOR_OK)

    def statusKO(self):
        self.changeBackgroundColor(COLOR_KO)

    def statusSkipped(self):
        self.changeBackgroundColor(COLOR_SKIPPED)

    def statusInProgress(self):
        self.changeBackgroundColor(COLOR_PROGRESS)
