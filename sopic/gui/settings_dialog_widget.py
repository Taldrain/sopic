from copy import deepcopy
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QLineEdit,
    QLabel,
)


class SettingsDialogWidget(QDialog):
    def __init__(self, get_settings_handler, reset_handler, save_handler, parent=None):
        super(SettingsDialogWidget, self).__init__(parent)

        self.setWindowTitle("Settings")

        self.get_settings_handler = get_settings_handler
        self.reset_handler = reset_handler
        self.save_handler = save_handler

        self._settings = self.get_settings_handler()
        self._inputs_widgets = dict()

        form_layout = QFormLayout()

        for key in self._settings.keys():
            label, input = self.generate_settings_widget(
                key,
                self._settings[key],
            )
            self._inputs_widgets[key] = input
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

    def generate_settings_widget(self, key, settings):
        label = QLabel(settings["label"] if "label" in settings else key)
        input = QLineEdit()
        input.setText(str(settings["value"]))
        input.setReadOnly(settings["edit"] is False if "edit" in settings else False)
        input.textEdited.connect(lambda:
            self._settings.get(key).update({ "value": input.text() }))
        return (label, input)

    def handle_validate(self):
        self.save_handler(deepcopy(self._settings))
        super().accept()

    def handle_reset(self):
        self.reset_handler()
        self._settings = self.get_settings_handler()
        for key in self._settings.keys():
            self._inputs_widgets[key].setText(str(self._settings[key]["value"]))
