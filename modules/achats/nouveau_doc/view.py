from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget

from modules.achats.nouveau_doc.controller import NouveauAchatDocumentController


class NouveauAchatDocumentView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/achats/nouveau_doc/nouveau_doc.ui", self)

        self.setup()
        self.controller = NouveauAchatDocumentController(self)

    def setup(self):
        self.setup_ui()

    def setup_ui(self):
        self.TitleLabel.setText("Nouveau document d'achat")
