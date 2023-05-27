import logging

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import Signal, Slot, QObject
from PySide6.QtGui import QPalette, QColor, QFont

from sopic.utils.logger import widget_formatter

# prevents method clashing issue
class LogSignal(QObject):
    signal = Signal(str, int)

class LoggerWidget(QWidget, logging.Handler):
    _signal_wrapper = LogSignal()

    def __init__(self):
        QWidget.__init__(self)
        logging.Handler.__init__(self)

        self.text_widget = self._init_widgets()
        self._signal_wrapper.signal.connect(self.on_log)
        self._init_handler()

    def _init_widgets(self):
        layout = QVBoxLayout()

        logger = QTextEdit()
        logger.setReadOnly(True)
        # set background to black
        palette = logger.palette()
        palette.setColor(QPalette.Base, QColor(0, 0, 0))
        logger.setPalette(palette)
        # increase font size
        font = QFont()
        font.setPointSize(12)
        logger.setFont(font)

        layout.addWidget(logger)
        self.setLayout(layout)

        return logger

    def _init_handler(self):
        self.setLevel(logging.DEBUG)
        self.setFormatter(widget_formatter())

    def _level_to_style(self, level):
        if level == logging.CRITICAL:
            return "color:red;font-weight:bold"
        if level == logging.ERROR:
            return "color:red;"
        if level == logging.WARNING:
            return "color:yellow;"
        if level == logging.INFO:
            return "color:green;"
        return "color:white;"

    def emit(self, record):
        self._signal_wrapper.signal.emit(self.format(record), record.levelno)

    @Slot(str, int)
    def on_log(self, msg, level):
        style = self._level_to_style(level)
        self.text_widget.append(f'<span style="{style}">{msg}</span>')
