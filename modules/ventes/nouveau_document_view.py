from ui_utils.effects import set_drop_shadow
from ui_utils.canvas import create_uniform_icon, get_colored_icon

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt

from PyQt5.QtWidgets import (
    QAction, QFrame, QMainWindow, QWidget,
    QLineEdit, QToolButton, QHeaderView)

from ui_utils.widgets.document_lines import (
    COL_ACTIONS,
    COL_INDEX,
    COL_TYPE,
    ColumnEditorType,
    DocumentLineColumn,
    DocumentLinesWidget,
    LineType,
)

from modules.ventes.controller import NouveauDocumentController
from modules.ventes.model import NouveauDocumentModel

class NouveauDocumentView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/ventes/nouveau_document.ui", self)

        self.setup_table()

        self.model = NouveauDocumentModel()
        self.controller = NouveauDocumentController(self, self.model)

    def setup_table(self):
        columns = [
            DocumentLineColumn(
                COL_INDEX,
                "#",
                width=36,
                min_width=32,
                editor_type=ColumnEditorType.READONLY,
                align=Qt.AlignCenter,
                editable=False,
            ),
            DocumentLineColumn(
                COL_TYPE,
                "TYPE",
                width=52,
                min_width=44,
                editor_type=ColumnEditorType.READONLY,
                align=Qt.AlignCenter,
                editable=False,
            ),
            DocumentLineColumn("reference", "REFERENCE", width=120, min_width=90),
            DocumentLineColumn(
                "designation",
                "DESIGNATION",
                width=300,
                min_width=160,
                stretch=True,
            ),
            DocumentLineColumn(
                "quantity",
                "QTE",
                width=80,
                min_width=60,
                editor_type=ColumnEditorType.NUMERIC,
                align=Qt.AlignRight | Qt.AlignVCenter,
                decimals=4,
                editable_for=[LineType.PRODUCT, LineType.SERVICE],
            ),
            DocumentLineColumn(
                "unit",
                "UNITE",
                width=75,
                min_width=60,
                editor_type=ColumnEditorType.COMBO,
                align=Qt.AlignCenter,
                editable_for=[LineType.PRODUCT, LineType.SERVICE],
                editable=True,
            ),
            DocumentLineColumn(
                "price_ht",
                "PU HT",
                width=100,
                min_width=80,
                editor_type=ColumnEditorType.NUMERIC,
                align=Qt.AlignRight | Qt.AlignVCenter,
                decimals=2,
                editable_for=[LineType.PRODUCT, LineType.SERVICE],
            ),
            DocumentLineColumn(
                "discount_percent",
                "REM %",
                width=80,
                min_width=60,
                editor_type=ColumnEditorType.NUMERIC,
                align=Qt.AlignRight | Qt.AlignVCenter,
                decimals=2,
                editable_for=[LineType.PRODUCT, LineType.SERVICE],
            ),
            DocumentLineColumn(
                "vat_percent",
                "TVA %",
                width=80,
                min_width=60,
                editor_type=ColumnEditorType.NUMERIC,
                align=Qt.AlignRight | Qt.AlignVCenter,
                decimals=2,
                editable_for=[LineType.PRODUCT, LineType.SERVICE],
            ),
            DocumentLineColumn(
                "total_ht",
                "TOTAL HT",
                width=110,
                min_width=85,
                editor_type=ColumnEditorType.COMPUTED,
                align=Qt.AlignRight | Qt.AlignVCenter,
                editable=False,
            ),
            DocumentLineColumn(
                COL_ACTIONS,
                "ACTIONS",
                width=70,
                min_width=52,
                editor_type=ColumnEditorType.READONLY,
                align=Qt.AlignCenter,
                editable=False,
            ),
        ]

        self.DocumentLines.set_columns(columns)
        self.DocumentLines.set_currency_symbol("DH")
        self.DocumentLines.set_number_format(decimals=2, thousands_sep=" ")
        self.DocumentLines.set_default_vat_percent(20.0)
        self.DocumentLines.set_default_unit("PCS")
        self.DocumentLines.set_units(["PCS", "KG", "L", "M", "H"])
        self.DocumentLines.set_vat_rates([0.0, 7.0, 10.0, 20.0])
        self.DocumentLines.set_tax_enabled(True)
        self.DocumentLines.set_discount_enabled(True)
        self.DocumentLines.set_placeholder_text("Rechercher ou saisir un article...")
        self.DocumentLines.set_search_min_chars(2)
        self.DocumentLines.set_search_debounce_ms(250)
        self.DocumentLines.articleSearchRequested.connect(self.on_article_search)
        self.DocumentLines.totalsChanged.connect(self.on_totals_changed)

    def on_article_search(self, search_text):
        self.DocumentLines.set_article_search_results([])

    def on_totals_changed(self, totals):
        # Implement your totals changed logic here
        pass
