from ui_utils.effects import set_drop_shadow
from ui_utils.canvas import create_uniform_icon, get_colored_icon

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import (
    QAction, QFrame, QMainWindow, QWidget,
    QLineEdit, QToolButton, QHeaderView)

from modules.ventes.controller import VentesController
from modules.ventes.model import VentesModel

class AchatsView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/achats/achats.ui", self)

        # model = AchatsModel()
        # self.controller = AchatsController(self, model)

        from PyQt5.QtCore import Qt
        from ui_utils.widgets.erp_data_table import ERPTableColumn

        # inside VentesView.setup():
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
        # self.AchatsTable.set_rows(rows_from_your_service)
        # self.AchatsTable.rowDoubleClicked.connect(self.open_document)
        # self.AchatsTable.selectionChangedRows.connect(self.on_checked_changed)
