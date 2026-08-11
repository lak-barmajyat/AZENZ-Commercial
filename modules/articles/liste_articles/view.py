from ui_utils.loader import load_ui as loadUi
from PyQt5.QtWidgets import QWidget

from modules.articles.liste_articles.controller import ListeArticlesController


class ListeArticlesView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/articles/liste_articles/liste_articles.ui", self)

        self.setup()
        self.controller = ListeArticlesController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Articles")
