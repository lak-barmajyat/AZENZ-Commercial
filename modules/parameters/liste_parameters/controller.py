import logging

from modules.parameters.liste_parameters.model import ListeParametersModel


class ListeParametersController:
    def __init__(self, view):
        self.view = view
        self.model = ListeParametersModel()
        self.logger = logging.getLogger("app.parameters.list")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
