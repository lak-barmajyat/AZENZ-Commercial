import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.ventes.nouveau_doc.view import NouveauDocumentView


def main():
    app = QApplication(sys.argv)
    view = NouveauDocumentView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
