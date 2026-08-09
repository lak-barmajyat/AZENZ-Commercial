import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.reglements.liste_reglements.view import ReglementsView


def main():
    app = QApplication(sys.argv)
    view = ReglementsView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
