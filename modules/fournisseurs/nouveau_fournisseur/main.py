import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.fournisseurs.nouveau_fournisseur.view import NouveauFournisseurView


def main():
    app = QApplication(sys.argv)
    view = NouveauFournisseurView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
