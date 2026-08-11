from ui_utils.loader import load_ui as loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QToolButton, QWidget

from ui_utils.buttons import install_danger_icon_hover
from ui_utils.widgets.erp_data_table import ERPTableColumn

from modules.reglements.liste_reglements.controller import ReglementsController


class ReglementsView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/reglements/liste_reglements/reglements.ui", self)

        self.setup()
        self.controller = ReglementsController(self)

    def setup(self):
        self.setup_table()
        self.setup_navigation()
        self.setup_danger_buttons()

    def setup_danger_buttons(self):
        install_danger_icon_hover(self.findChild(QToolButton, "SupprimerReglementButton"))

    def setup_navigation(self):
        self.NouveauReglementButton.clicked.connect(self.open_new_reglement)

    def open_new_reglement(self):
        app = QApplication.instance()
        if app is None or not hasattr(app, "window_manager"):
            return
        app.window_manager.open("reglements.nouveau_reglement")

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
