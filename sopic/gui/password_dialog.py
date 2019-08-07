from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QPushButton,
    QLabel,
    QLineEdit,
)

class PasswordDialog(QDialog):
    def __init__(self, admin_password):
        super().__init__()

        self.password = admin_password

        self.init_gui()

    def init_gui(self):
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.wrong_password = QLabel("Wrong password")
        self.wrong_password.hide()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.slot_ok_button)
        ok_button.setDefault(True)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.slot_cancel_button)

        layout = QGridLayout(self)
        layout.addWidget(QLabel("Password:"), 0, 0)
        layout.addWidget(self.input_password, 1, 0)
        layout.addWidget(self.wrong_password, 2, 0)
        layout.addWidget(cancel_button, 3, 0)
        layout.addWidget(ok_button, 3, 1)

        self.setLayout(layout)

        self.setWindowTitle("Admin password")

    def clean(self):
        self.wrong_password.hide()
        self.input_password.setText("")

    def reject(self):
        self.clean()
        super().reject()

    def accept(self):
        self.clean()
        super().accept()

    def slot_ok_button(self):
        if (self.input_password.text() == self.password):
            self.accept()
        else:
            self.wrong_password.show()

    def slot_cancel_button(self):
        self.reject()
