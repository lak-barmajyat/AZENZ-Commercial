from PyQt5.QtWidgets import QApplication
from resources import resources_rc
import sys

from modules.login.login_view import LoginUI
from modules.table_de_bord.table_de_bord_ui import DashboardMenuUI, DashboardWidget
from services.logger.logger import setup_logger


def get_qss():
    with open("theme/style/base.qss", 'r') as f:
        return f.read()

def main():
    logger = setup_logger()
    logger.info("Application started")
    qss = get_qss()
    app = QApplication(sys.argv)
    login_window = LoginUI()
    
    app.setStyleSheet(qss)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
