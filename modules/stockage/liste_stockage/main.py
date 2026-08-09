import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.stockage.liste_stockage.view import ListeStockageView


def main():
    app = QApplication(sys.argv)
    view = ListeStockageView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
