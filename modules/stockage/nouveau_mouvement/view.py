from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget

from modules.stockage.nouveau_mouvement.controller import NouveauMouvementController


class NouveauMouvementView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/stockage/nouveau_mouvement/nouveau_mouvement.ui", self)

        self.setup()
        self.controller = NouveauMouvementController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Nouveau mouvement")
