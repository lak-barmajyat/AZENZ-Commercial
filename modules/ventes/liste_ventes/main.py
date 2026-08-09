import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.ventes.liste_ventes.view import VentesView


def main():
    app = QApplication(sys.argv)
    view = VentesView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
