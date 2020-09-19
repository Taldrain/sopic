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

        self.inputPassword = QLineEdit()
        self.inputPassword.setEchoMode(QLineEdit.Password)

        self.wrongPassword = QLabel("Wrong password")
        self.wrongPassword.hide()

        buttonOK = QPushButton("OK")
        buttonOK.clicked.connect(self.handleButtonOk)
        buttonOK.setDefault(True)

        buttonCancel = QPushButton("Cancel")
        buttonCancel.clicked.connect(self.handleButtonCancel)

        layout = QGridLayout(self)
        layout.addWidget(QLabel("Password:"), 0, 0)
        layout.addWidget(self.inputPassword, 1, 0)
        layout.addWidget(self.wrongPassword, 2, 0)
        layout.addWidget(buttonCancel, 3, 0)
        layout.addWidget(buttonOK, 3, 1)

        self.setLayout(layout)

        self.setWindowTitle("Admin password")

    def clean(self):
        self.wrongPassword.hide()
        self.inputPassword.setText("")

    def reject(self):
        self.clean()
        super().reject()

    def accept(self):
        self.clean()
        super().accept()

    def handleButtonOk(self):
        if self.inputPassword.text() == self.password:
            self.accept()
        else:
            self.inputPassword.clear()
            self.wrongPassword.show()

    def handleButtonCancel(self):
        self.reject()
