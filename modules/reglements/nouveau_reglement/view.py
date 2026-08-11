from ui_utils.loader import load_ui as loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

from ui_utils.widgets.erp_data_table import ERPTableColumn

from modules.reglements.nouveau_reglement.controller import (
    NouveauReglementController,
)


class NouveauReglementView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/reglements/nouveau_reglement/nouveau_reglement.ui", self)

        self.setup()
        self.controller = NouveauReglementController(self)

    def setup(self):
        self.setup_documents_table()
        self.setup_navigation()

    def setup_navigation(self):
        self.RetourButton.clicked.connect(self.go_back)

    def go_back(self):
        app = QApplication.instance()
        if app is None or not hasattr(app, "window_manager"):
            return
        app.window_manager.open("reglements.list")

    def setup_documents_table(self):
        columns = [
            ERPTableColumn("numero_document", "N° DOCUMENT", width=150, is_link=True),
            ERPTableColumn("date", "DATE", width=110, is_date=True),
            ERPTableColumn("total_ttc", "TOTAL TTC", width=130, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("deja_regle", "DÉJÀ RÉGLÉ", width=130, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("reste", "RESTE", width=130, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("montant_affecte", "MONTANT AFFECTÉ", width=160, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("statut", "STATUT", width=130, align=Qt.AlignCenter, is_status=True),
        ]
        self.DocumentsTable.set_columns(columns)
