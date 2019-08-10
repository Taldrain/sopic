import threading
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot

from sopic.step import Step
from sopic.gui import StepUI

class StartButtonUI(StepUI):
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

class StartButton(Step):
    STEP_NAME = 'start-button'
    event = threading.Event()

    def start(self, stepsData):
        super().start()

        self.event.wait()
        self.event.clear()

        return self.OK()

    def getWidget(self):
        if (self.widget == None):
            self.widget = StartButtonUI(event=self.event)

        return self.widget
