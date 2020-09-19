from PyQt5.QtWidgets import QTabWidget


class TabManagerWidget(QTabWidget):
    def __init__(self, station, parent=None):
        super().__init__(parent)

        self.station = station
        for step in self.station.getSteps():
            self.addTab(step.getWidget(), step.getStepName())

        if self.station.startStep is not None:
            self.addTab(
                self.station.startStep.getWidget(), self.station.startStep.getStepName()
            )

        if self.station.endStep is not None:
            self.addTab(
                self.station.endStep.getWidget(), self.station.endStep.getStepName()
            )

        for i in range(len(self.station.getSteps())):
            self.setTabEnabled(i, False)

        self.tabBar().setVisible(False)
        self.updateCurrentTab()

    def updateCurrentTab(self):
        self.switchToTabIndex(self.station.getCurrentStep())

    def switchToTabIndex(self, index):
        self.setTabEnabled(self.currentIndex(), False)
        self.setTabEnabled(index, True)
        self.setCurrentIndex(index)
