import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / "resources").is_dir():
    ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import resources
import ui_utils.qss
from PyQt5.QtWidgets import QApplication

from modules.clients.liste_clients.view import ListeClientsView


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(ui_utils.qss.load_base_qss())
    view = ListeClientsView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
