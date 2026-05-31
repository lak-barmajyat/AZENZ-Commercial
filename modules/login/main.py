from modules.login.login_view import LoginUI
from PyQt5.QtWidgets import QApplication
from modules.login.controller import LoginController
from modules.login.model import LoginModel
import os

if __name__ == "__main__":
    app = QApplication([])
    controller = LoginController()
    view = LoginUI()
    model = LoginModel()
    controller = LoginController(model, view)
    app.exec_()