import threading
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

from sopic.step import Step
from sopic.gui import StepUI


class StartButtonUI(StepUI):
    def __init__(self, parent=None, event=None):
        super().__init__(parent)
        self.event = event

        btn = QPushButton("OK")
        btn.clicked.connect(self.handleClick)

        htoplayout = QHBoxLayout()
        htoplayout.addWidget(btn)

        self.setLayout(htoplayout)

    @pyqtSlot()
    def handleClick(self):
        self.event.set()


class StartButton(Step):
    STEP_NAME = "start-button"
    event = threading.Event()

    def start(self, _stepsData):
        super().start()

        self.event.wait()
        self.event.clear()

        return self.OK()

    def getWidget(self):
        if self.widget is None:
            self.widget = StartButtonUI(event=self.event)

        return self.widget
