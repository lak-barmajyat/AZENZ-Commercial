from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

from ui_utils.widgets.erp_data_table import ERPTableColumn

from modules.achats.liste_achats.controller import AchatsController


class AchatsView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/achats/liste_achats/achats.ui", self)

        self.setup()
        self.controller = AchatsController(self)

    def setup(self):
        self.setup_table()
        self.setup_navigation()

    def setup_table(self):
        columns = [
            ERPTableColumn("id", "ID", width=100, visible=False),
            ERPTableColumn("utilisateur_id", "ID", width=100, visible=False),
            ERPTableColumn("vendeur_id", "ID", width=100, visible=False),
            ERPTableColumn("type", "TYPE", width=100),
            ERPTableColumn("numero_document", "N° DOCUMENT", width=150, is_link=True),
            ERPTableColumn("icon", "ICON", width=100),
            ERPTableColumn("date", "DATE", width=110, is_date=True),
            ERPTableColumn("client", "CLIENT", width=260, stretch=True),
            ERPTableColumn("total_ht", "TOTAL HT", width=130, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("total_ttc", "TOTAL TTC", width=130, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("solde", "SOLDE", width=130, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("statut", "STATUT", width=130, align=Qt.AlignCenter, is_status=True),
        ]
        self.AchatsTable.set_columns(columns)
        self.AchatsTable.rowDoubleClicked.connect(self.open_document)

    def setup_navigation(self):
        pass

    def open_document(self, row):
        document_id = row.get("id") if isinstance(row, dict) else row
        if document_id:
            app = QApplication.instance()
            if app is None or not hasattr(app, "window_manager"):
                return
            app.window_manager.open("achats.nouveau_doc", document_id=document_id)
