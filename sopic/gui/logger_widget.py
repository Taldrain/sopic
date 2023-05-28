import re
import logging

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QComboBox
from PySide6.QtCore import Signal, Slot, QObject, Qt
from PySide6.QtGui import QPalette, QColor, QFont, QKeyEvent

from sopic.utils.logger import widget_formatter

# prevents method clashing issue
class LogSignal(QObject):
    signal = Signal(str, int)

class LoggerWidget(QWidget, logging.Handler):
    _signal_wrapper = LogSignal()

    def __init__(self):
        QWidget.__init__(self)
        logging.Handler.__init__(self)

        self._logs = []

        self._text_widget, self._level_widget = self._init_widgets()
        self._signal_wrapper.signal.connect(self.on_log)
        self._init_handler()

    def _init_widgets(self):
        layout = QVBoxLayout()

        # text widget
        text_widget = QTextEdit()
        text_widget.setReadOnly(True)
        # set background to black
        palette = text_widget.palette()
        palette.setColor(QPalette.Base, QColor(0, 0, 0))
        text_widget.setPalette(palette)
        # increase font size
        font = QFont()
        font.setPointSize(12)
        text_widget.setFont(font)

        # log level widget
        level_widget = QComboBox()
        level_widget.addItem("DEBUG", userData=logging.DEBUG)
        level_widget.addItem("INFO", userData=logging.INFO)
        level_widget.addItem("WARNING", userData=logging.WARNING)
        level_widget.addItem("ERROR", userData=logging.ERROR)
        level_widget.addItem("CRITICAL", userData=logging.CRITICAL)

        level_widget.setCurrentIndex(0)
        level_widget.currentIndexChanged.connect(self._handle_level_filter)

        layout.addWidget(text_widget)
        layout.addWidget(level_widget)
        self.setLayout(layout)

        return text_widget, level_widget

    def _init_handler(self):
        self.setLevel(logging.DEBUG)
        self.setFormatter(widget_formatter())

    def _level_to_style(self, level):
        if level == logging.CRITICAL:
            return "color:red;font-weight:bold;"
        if level == logging.ERROR:
            return "color:red;"
        if level == logging.WARNING:
            return "color:yellow;"
        if level == logging.INFO:
            return "color:green;"
        return "color:white;"

    def emit(self, record):
        self._signal_wrapper.signal.emit(self.format(record), record.levelno)

    def _handle_level_filter(self):
        selected_level = self._level_widget.currentData()
        filtered_logs = []
        for line in self._logs:
            match = re.match(r'^<span level=\"(\d+)\".*', line)
            level = int(match.group(1))
            if level >= selected_level:
                filtered_logs.append(line)
        self._text_widget.setHtml('<br>'.join(filtered_logs))

    @Slot(str, int)
    def on_log(self, msg, level):
        style = self._level_to_style(level)
        msg_html = f'<span level="{level}" style="{style}">{msg}</span>'
        self._logs.append(msg_html)
        if level >= self._level_widget.currentData():
            self._text_widget.append(msg_html)

    def event(self, event):
        if event.type() == QKeyEvent.KeyPress:
            if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_L:
                self._logs.clear()
                self._text_widget.clear()
                return True
        return super().event(event)

    def close(self):
        # prevent issue with LoggingHandler closing before the widget
        pass
