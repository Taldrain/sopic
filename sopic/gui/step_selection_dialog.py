from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QPushButton,
    QLabel,
    QCheckBox
)

class StepSelectionDialog(QDialog):
    def __init__(self, steps):
        super().__init__()

        self.steps = steps

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.slot_ok_button)

        self.layout = QGridLayout(self)
        self.layout.addWidget(ok_button, 99, 1)

        self.allStepsActivated = True
        self.checkboxes = []

        self.init_gui()

        self.setLayout(self.layout)
        self.setWindowTitle("Step selection")


    def init_gui(self):
        checkbox = QCheckBox()
        checkbox.setChecked(self.allStepsActivated)
        checkbox.stateChanged.connect(self.controlAllSteps)
        self.layout.addWidget(QLabel('All steps'), 0, 0)
        self.layout.addWidget(checkbox, 0, 1)

        # skip the first and last element (nfc)
        for index, step in enumerate(self.steps[1:-1]):
            # keep index 0 for the 'All steps' checkbox
            index += 1
            checkbox = QCheckBox()
            checkbox.setChecked(step.ACTIVATED)
            checkbox.stateChanged.connect(self.slot_checkbox(step))
            self.layout.addWidget(QLabel(step.STEP_NAME), index, 0)
            self.layout.addWidget(checkbox, index, 1)
            self.checkboxes.append(checkbox)

    def controlAllSteps(self):
        self.allStepsActivated = not self.allStepsActivated

        for checkbox in self.checkboxes:
            checkbox.setChecked(self.allStepsActivated)


    def slot_checkbox(self, step):
        def _slot_checkbox(state):
            step.ACTIVATED = state

        return _slot_checkbox

    def slot_ok_button(self):
        super().accept()

