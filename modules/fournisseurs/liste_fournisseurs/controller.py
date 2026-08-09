import logging

from modules.fournisseurs.liste_fournisseurs.model import ListeFournisseursModel


class ListeFournisseursController:
    def __init__(self, view):
        self.view = view
        self.model = ListeFournisseursModel()
        self.logger = logging.getLogger("app.fournisseurs.list")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
