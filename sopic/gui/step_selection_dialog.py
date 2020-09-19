from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton, QLabel, QCheckBox


def handleClick(step):
    def _handleClick(state):
        # from qt doc:
        # 0: unchecked
        # 1: partially checked
        # 2: checked
        step.ACTIVATED = state == 2

    return _handleClick


class StepSelectionDialog(QDialog):
    def __init__(self, steps):
        super().__init__()

        self.steps = steps

        buttonOK = QPushButton("OK")
        buttonOK.clicked.connect(self.handleValidate)

        layout = QGridLayout(self)
        layout.addWidget(buttonOK, 99, 1)

        self.allStepsActivated = True
        self.checkboxes = []

        checkbox = QCheckBox()
        checkbox.setChecked(self.allStepsActivated)
        checkbox.stateChanged.connect(self.controlAllSteps)
        layout.addWidget(QLabel("All steps"), 0, 0)
        layout.addWidget(checkbox, 0, 1)

        for index, step in enumerate(self.steps):
            # keep index 0 for the 'All steps' checkbox
            index += 1
            checkbox = QCheckBox()
            checkbox.setChecked(step.ACTIVATED)
            checkbox.stateChanged.connect(handleClick(step))
            layout.addWidget(QLabel(step.STEP_NAME), index, 0)
            layout.addWidget(checkbox, index, 1)
            self.checkboxes.append(checkbox)

        self.setLayout(layout)
        self.setWindowTitle("Step selection")

    def controlAllSteps(self):
        self.allStepsActivated = not self.allStepsActivated

        for checkbox in self.checkboxes:
            checkbox.setChecked(self.allStepsActivated)

    def handleValidate(self):
        super().accept()
