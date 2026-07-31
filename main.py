from PyQt5.QtWidgets import QApplication
from resources import resources_rc
import sys, os

from modules.login.login_view import LoginView
from modules.table_de_bord.table_de_bord_view import DashboardMenuView, DashboardWidget
from services.logger.logger import setup_logger


def get_qss():
    with open("theme/style/base.qss", "r") as f:
        return f.read()


def main():
    logger = setup_logger()
    logger.info("Application started")
    qss = get_qss()
    app = QApplication(sys.argv)
    app.LoginView = LoginView()
    # app.LoginView = LoginView()
    app.setStyleSheet(qss)

    # os.environ["DB_HOST"] = "localhost"
    # os.environ["DB_PORT"] = "3306"
    # os.environ["DB_NAME"] = "azenz_commercial"
    # os.environ["DB_USER"] = "root"
    # os.environ["DB_PASSWORD"] = "0x5c86a761143cc92c93ee82160645399a"
    # os.environ["DB_CHARSET"] = "utf8mb4"
    # os.environ["DB_COLLATION"] = "utf8mb4_general_ci"
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
