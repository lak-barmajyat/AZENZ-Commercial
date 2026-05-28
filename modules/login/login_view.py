from ui_utils.effects import set_drop_shadow
from ui_utils.canvas import create_uniform_icon

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QAction, QMainWindow,
    QLineEdit)


class LoginUI(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("modules/login/login.ui", self)

        self.is_password_hidden = True
        self._drag_origin = None

        self.DatabaseCombobox.addItems(["Production", "Testing"])
        self.setup()

    def setup(self):
        self.setup_window()
        self.setup_widgets()
        self.setup_icons()
        self.setup_connections()
        self.hide_error()

    # ------------------------ Setup Functions ----------------------- #
    def setup_window(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("LAK ERP - Login")
        self.setWindowIcon(QIcon(":/icons/resources/icons/app_icon.svg"))

    def setup_widgets(self):
        # set widget properties for styling
        self.LoginButton.setProperty("class", "primary")
        self.CancelButton.setProperty("class", "outlined")
        self.UsernameEntry.setProperty("class", "icon-lineedit")
        self.PasswordEntry.setProperty("class", "icon-lineedit")

        # Apply drop shadows
        set_drop_shadow(self.LoginFrame, 70, 15, 20, 100)
        set_drop_shadow(self.UsernameEntry, 25, 0, 7, 50)
        set_drop_shadow(self.PasswordEntry, 25, 0, 7, 50)

        self.UsernameEntry.setFocus(True)
        self.UsernameEntry.returnPressed.connect(self.PasswordEntry.setFocus)
        self.PasswordEntry.returnPressed.connect(self.LoginButton.click)

    def setup_icons(self):
        # For Username Field
        username_icon = QAction(self)
        username_icon.setIcon(create_uniform_icon(":/icons/resources/icons/user.svg"))
        self.UsernameEntry.addAction(username_icon, QLineEdit.LeadingPosition)

        # For Password Field
        password_icon = QAction(self)
        password_icon.setIcon(create_uniform_icon(":/icons/resources/icons/lock.svg"))
        self.PasswordEntry.addAction(password_icon, QLineEdit.LeadingPosition)

        self.toggle_password_action = QAction(self)
        self.toggle_password_action.setIcon(QIcon(f":/icons/resources/icons/eye-closed.svg"))
        self.PasswordEntry.addAction(self.toggle_password_action, QLineEdit.TrailingPosition)

    def setup_connections(self):
        self.toggle_password_action.triggered.connect(self.toggle_password_visibility)

    # ------------------------ Slot Functions ----------------------- #
    def toggle_password_visibility(self):
        self.is_password_hidden = not self.is_password_hidden
        if self.is_password_hidden:
            self.PasswordEntry.setEchoMode(QLineEdit.Password)
            self.toggle_password_action.setIcon(QIcon(f":/icons/resources/icons/eye-closed.svg"))
        else:
            self.PasswordEntry.setEchoMode(QLineEdit.Normal)
            self.toggle_password_action.setIcon(QIcon(f":/icons/resources/icons/eye-open.svg"))

    def hide_error(self):
        self.LoginErrorLabel.hide()

    # ------------------------ Window Drag ----------------------- #
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


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    login_window = LoginUI()
    login_window.show()
    sys.exit(app.exec_())
