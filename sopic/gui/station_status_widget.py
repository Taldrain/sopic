from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)

class StationStatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        self.init_widgets()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.nbPassed)
        hlayout.addWidget(self.nbFailed)
        hlayout.addWidget(self.consecutiveFailed)

        self.setLayout(hlayout)

    def formatDisplayStat(self, x, y):
        return "{}/{} ({:.0f}%)".format(x, y, (0 if y == 0 else x/y) * 100)

    def init_widgets(self):
        self.nbPassed = QLabel("Number of passed: " + self.formatDisplayStat(0, 0))
        self.nbFailed = QLabel("Number of failed: " + self.formatDisplayStat(0, 0))
        self.consecutiveFailed = QLabel("Consecutive fails: 0")

    def update(self, runObj):
        runFail = runObj['nb_failed']
        nbRun = runObj['nb_run']
        runPass = nbRun - runFail

        self.nbPassed.setText("Number of passed: " + self.formatDisplayStat(runPass, nbRun))
        self.nbFailed.setText("Number of failed: " + self.formatDisplayStat(runFail, nbRun))
        self.consecutiveFailed.setText("Consecutive fails: " + str(runObj['consecutive_failed']))
