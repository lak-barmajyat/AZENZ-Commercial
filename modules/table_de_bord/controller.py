from PyQt5.QtWidgets import QApplication

class DashboardController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.setup()

    def logout(self):
        app = QApplication.instance()
        if app is None:
            return

        app.window_manager.open("login")
        app.window_manager.hide("table_de_bord.menu")

        login_view = app.window_manager.get_instance("login")
        if login_view is not None:
            login_view.PasswordEntry.clear()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        self.view.LogoutButton.clicked.connect(self.logout)