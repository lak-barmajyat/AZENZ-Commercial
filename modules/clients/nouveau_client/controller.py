import logging

from modules.clients.nouveau_client.model import NouveauClientModel


class NouveauClientController:
    def __init__(self, view):
        self.view = view
        self.model = NouveauClientModel()
        self.logger = logging.getLogger("app.clients.nouveau_client")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
