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


class NouveauDocumentView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/ventes/nouveau_document.ui", self)

    def setup_table(self):
        # self.DocumentLines is created automatically from the .ui name=
        self.DocumentLines.set_columns(default_columns())
        self.DocumentLines.set_currency_symbol("€")
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
