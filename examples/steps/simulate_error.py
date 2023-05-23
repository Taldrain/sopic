import threading

from PySide6.QtWidgets import QPushButton, QHBoxLayout
from PySide6.QtCore import Slot

from sopic.step import Step
from sopic.gui import StepUI

SELECTION = ""

class KOException(Exception):
    pass

class SimulateErrorUI(StepUI):
    def __init__(self, event):
        super().__init__()
        self._event = event

        buttonOK = QPushButton("OK")
        buttonOK.clicked.connect(self.handleClickOK)

        buttonKO = QPushButton("KO - Cath error")
        buttonKO.clicked.connect(self.handleClickKO)

        buttonThrow = QPushButton("KO - Not catched error")
        buttonThrow.clicked.connect(self.handleClickThrow)

        htoplayout = QHBoxLayout()
        htoplayout.addWidget(buttonOK)
        htoplayout.addWidget(buttonKO)
        htoplayout.addWidget(buttonThrow)

        self.setLayout(htoplayout)

    @Slot()
    def handleClickOK(self):
        global SELECTION
        SELECTION = "ok"
        self._event.set()

    @Slot()
    def handleClickKO(self):
        global SELECTION
        SELECTION = "ko"
        self._event.set()

    @Slot()
    def handleClickThrow(self):
        global SELECTION
        SELECTION = "throw"
        self._event.set()



class SimulateError(Step):
    STEP_NAME = "simulate-error"
    _event = threading.Event()

    def start(self, *kwargs):
        super().start()

        self._event.wait()
        self._event.clear()

        global SELECTION
        try:
            if SELECTION == 'ok':
                return self.OK(self.get_step_key('ok'))

            if SELECTION == 'ko':
                raise KOException

            if SELECTION == 'throw':
                raise Exception
        except KOException:
            return self.KO(self.get_step_key('ko'))

    def getWidget(self):
        if self.widget is None:
            self.widget = SimulateErrorUI(self._event)

        return self.widget
