from ui_utils.loader import load_ui as loadUi
from PyQt5.QtWidgets import QWidget

from modules.fournisseurs.liste_fournisseurs.controller import ListeFournisseursController


class ListeFournisseursView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/fournisseurs/liste_fournisseurs/liste_fournisseurs.ui", self)

        self.setup()
        self.controller = ListeFournisseursController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Fournisseurs")
