from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QColor, QPalette

COLOR_DEFAULT = QColor(0, 0, 0, 0)
COLOR_PROGRESS = QColor(252, 252, 103)
COLOR_OK = QColor(73, 229, 76)
COLOR_KO = QColor(249, 72, 72)
COLOR_SKIPPED = QColor(128, 128, 128)

class StepStatusWidget(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.setAutoFillBackground(True)
        self.init_gui()

    def init_gui(self):
        self.init_widgets()

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.label)

        self.setLayout(hlayout)

    def init_widgets(self):
        self.label = QLabel(self.name)

    def change_background_color(self, color):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def reset(self):
        self.change_background_color(COLOR_DEFAULT)

    def ok(self):
        self.change_background_color(COLOR_OK)

    def ko(self):
        self.change_background_color(COLOR_KO)

    def skipped(self):
        self.change_background_color(COLOR_SKIPPED)

    def in_progress(self):
        self.change_background_color(COLOR_PROGRESS)
