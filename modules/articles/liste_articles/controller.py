import logging

from modules.articles.liste_articles.model import ListeArticlesModel


class ListeArticlesController:
    def __init__(self, view):
        self.view = view
        self.model = ListeArticlesModel()
        self.logger = logging.getLogger("app.articles.list")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
