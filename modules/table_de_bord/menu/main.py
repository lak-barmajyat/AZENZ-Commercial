import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.table_de_bord.menu.view import DashboardMenuView


def main():
    app = QApplication(sys.argv)
    view = DashboardMenuView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
