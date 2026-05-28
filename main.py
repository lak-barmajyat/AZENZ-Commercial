from PyQt5.QtWidgets import QApplication
import resources_rc
import sys

from ui.screens.login.login_ui import LoginUI
from ui.screens.dashboard.dashboard_ui import DashboardMenuUI, DashboardWidget


def get_qss():
    with open("ui/styles/style.qss", 'r') as f:
        return f.read()

def main():

    qss = get_qss()
    app = QApplication(sys.argv)
    login_window = LoginUI()
    app.setStyleSheet(qss)
    login_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
