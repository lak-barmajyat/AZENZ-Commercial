import sys

import resources.resources_rc
from PyQt5.QtWidgets import QApplication

from modules.articles.nouveau_article.view import NouveauArticleView


def main():
    app = QApplication(sys.argv)
    view = NouveauArticleView()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
