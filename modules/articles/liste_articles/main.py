import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.articles.liste_articles.view import ListeArticlesView


def main():
    app = QApplication(sys.argv)
    view = ListeArticlesView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
