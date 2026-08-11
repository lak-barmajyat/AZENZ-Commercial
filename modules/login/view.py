from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QLineEdit, QMainWindow
from ui_utils.loader import load_ui as loadUi

from modules.login.controller import LoginController
from ui_utils.canvas import create_uniform_icon
from ui_utils.effects import set_drop_shadow


class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("modules/login/login.ui", self)

        self.is_password_hidden = True
        self._drag_pos = None

        self.setup()
        self.controller = LoginController(self)

    def setup(self):
        self.setup_window()
        self.setup_widgets()
        self.setup_icons()
        self.hide_error()

    # ------------------------ Setup Functions ----------------------- #
    def setup_window(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("AZENZ - Login")
        self.setWindowIcon(QIcon(":/images/images/program_logo.png"))

    def setup_widgets(self):
        self.LoginButton.setProperty("class", "primary")
        self.CancelButton.setProperty("class", "outlined")
        self.UsernameLineEdit.setProperty("class", "icon-lineedit")
        self.PasswordLineEdit.setProperty("class", "icon-lineedit")

        set_drop_shadow(self.LoginFrame, 70, 15, 20, 100)
        set_drop_shadow(self.UsernameLineEdit, 25, 0, 7, 50)
        set_drop_shadow(self.PasswordLineEdit, 25, 0, 7, 50)

        self.UsernameLineEdit.setFocus()

    def setup_icons(self):
        username_action = QAction(self)
        username_action.setIcon(create_uniform_icon(":/icons/icons/user.svg"))
        self.UsernameLineEdit.addAction(username_action, QLineEdit.LeadingPosition)

        password_action = QAction(self)
        password_action.setIcon(create_uniform_icon(":/icons/icons/lock.svg"))
        self.PasswordLineEdit.addAction(password_action, QLineEdit.LeadingPosition)

        self.TogglePasswordAction = QAction(self)
        self.TogglePasswordAction.setIcon(QIcon(":/icons/icons/eye-closed.svg"))
        self.PasswordLineEdit.addAction(
            self.TogglePasswordAction,
            QLineEdit.TrailingPosition,
        )

    # ------------------------ View Functions ----------------------- #
    def toggle_password_visibility(self):
        self.is_password_hidden = not self.is_password_hidden

        if self.is_password_hidden:
            self.PasswordLineEdit.setEchoMode(QLineEdit.Password)
            icon_path = ":/icons/icons/eye-closed.svg"
        else:
            self.PasswordLineEdit.setEchoMode(QLineEdit.Normal)
            icon_path = ":/icons/icons/eye-open.svg"

        self.TogglePasswordAction.setIcon(QIcon(icon_path))

    def show_error(self, message):
        self.LoginErrorLabel.setText(message)
        self.LoginErrorLabel.show()

    def hide_error(self):
        self.LoginErrorLabel.hide()

    def set_login_enabled(self, enabled):
        self.UsernameLineEdit.setEnabled(enabled)
        self.PasswordLineEdit.setEnabled(enabled)
        self.LoginButton.setEnabled(enabled)

    # ------------------------ Window Events ----------------------- #
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self._drag_pos is not None:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            return

        super().keyPressEvent(event)