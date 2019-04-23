from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QPushButton
)

class MainSettingsDialog(QDialog):
    def __init__(self, station, callbackUpdateSettings, callbackUpdateFile, callbackResetSettings):
        super().__init__()

        self.station = station
        self.widgets = []

        self.settings = station.settings
        self.cbUpdateSettings = callbackUpdateSettings
        self.cbUpdateFile = callbackUpdateFile
        self.cbResetSettings = callbackResetSettings

        reset_button = QPushButton('Reset')
        reset_button.clicked.connect(self.slot_reset_button)

        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.slot_ok_button)

        self.layout = QGridLayout(self)
        self.layout.addWidget(ok_button, 99, 1)
        self.layout.addWidget(reset_button, 99, 0)

        # From child class
        self.init_gui()
        self.init_values()

        for index, value in enumerate(self.widgets):
            self.layout.addWidget(value[0], index, 0)
            self.layout.addWidget(value[1], index, 1)

        self.set_layout()

    def slot_ok_button(self):
        self.cbUpdateFile()
        super().accept()

    def slot_reset_button(self):
        self.cbResetSettings()
        self.settings = self.station.settings
        self.init_values()
        super().accept()

    def set_layout(self):
        self.setLayout(self.layout)
        self.setWindowTitle('Settings')
