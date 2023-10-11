import threading

from PySide6.QtWidgets import QPushButton, QHBoxLayout

from sopic.step import Step


class Select(Step):
    STEP_NAME = "button-select"
    _event = threading.Event()
    _selected_ok = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_ui()

    def start(self, *kwargs):
        super().start()

        self._event.wait()
        self._event.clear()

        if self._selected_ok:
            return self.OK(self.get_step_key("ok"))

        return self.KO(self.get_step_key("ko"), "KO button clicked")

    def _init_ui(self):
        button_ok = QPushButton("OK")
        button_ok.clicked.connect(self._handle_click_ok)

        button_ko = QPushButton("KO")
        button_ko.clicked.connect(self._handle_click_ko)

        htoplayout = QHBoxLayout()
        htoplayout.addWidget(button_ok)
        htoplayout.addWidget(button_ko)
        self.setLayout(htoplayout)

    def _handle_click_ok(self):
        self._selected_ok = True
        self._event.set()

    def _handle_click_ko(self):
        self._selected_ok = False
        self._event.set()
