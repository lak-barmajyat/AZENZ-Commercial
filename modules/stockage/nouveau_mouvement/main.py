import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.stockage.nouveau_mouvement.view import NouveauMouvementView


def main():
    app = QApplication(sys.argv)
    view = NouveauMouvementView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
