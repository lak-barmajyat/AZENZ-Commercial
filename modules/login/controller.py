from modules.login.model import LoginModel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from modules.table_de_bord.table_de_bord_ui import DashboardWidget
# from modules.login.login_view import LoginUI

class LoginController:
    def __init__(self, model: LoginModel, view):
        self.model = model
        self.view = view

        self.setup()
        self.connect_signals()

    
    def check_database_connection(self, code_societe):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        if not self.model.check_database_connection(code_societe):
            self.view.LoginErrorLabel.setText("     Échec de la connexion")
            self.view.LoginErrorLabel.show()
            self.view.UsernameEntry.setEnabled(False)
            self.view.PasswordEntry.setEnabled(False)
        else:
            self.view.LoginErrorLabel.hide()
            self.view.UsernameEntry.setEnabled(True)
            self.view.PasswordEntry.setEnabled(True)
        QApplication.restoreOverrideCursor()

    def handle_login(self):
        username = self.view.UsernameEntry.text()
        password = self.view.PasswordEntry.text()
        
        if not self.model.authenticate_user(username, password):
            self.view.LoginErrorLabel.setText("     Nom d'utilisateur ou mot de passe incorrect")
            self.view.LoginErrorLabel.show()
        else:
            self.view.LoginErrorLabel.hide()
            QApplication.DashboardWidget = DashboardWidget()
            QApplication.DashboardWidget.show()
            self.view.close()
    
    def connect_signals(self):
        self.view.DatabaseCombobox.currentIndexChanged.connect(
            lambda _: self.check_database_connection(self.view.DatabaseCombobox.currentText())
            )
        self.view.LoginButton.clicked.connect(self.handle_login)
        self.view.CancelButton.clicked.connect(self.view.close)

    def setup(self):
        self.view.DatabaseCombobox.addItems(self.model.get_societes())
        self.check_database_connection(self.view.DatabaseCombobox.currentText())
