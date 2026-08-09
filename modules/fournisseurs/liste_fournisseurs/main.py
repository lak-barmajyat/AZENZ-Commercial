import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.fournisseurs.liste_fournisseurs.view import ListeFournisseursView


def main():
    app = QApplication(sys.argv)
    view = ListeFournisseursView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
