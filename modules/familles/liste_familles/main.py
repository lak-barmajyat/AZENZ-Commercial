import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.familles.liste_familles.view import ListeFamillesView


def main():
    app = QApplication(sys.argv)
    view = ListeFamillesView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
