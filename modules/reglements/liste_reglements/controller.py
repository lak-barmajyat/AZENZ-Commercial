import logging

from modules.reglements.liste_reglements.model import ReglementsModel


class ReglementsController:
    def __init__(self, view):
        self.view = view
        self.model = ReglementsModel()
        self.logger = logging.getLogger("app.reglements.list")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
