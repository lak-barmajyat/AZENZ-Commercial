import logging

from modules.clients.liste_clients.model import ListeClientsModel


class ListeClientsController:
    def __init__(self, view):
        self.view = view
        self.model = ListeClientsModel()
        self.logger = logging.getLogger("app.clients.list")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
