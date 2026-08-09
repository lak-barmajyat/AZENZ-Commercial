import logging

from modules.reglements.nouveau_reglement.model import NouveauReglementModel


class NouveauReglementController:
    def __init__(self, view):
        self.view = view
        self.model = NouveauReglementModel()
        self.logger = logging.getLogger("app.reglements.nouveau_reglement")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
