from ui_utils.loader import load_ui as loadUi
from PyQt5.QtWidgets import QWidget

from modules.stockage.liste_stockage.controller import ListeStockageController


class ListeStockageView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/stockage/liste_stockage/liste_stockage.ui", self)

        self.setup()
        self.controller = ListeStockageController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Stockage")
