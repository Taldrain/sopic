from PyQt5.QtWidgets import QTabWidget, QWidget

from .step_ui_widget import StepUI

class TabManagerWidget(QTabWidget):
    def __init__(self, station, parent=None):
        super().__init__(parent)
        self.station = station
        self.init_gui()

    def init_gui(self):
        for step in self.station.getSteps():
            self.addTab(step.getWidget(), step.getStepName())

        for i, val in enumerate(self.station.getSteps()):
            self.setTabEnabled(i, False)

        self.tabBar().setVisible(False)
        self.update_current_tab()

    def update_current_tab(self):
        new_index = self.station.getCurrentStep()
        self.setTabEnabled(self.currentIndex(), False)
        self.setTabEnabled(new_index, True)
        self.setCurrentIndex(new_index)
