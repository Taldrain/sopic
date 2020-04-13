import threading
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

from sopic.step import Step
from sopic.gui import StepUI

class EndButtonUI(StepUI):
    def __init__(self, parent=None, event=None):
        super().__init__(parent)
        self.event = event

        btn = QPushButton('OK')
        btn.clicked.connect(self.handleClick)

        htoplayout = QHBoxLayout()
        htoplayout.addWidget(btn)

        self.setLayout(htoplayout)

    @pyqtSlot()
    def handleClick(self):
        self.event.set()

class EndButton(Step):
    STEP_NAME = 'end-button'
    event = threading.Event()

    def start(self, stepsData):
        super().start()

        # we can display run information here
        self.logger.info("Has current run failed: {}".format("lastFailedStep" in stepsData['__status']))

        self.event.wait()
        self.event.clear()

        return self.OK()

    def getWidget(self):
        if self.widget is None:
            self.widget = EndButtonUI(event=self.event)

        return self.widget
