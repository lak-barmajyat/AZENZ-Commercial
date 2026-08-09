from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget

from modules.parameters.liste_parameters.controller import ListeParametersController


class ListeParametersView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/parameters/liste_parameters/liste_parameters.ui", self)

        self.setup()
        self.controller = ListeParametersController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Paramètres")
