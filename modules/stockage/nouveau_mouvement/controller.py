import logging

from modules.stockage.nouveau_mouvement.model import NouveauMouvementModel


class NouveauMouvementController:
    def __init__(self, view):
        self.view = view
        self.model = NouveauMouvementModel()
        self.logger = logging.getLogger("app.stockage.nouveau_mouvement")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
