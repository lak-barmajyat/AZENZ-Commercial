import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

from modules.login.model import LoginModel


class LoginController:
    def __init__(self, view):
        self.view = view
        self.model = LoginModel()
        self.logger = logging.getLogger("app.login")

        self.setup()

    def setup(self):
        self.fill_societes()
        self.connect_signals()

        if self.view.DatabaseComboBox.count():
            self.check_database_connection(
                self.view.DatabaseComboBox.currentText()
            )
        else:
            self.view.show_error("     Aucune société active")
            self.view.set_login_enabled(False)

    def connect_signals(self):
        self.view.DatabaseComboBox.currentTextChanged.connect(
            self.check_database_connection
        )
        self.view.LoginButton.clicked.connect(self.handle_login)
        self.view.CancelButton.clicked.connect(self.view.close)

        self.view.UsernameLineEdit.returnPressed.connect(
            self.view.PasswordLineEdit.setFocus
        )
        self.view.PasswordLineEdit.returnPressed.connect(
            self.view.LoginButton.click
        )
        self.view.TogglePasswordAction.triggered.connect(
            self.view.toggle_password_visibility
        )

    def fill_societes(self):
        self.view.DatabaseComboBox.clear()
        self.view.DatabaseComboBox.addItems(self.model.get_societes())

    def check_database_connection(self, code_societe):
        if not code_societe:
            return

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        try:
            if self.model.check_database_connection(code_societe):
                self.view.hide_error()
                self.view.set_login_enabled(True)
                self.logger.info(
                    "Connected to database for société %s",
                    code_societe,
                )
            else:
                self.view.show_error("     Échec de la connexion")
                self.view.set_login_enabled(False)
                self.logger.error(
                    "Failed to connect to database for société %s",
                    code_societe,
                )
        finally:
            QApplication.restoreOverrideCursor()

    def handle_login(self):
        username = self.view.UsernameLineEdit.text().strip()
        password = self.view.PasswordLineEdit.text()

        if not self.model.authenticate_user(username, password):
            self.view.show_error(
                "     Nom d'utilisateur ou mot de passe incorrect"
            )
            self.logger.warning("Login failed for user %s", username)
            return

        self.view.hide_error()
        self.logger.info("User %s logged in successfully", username)

        app = QApplication.instance()
        if app is not None and hasattr(app, "window_manager"):
            app.window_manager.open("table_de_bord.menu")
            app.window_manager.open("table_de_bord.widget")
            app.window_manager.hide("login")