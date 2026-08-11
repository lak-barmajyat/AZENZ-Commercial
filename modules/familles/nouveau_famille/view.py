from ui_utils.loader import load_ui as loadUi
from PyQt5.QtWidgets import QWidget

from modules.familles.nouveau_famille.controller import NouveauFamilleController


class NouveauFamilleView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/familles/nouveau_famille/nouveau_famille.ui", self)

        self.setup()
        self.controller = NouveauFamilleController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Nouvelle famille")
