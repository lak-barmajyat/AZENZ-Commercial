from ui_utils.effects import set_drop_shadow
from ui_utils.canvas import create_uniform_icon, get_colored_icon

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import (
    QAction, QFrame, QMainWindow, QWidget,
    QLineEdit, QToolButton, QHeaderView)

from ui_utils.widgets.document_lines import (
    DocumentLinesWidget,
    default_columns,
)

from modules.ventes.controller import NouveauDocumentController
from modules.ventes.model import NouveauDocumentModel

class NouveauDocumentView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/ventes/nouveau_document.ui", self)

        self.model = NouveauDocumentModel()
        self.controller = NouveauDocumentController(self, self.model)

    def setup_table(self):
        # self.DocumentLines is created automatically from the .ui name=

        # code article
        # designation
        # quantite
        # unit
        # prix ht
        # total ttc
        # prix ttc
        # taux tva
        # affaire
        # marge
        # depot
        # remise
        # 
        columns = [
            DocumentLineColumn(COL_INDEX, "#", width=36, min_width=32,
                            editor_type=ColumnEditorType.READONLY,
                            align=Qt.AlignCenter, editable=False),
            DocumentLineColumn(COL_TYPE, "TYPE", width=44, min_width=40,
                            editor_type=ColumnEditorType.READONLY,
                            align=Qt.AlignCenter, editable=False),
            DocumentLineColumn("reference", "REFERENCE", width=110, min_width=80),
            DocumentLineColumn("description", "DESCRIPTION", width=220,
                            min_width=120),
            DocumentLineColumn("quantity", "QTY", width=72, min_width=56,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter, decimals=4,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("unit", "UNIT", width=72, min_width=56,
                            editor_type=ColumnEditorType.COMBO,
                            align=Qt.AlignCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("price_ht", "PRICE HT", width=96, min_width=72,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("discount_percent", "DISC %", width=72, min_width=56,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter, decimals=2,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("vat_percent", "VAT %", width=72, min_width=56,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter, decimals=2,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("total_ht", "TOTAL HT", width=100, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn(COL_ACTIONS, "ACTIONS", width=52, min_width=48,
                            editor_type=ColumnEditorType.READONLY,
                            align=Qt.AlignCenter, editable=False),
        ]
        self.DocumentLines.set_columns(columns)
        self.DocumentLines.set_currency_symbol("dh")
        self.DocumentLines.set_default_vat_percent(20.0)
        self.DocumentLines.set_units(["Unit", "Kg", "L", "h"])
        # Connect signals to your controller
        self.DocumentLines.articleSearchRequested.connect(self.on_article_search)
        self.DocumentLines.totalsChanged.connect(self.on_totals_changed)

    def on_article_search(self, search_text):
        self.DocumentLines.set_article_search_results([])

    def on_totals_changed(self):
        # Implement your totals changed logic here
        pass
