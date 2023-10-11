from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QCheckBox,
    QComboBox,
)
from PySide6.QtGui import QIntValidator


def common_line_edit_widget(key, settings):
    label = QLabel(settings["label"] if "label" in settings else key)
    input = QLineEdit()
    input.setText(str(settings["value"]))

    def set_value(value):
        input.setText(str(value))

    set_value(settings["value"])
    input.setReadOnly(settings["edit"] is False if "edit" in settings else False)
    return (label, input, set_value)


def string_widget(key, settings, on_change):
    label, input, set_value = common_line_edit_widget(key, settings)
    input.textEdited.connect(lambda: on_change(key, input.text()))
    return (label, input, set_value)


def number_widget(key, settings, on_change):
    label, input, set_value = common_line_edit_widget(key, settings)
    input.setValidator(QIntValidator())
    input.textEdited.connect(lambda: on_change(key, int(input.text())))
    return (label, input, set_value)


def bool_widget(key, settings, on_change):
    label = QLabel(settings["label"] if "label" in settings else key)
    input = QCheckBox()
    input.setChecked(settings["value"])

    def set_value(value):
        input.setChecked(value)

    set_value(settings["value"])
    input.stateChanged.connect(lambda: on_change(key, input.isChecked()))
    return (label, input, set_value)


def combobox_widget(key, settings, on_change):
    label = QLabel(settings["label"] if "label" in settings else key)
    input = QComboBox()
    input.addItems(settings["values"])

    def set_value(value):
        input.setCurrentText(value)

    set_value(settings["value"])
    input.currentTextChanged.connect(lambda: on_change(key, input.currentText()))
    return (label, input, set_value)
