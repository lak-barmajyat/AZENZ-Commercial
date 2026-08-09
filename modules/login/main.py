import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.login.view import LoginView


def main():
    app = QApplication(sys.argv)

    view = LoginView()
    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()