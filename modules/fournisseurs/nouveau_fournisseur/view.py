from ui_utils.loader import load_ui as loadUi
from PyQt5.QtWidgets import QWidget

from modules.fournisseurs.nouveau_fournisseur.controller import NouveauFournisseurController


class NouveauFournisseurView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/fournisseurs/nouveau_fournisseur/nouveau_fournisseur.ui", self)

        self.setup()
        self.controller = NouveauFournisseurController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Nouveau fournisseur")
