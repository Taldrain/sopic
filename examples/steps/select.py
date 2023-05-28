import threading

from PySide6.QtWidgets import QPushButton, QHBoxLayout
from PySide6.QtCore import Slot

from sopic.step import Step
from sopic.gui import StepUI

# Dirty
# sharing data between the StepUI and the Step
# which button was clicked
IS_OK = True


class SelectUI(StepUI):
    def __init__(self, event):
        super().__init__()
        self._event = event

        buttonOK = QPushButton("OK")
        buttonOK.clicked.connect(self.handleClickOK)

        buttonKO = QPushButton("KO")
        buttonKO.clicked.connect(self.handleClickKO)

        htoplayout = QHBoxLayout()
        htoplayout.addWidget(buttonOK)
        htoplayout.addWidget(buttonKO)

        self.setLayout(htoplayout)

    @Slot()
    def handleClickOK(self):
        global IS_OK
        IS_OK = True
        self._event.set()

    @Slot()
    def handleClickKO(self):
        global IS_OK
        IS_OK = False
        self._event.set()


class Select(Step):
    STEP_NAME = "button-select"
    _event = threading.Event()

    def start(self, *kwargs):
        super().start()

        self._event.wait()
        self._event.clear()

        global IS_OK
        if IS_OK:
            return self.OK(self.get_step_key("ok"))

        return self.KO(self.get_step_key("ko"))

    def getWidget(self):
        if self.widget is None:
            self.widget = SelectUI(self._event)

        return self.widget
