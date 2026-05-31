from ui_utils.effects import set_drop_shadow
from ui_utils.canvas import create_uniform_icon, get_colored_icon

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import (
    QAction, QFrame, QMainWindow, QWidget,
    QLineEdit, QToolButton, QHeaderView)


class VentesView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/ventes/ventes.ui", self)

        from PyQt5.QtCore import Qt
        from ui_utils.widgets.erp_data_table import ERPTableColumn

        # inside VentesView.setup():
        columns = [
            ERPTableColumn("type", "TYPE", width=100),
            ERPTableColumn("numero_document", "N° DOCUMENT", width=150, is_link=True),
            ERPTableColumn("date", "DATE", width=110, is_date=True),
            ERPTableColumn("client", "CLIENT", width=260, stretch=True),
            ERPTableColumn("total_ht", "TOTAL HT", width=130, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("total_ttc", "TOTAL TTC", width=130, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("solde", "SOLDE", width=130, align=Qt.AlignRight, is_money=True),
            ERPTableColumn("statut", "STATUT", width=130, align=Qt.AlignCenter, is_status=True),
        ]
        self.VentesTable.set_columns(columns)
        # self.VentesTable.set_rows(rows_from_your_service)
        # self.VentesTable.rowDoubleClicked.connect(self.open_document)
        # self.VentesTable.selectionChangedRows.connect(self.on_checked_changed)

