import threading

from PySide6.QtWidgets import QPushButton, QHBoxLayout
from PySide6.QtCore import Slot

from sopic.step import Step
from sopic.gui import StepUI


class StartButtonUI(StepUI):
    def __init__(self, event):
        super().__init__()
        self._event = event

        btn = QPushButton("Start")
        btn.clicked.connect(self.handleClick)

        htoplayout = QHBoxLayout()
        htoplayout.addWidget(btn)

        self.setLayout(htoplayout)

    @Slot()
    def handleClick(self):
        self._event.set()


class StartButton(Step):
    STEP_NAME = "start-button"
    _event = threading.Event()

    def start(self, *kwargs):
        super().start()

        self._event.wait()
        self._event.clear()

        return self.OK()

    def getWidget(self):
        if self.widget is None:
            self.widget = StartButtonUI(event=self._event)

        return self.widget
