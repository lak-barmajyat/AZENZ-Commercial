import logging

from PyQt5.QtWidgets import QApplication

from modules.table_de_bord.menu.model import DashboardMenuModel


class DashboardMenuController:
    def __init__(self, view):
        self.view = view
        self.model = DashboardMenuModel()
        self.logger = logging.getLogger("app.table_de_bord.menu")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        self.view.LogoutButton.clicked.connect(self.logout)

    def logout(self):
        app = QApplication.instance()
        if app is None:
            return

        app.window_manager.open("login")
        app.window_manager.hide("table_de_bord.menu")

        login_view = app.window_manager.get_instance("login")
        if login_view is not None:
            login_view.PasswordLineEdit.clear()

        self.logger.info("User logged out")
