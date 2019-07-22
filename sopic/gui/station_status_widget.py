from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)

class StationStatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.avgTime = 0

        self.init_gui()

    def init_gui(self):
        self.init_widgets()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.nbPassed)
        hlayout.addWidget(self.nbFailed)
        hlayout.addWidget(self.consecutiveFailed)
        hlayout.addWidget(self.stepTimer)
        hlayout.addWidget(self.stationTime)

        self.setLayout(hlayout)

    def formatDisplayStat(self, x, y):
        return "{}/{} ({:.0f}%)".format(x, y, (0 if y == 0 else x/y) * 100)

    def init_widgets(self):
        self.nbPassed = QLabel("Number of passed: " + self.formatDisplayStat(0, 0))
        self.nbFailed = QLabel("Number of failed: " + self.formatDisplayStat(0, 0))
        self.consecutiveFailed = QLabel("Consecutive fails: 0")
        self.stepTimer = QLabel("Previous run: {}s (avg: {}s)".format(0, 0))
        self.stationTime = QLabel("Date: {}".format(datetime.date.today.isoformat()))

    def update(self, runObj):
        runFail = runObj['nb_failed']
        nbRun = runObj['nb_run']
        runPass = nbRun - runFail
        timeSpent = (datetime.datetime.utc() - runObj['startDate']).seconds
        if (nbRun > 0):
            self.avgTime = (self.avgTime * (nbRun - 1) / nbRun) + timeSpent / nbRun

        self.nbPassed.setText("Number of passed: " + self.formatDisplayStat(runPass, nbRun))
        self.nbFailed.setText("Number of failed: " + self.formatDisplayStat(runFail, nbRun))
        self.consecutiveFailed.setText("Consecutive fails: " + str(runObj['consecutive_failed']))
        self.stepTimer = QLabel("Previous run: {}s (avg: {}s)".format(timeSpent, self.avgTime))
