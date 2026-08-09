import sys

import resources.resources_rc
from window_manger.window_manager import WindowManager
from services.logger.logger import setup_logger

from PyQt5.QtWidgets import QApplication


def get_qss():
    with open("theme/style/base.qss", "r") as f:
        return f.read()

def main():
    logger = setup_logger()
    logger.info("Application started")

    app = QApplication(sys.argv)

    qss = get_qss()
    app.setStyleSheet(qss)

    app.window_manager = WindowManager()
    app.window_manager.open("login")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
