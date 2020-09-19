from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton


class MainSettingsDialog(QDialog):
    def __init__(
        self, station, callbackUpdateSettings, callbackUpdateFile, callbackResetSettings
    ):
        super().__init__()

        self.station = station
        self.widgets = []

        self.settings = station.settings
        self.cbUpdateSettings = callbackUpdateSettings
        self.cbUpdateFile = callbackUpdateFile
        self.cbResetSettings = callbackResetSettings

        resetButton = QPushButton("Reset")
        resetButton.clicked.connect(self.handleReset)

        buttonOK = QPushButton("OK")
        buttonOK.clicked.connect(self.handleOK)

        self.layout = QGridLayout(self)
        self.layout.addWidget(buttonOK, 99, 1)
        self.layout.addWidget(resetButton, 99, 0)

        # From child class
        self.initUI()
        self.initValues()

        for index, value in enumerate(self.widgets):
            self.layout.addWidget(value[0], index, 0)
            self.layout.addWidget(value[1], index, 1)

        self.setLayout(self.layout)
        self.setWindowTitle("Settings")

    def handleOK(self):
        self.cbUpdateFile()
        super().accept()

    def handleReset(self):
        self.cbResetSettings()
        self.settings = self.station.settings
        self.initValues()
        super().accept()
