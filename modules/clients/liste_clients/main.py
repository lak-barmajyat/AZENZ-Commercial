import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.clients.liste_clients.view import ListeClientsView


def main():
    app = QApplication(sys.argv)
    view = ListeClientsView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
