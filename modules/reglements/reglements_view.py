from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from ui_utils.widgets.erp_data_table import ERPTableColumn


class ReglementsView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/reglements/reglements.ui", self)
        self.setup_table()

    def setup_table(self):
        columns = [
            ERPTableColumn("id", "ID", width=80, visible=False),
            ERPTableColumn("numero_reglement", "N° RÈGLEMENT", width=150, is_link=True),
            ERPTableColumn("date", "DATE", width=110, is_date=True),
            ERPTableColumn("client", "CLIENT", width=300, stretch=True),
            ERPTableColumn("mode", "MODE", width=130),
            ERPTableColumn("reference", "RÉFÉRENCE", width=160),
            ERPTableColumn("montant", "MONTANT", width=130, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("solde", "RESTE À RÉGLER", width=150, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("statut", "STATUT", width=130, align=Qt.AlignCenter, is_status=True),
        ]
        self.ReglementsTable.set_columns(columns)


class NouveauReglementView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/reglements/nouveau_reglement.ui", self)
        self.setup_documents_table()

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
