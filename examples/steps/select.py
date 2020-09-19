import threading
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

from sopic.step import Step
from sopic.gui import StepUI

# Dirty
# sharing data between the StepUI and the Step
# which button was clicked
IS_OK = True


class SelectUI(StepUI):
    def __init__(self, parent=None, event=None):
        super().__init__(parent)
        self.event = event

        buttonOK = QPushButton("OK")
        buttonOK.clicked.connect(self.handleClickOK)

        buttonKO = QPushButton("KO")
        buttonKO.clicked.connect(self.handleClickKO)

        htoplayout = QHBoxLayout()
        htoplayout.addWidget(buttonOK)
        htoplayout.addWidget(buttonKO)

        self.setLayout(htoplayout)

    @pyqtSlot()
    def handleClickOK(self):
        global IS_OK
        IS_OK = True
        self.event.set()

    @pyqtSlot()
    def handleClickKO(self):
        global IS_OK
        IS_OK = False
        self.event.set()


class Select(Step):
    STEP_NAME = "button-select"
    event = threading.Event()

    def start(self, _stepsData):
        super().start()

        self.event.wait()
        self.event.clear()

        global IS_OK
        if IS_OK:
            return self.OK()

        return self.KO()

    def getWidget(self):
        if self.widget is None:
            self.widget = SelectUI(event=self.event)

        return self.widget
