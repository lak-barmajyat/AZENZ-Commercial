import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.achats.nouveau_doc.view import NouveauAchatDocumentView


def main():
    app = QApplication(sys.argv)
    view = NouveauAchatDocumentView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
