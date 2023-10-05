from PySide6.QtWidgets import QTabWidget


class StepsViewerWidget(QTabWidget):
    def __init__(self, steps):
        super().__init__()

        self.tabBar().setVisible(True)

        for index, step in enumerate(steps):
            self.addTab(step.getWidget(), step.STEP_NAME)
            self.tabBar().setTabEnabled(index, False)

    def update_tab(self, step):
        self.setCurrentWidget(step.getWidget())
