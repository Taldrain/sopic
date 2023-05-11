from PySide6.QtWidgets import QTabWidget


class StepsViewerWidget(QTabWidget):
    def __init__(self, steps):
        super().__init__()

        self.tabBar().setVisible(False)

        for step in steps:
            self.addTab(step.getWidget(), step.STEP_NAME)

    def update_tab(self, step):
        self.setCurrentWidget(step.getWidget())
