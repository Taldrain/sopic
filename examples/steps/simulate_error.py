import threading

from PySide6.QtWidgets import QPushButton, QHBoxLayout

from sopic.step import Step


class KOException(Exception):
    pass


class SimulateError(Step):
    STEP_NAME = "simulate-error"
    _event = threading.Event()
    _selection = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_ui()

    def start(self, *kwargs):
        super().start()

        self._event.wait()
        self._event.clear()

        try:
            if self._selection == "ok":
                return self.OK(self.get_step_key("ok"))

            if self._selection == "ko":
                raise KOException

            if self._selection == "throw":
                # uncatched exception
                raise Exception
        except KOException:
            return self.KO(self.get_step_key("ko"))

    def _init_ui(self):
        button_ok = QPushButton("OK")
        button_ok.clicked.connect(self.handle_click_ok)

        button_ko = QPushButton("KO - Cath error")
        button_ko.clicked.connect(self.handle_click_ko)

        button_throw = QPushButton("KO - Not catched error")
        button_throw.clicked.connect(self.handle_click_throw)

        htoplayout = QHBoxLayout()
        htoplayout.addWidget(button_ok)
        htoplayout.addWidget(button_ko)
        htoplayout.addWidget(button_throw)

        self.setLayout(htoplayout)

    def handle_click_ok(self):
        self._selection = "ok"
        self._event.set()

    def handle_click_ko(self):
        self._selection = "ko"
        self._event.set()

    def handle_click_throw(self):
        self._selection = "throw"
        self._event.set()
