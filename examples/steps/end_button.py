import threading
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot

from sopic.step import Step
from sopic.gui import StepUI

class EndButtonUI(StepUI):
    def __init__(self, parent = None, event = None):
        self.event = event
        super().__init__(parent)

    def init_gui(self):
        self.init_widgets()

        htoplayout = QHBoxLayout()
        htoplayout.addWidget(self.btn)

        self.setLayout(htoplayout)

    def init_widgets(self):
        self.btn = QPushButton('OK')
        self.btn.clicked.connect(self.slot_btn)

    @pyqtSlot()
    def slot_btn(self):
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
        if (self.widget == None):
            self.widget = EndButtonUI(event=self.event)

        return self.widget
