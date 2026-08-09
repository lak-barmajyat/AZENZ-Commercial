import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.table_de_bord.widget.view import DashboardWidget


def main():
    app = QApplication(sys.argv)
    view = DashboardWidget()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
