from PyQt5.QtWidgets import QApplication
from resources import resources_rc
import sys

from modules.login.login_view import LoginView
from modules.table_de_bord.table_de_bord_view import DashboardMenuView, DashboardWidget


def get_qss():
    with open("theme/style/base.qss", 'r') as f:
        return f.read()

def main():

    qss = get_qss()
    app = QApplication(sys.argv)
    login_window = DashboardMenuView()
    app.setStyleSheet(qss)
    login_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
