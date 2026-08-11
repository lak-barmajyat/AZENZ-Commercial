import sys

import resources
from ui_utils.qss import load_base_qss
from window_manger.window_manager import WindowManager
from services.logger.logger import setup_logger

from PyQt5.QtWidgets import QApplication


def main():
    logger = setup_logger()
    logger.info("Application started")

    app = QApplication(sys.argv)

    app.setStyleSheet(load_base_qss())

    app.window_manager = WindowManager()
    app.window_manager.open("login")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
