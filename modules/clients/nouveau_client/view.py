from ui_utils.loader import load_ui as loadUi
from PyQt5.QtWidgets import QWidget

from modules.clients.nouveau_client.controller import NouveauClientController


class NouveauClientView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/clients/nouveau_client/nouveau_client.ui", self)

        self.setup()
        self.controller = NouveauClientController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Nouveau client")
