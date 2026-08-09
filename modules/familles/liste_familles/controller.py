import logging

from modules.familles.liste_familles.model import ListeFamillesModel


class ListeFamillesController:
    def __init__(self, view):
        self.view = view
        self.model = ListeFamillesModel()
        self.logger = logging.getLogger("app.familles.list")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
