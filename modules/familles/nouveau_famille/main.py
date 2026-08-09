import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.familles.nouveau_famille.view import NouveauFamilleView


def main():
    app = QApplication(sys.argv)
    view = NouveauFamilleView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
