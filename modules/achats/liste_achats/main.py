import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.achats.liste_achats.view import AchatsView


def main():
    app = QApplication(sys.argv)
    view = AchatsView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
