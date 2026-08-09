import logging

from modules.stockage.liste_stockage.model import ListeStockageModel


class ListeStockageController:
    def __init__(self, view):
        self.view = view
        self.model = ListeStockageModel()
        self.logger = logging.getLogger("app.stockage.list")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
