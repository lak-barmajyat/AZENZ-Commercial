import logging

from modules.achats.liste_achats.model import AchatsModel


class AchatsController:
    def __init__(self, view):
        self.view = view
        self.model = AchatsModel()
        self.logger = logging.getLogger("app.achats.list")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
