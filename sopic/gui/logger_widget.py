import logging

from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QBrush

from ..utils import getDefaultFormatter


class LoggerWidget(QPlainTextEdit, logging.Handler):
    signal = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        # super(logging.Handler).__init__()

        self.signal.connect(self.onLog)
        self.setFormatter(getDefaultFormatter())
        self.setReadOnly(True)

    def emit(self, record):
        self.signal.emit(self.format(record), record.levelno)

    def write(self, data):
        pass

    @pyqtSlot(str, int)
    def onLog(self, log, level):
        color = Qt.black
        if level in [logging.CRITICAL, logging.ERROR]:
            color = Qt.red
        elif level == logging.WARNING:
            color = QColor(240, 143, 58)
        elif level == logging.INFO:
            color = QColor(6, 120, 21)
        charFormat = self.currentCharFormat()
        charFormat.setForeground(QBrush(color))
        self.setCurrentCharFormat(charFormat)
        self.appendPlainText(log)
