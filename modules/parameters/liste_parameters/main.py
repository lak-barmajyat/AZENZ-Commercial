import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.parameters.liste_parameters.view import ListeParametersView


def main():
    app = QApplication(sys.argv)
    view = ListeParametersView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
