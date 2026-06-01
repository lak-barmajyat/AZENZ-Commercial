from PyQt5.QtWidgets import QApplication

class DashboardController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.app = QApplication.instance()

        self.setup()

    def logout(self):
        self.app.DashboardMenuView.close()
        self.app.LoginView.show()
        # self.app.LoginView.UsernameEntry.clear()
        self.app.LoginView.PasswordEntry.clear()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        self.view.LogoutButton.clicked.connect(self.logout)