from ui_utils.effects import set_drop_shadow
from ui_utils.widgets.erp_data_table import ERPTableColumn
from modules.ventes.liste_ventes.controller import VentesController

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QAction, QApplication, QFrame, QWidget,
    QLineEdit, QToolButton, QHeaderView)


class VentesView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/ventes/liste_ventes/ventes.ui", self)

        self.setup()
        self.controller = VentesController(self)

    def setup(self):
        self.setup_erp_table()
        self.setup_navigation()

    def setup_navigation(self):
        self.NouveauDocButton.clicked.connect(self.open_new_document)

    def open_new_document(self):
        app = QApplication.instance()
        if app is None or not hasattr(app, "window_manager"):
            return
        app.window_manager.open("ventes.nouveau_doc")

    def setup_erp_table(self):
        # inside VentesView.setup():
        columns = [
            ERPTableColumn("id", "ID", width=100, min_width=700 , visible=False),
            ERPTableColumn("type_document_id", "TYPE DOCUMENT", width=100, min_width=320),
            ERPTableColumn("code_document", "CODE DOCUMENT", width=150, min_width=120, is_link=True),
            ERPTableColumn("autre_code_document", "AUTRE CODE DOCUMENT", width=150, min_width=120),
            ERPTableColumn("document_origine_id", "DOCUMENT ORIGINE", width=180, min_width=120),
            ERPTableColumn("tier_id", "TIER", width=460, min_width=320, stretch=True),
            ERPTableColumn("adresse_livraison_id", "ADRESSE LIVRAISON", width=260, min_width=180),
            ERPTableColumn("utilisateur_id", "UTILISATEUR", width=180, min_width=140),
            ERPTableColumn("vendeur_id", "VENDEUR", width=180, min_width=140),
            ERPTableColumn("montant_ht", "MONTANT HT", width=130, min_width=320, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("montant_remise", "MONTANT REMISE", width=130, min_width=320, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("montant_net_ht", "MONTANT NET HT", width=130, min_width=320, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("montant_tva", "MONTANT TVA", width=130, min_width=320, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("montant_ttc", "MONTANT TTC", width=130, min_width=320, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("montant_net_ttc", "MONTANT NET TTC", width=130, min_width=320, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("montant_paye", "MONTANT PAYE", width=130, min_width=320, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("montant_restant", "MONTANT RESTANT", width=130, min_width=320, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("statut_document_id", "STATUT DOCUMENT", width=130, min_width=320, align=Qt.AlignCenter, is_status=True),
            ERPTableColumn("document_valide", "DOCUMENT VALIDE", width=120, min_width=120),
            ERPTableColumn("document_cloture", "DOCUMENT CLOTURE", width=120, min_width=120),
            ERPTableColumn("date_document", "DATE DOCUMENT", width=110, min_width=320 , is_date=True),
            ERPTableColumn("date_livraison_prevue", "DATE LIVRAISON PREVUE", width=110, min_width=320 , is_date=True),
            ERPTableColumn("date_livraison_effective", "DATE LIVRAISON EFFECTIVE", width=110, min_width=320 , is_date=True),
            ERPTableColumn("transforme", "TRANSFORME", width=100, min_width=120),
            ERPTableColumn("date_transforme", "DATE TRANSFORME", width=110, min_width=320 , is_date=True),
            ERPTableColumn("commentaire", "COMMENTAIRE", width=320, min_width=220),
        ]
        self.VentesTable.set_columns(columns)
        self.VentesTable.rowDoubleClicked.connect(self.open_document)
        # self.VentesTable.selectionChangedRows.connect(self.on_checked_changed)

    def open_document(self, row):
        document_id = row.get("id") if isinstance(row, dict) else row
        if document_id:
            app = QApplication.instance()
            if app is None or not hasattr(app, "window_manager"):
                return
            app.window_manager.open("ventes.nouveau_doc", document_id=document_id)