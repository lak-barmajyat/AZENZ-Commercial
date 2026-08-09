from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget

from modules.articles.nouveau_article.controller import NouveauArticleController


class NouveauArticleView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/articles/nouveau_article/nouveau_article.ui", self)

        self.setup()
        self.controller = NouveauArticleController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Nouvel article")
