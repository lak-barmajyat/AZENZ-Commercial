import logging

from modules.fournisseurs.nouveau_fournisseur.model import NouveauFournisseurModel


class NouveauFournisseurController:
    def __init__(self, view):
        self.view = view
        self.model = NouveauFournisseurModel()
        self.logger = logging.getLogger("app.fournisseurs.nouveau_fournisseur")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
