from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget

from modules.familles.liste_familles.controller import ListeFamillesController


class ListeFamillesView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/familles/liste_familles/liste_familles.ui", self)

        self.setup()
        self.controller = ListeFamillesController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Familles")
