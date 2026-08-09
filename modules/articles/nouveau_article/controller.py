import logging

from modules.articles.nouveau_article.model import NouveauArticleModel


class NouveauArticleController:
    def __init__(self, view):
        self.view = view
        self.model = NouveauArticleModel()
        self.logger = logging.getLogger("app.articles.nouveau_article")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
