from copy import deepcopy
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
)

from .settings_widgets import string_widget


class SettingsDialogWidget(QDialog):
    def __init__(self, get_settings_handler, reset_handler, save_handler, parent=None):
        super(SettingsDialogWidget, self).__init__(parent)

        self.setWindowTitle("Settings")

        self.get_settings_handler = get_settings_handler
        self.reset_handler = reset_handler
        self.save_handler = save_handler

        self._settings = self.get_settings_handler()
        self._reset_widgets = dict()

        form_layout = QFormLayout()

        for key in self._settings.keys():
            # default to the string widget
            widget = string_widget
            # otherwhise use the `widget` key in the `default_settings` object
            if ('widget' in self._settings[key]):
                widget = self._settings[key]['widget']
            label, input, reset = widget(key, self._settings[key], self.on_change)
            self._reset_widgets[key] = reset
            form_layout.addRow(label, input)

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.handle_reset)

        validate_btn = QPushButton("OK")
        validate_btn.clicked.connect(self.handle_validate)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(validate_btn)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def on_change(self, key, value):
        self._settings.get(key).update({"value": value})

    def handle_validate(self):
        self.save_handler(deepcopy(self._settings))
        super().accept()

    def handle_reset(self):
        self.reset_handler()
        self._settings = self.get_settings_handler()
        for key in self._settings.keys():
            self._reset_widgets[key](self._settings[key]["value"])
