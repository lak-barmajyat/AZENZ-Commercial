import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.clients.nouveau_client.view import NouveauClientView


def main():
    app = QApplication(sys.argv)
    view = NouveauClientView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
