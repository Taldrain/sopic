import threading

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel


class StartScreenWidget(QWidget):
    TAB_NAME = "Start screen"

    event = threading.Event()

    def __init__(self):
        super().__init__()

        self._init_widgets()

        vlayout = QVBoxLayout()

        vlayout.addWidget(self.run_status_label)
        vlayout.addWidget(self.steps_failed_label)
        vlayout.addWidget(self.btn)
        vlayout.setAlignment(Qt.AlignLeft | Qt.AlignCenter)

        self.setLayout(vlayout)

    def _init_widgets(self):
        self.run_status_label = QLabel("")

        self.steps_failed_label = QLabel("")
        self.steps_failed_label.setStyleSheet("QLabel {font-size: 24px}")

        self.btn = QPushButton("")
        self.btn.setFixedSize(QSize(250, 80))
        self.btn.setStyleSheet("QPushButton {font-size: 24px}")
        self.btn.clicked.connect(self._btn_clicked)

    def _btn_clicked(self):
        self.btn.setEnabled(False)
        self.event.set()

    def _format_fail(self, fail):
        res = fail["stepName"]
        if fail["infoStr"] is not None:
            res += ": {}".format(fail["infoStr"])
        if fail["errorCode"] is not None:
            res += " (error code: {})".format(fail["errorCode"])
        return res

    def _show_step_failed(self, fails):
        print(f"{fails=}")
        if len(fails) <= 0:
            self.steps_failed_label.setText("")
            return

        output_str = "Step{} failed:\n".format(len(fails) > 1 and "s" or "")
        for fail in fails:
            output_str += "- {}\n".format(self._format_fail(fail))
        self.steps_failed_label.setText(output_str)

    def start(self, first_run=False, is_success=False, fails=[]):
        if first_run:
            self.btn.setText("Start run")
        else:
            self.btn.setText("Start next run")
            self._show_step_failed(fails)
            if is_success:
                self.run_status_label.setText("Station passed")
                self.run_status_label.setStyleSheet(
                    "QLabel {color: green;font-size: 32px}"
                )
            else:
                self.run_status_label.setText("Station failed")
                self.run_status_label.setStyleSheet(
                    "QLabel {color: red;font-size: 32px}"
                )

        self.btn.setEnabled(True)

        self.event.wait()
        self.event.clear()

        return
