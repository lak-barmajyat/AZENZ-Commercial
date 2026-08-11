from ui_utils.loader import load_ui as loadUi
from PyQt5.QtWidgets import QWidget

from modules.clients.liste_clients.controller import ListeClientsController


class ListeClientsView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/clients/liste_clients/liste_clients.ui", self)

        self.setup()
        self.controller = ListeClientsController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Clients")
