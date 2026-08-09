import logging

from modules.familles.nouveau_famille.model import NouveauFamilleModel


class NouveauFamilleController:
    def __init__(self, view):
        self.view = view
        self.model = NouveauFamilleModel()
        self.logger = logging.getLogger("app.familles.nouveau_famille")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
