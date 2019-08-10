import threading
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot

from sopic.step import Step
from sopic.gui import StepUI

# Dirty
# sharing data between the StepUI and the Step
# which button was clicked
IS_OK = True

class SelectUI(StepUI):
    def __init__(self, parent = None, event = None):
        self.event = event
        super().__init__(parent)

    def init_gui(self):
        self.init_widgets()

        htoplayout = QHBoxLayout()
        htoplayout.addWidget(self.ok_btn)
        htoplayout.addWidget(self.ko_btn)

        self.setLayout(htoplayout)

    def init_widgets(self):
        self.ok_btn = QPushButton('OK')
        self.ok_btn.clicked.connect(self.slot_ok)

        self.ko_btn = QPushButton('KO')
        self.ko_btn.clicked.connect(self.slot_ko)

    @pyqtSlot()
    def slot_ok(self):
        global IS_OK
        IS_OK=True
        self.event.set()

    @pyqtSlot()
    def slot_ko(self):
        global IS_OK
        IS_OK=False
        self.event.set()

class Select(Step):
    STEP_NAME = 'button-select'
    event = threading.Event()

    def start(self, stepsData):
        super().start()

        self.event.wait()
        self.event.clear()

        global IS_OK
        if (IS_OK is True):
            return self.OK()

        return self.KO()

    def getWidget(self):
        if (self.widget == None):
            self.widget = SelectUI(event = self.event)

        return self.widget
