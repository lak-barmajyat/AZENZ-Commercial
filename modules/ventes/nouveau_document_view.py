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
    DocumentLinesWidget,
    default_columns,
)

from modules.ventes.controller import NouveauDocumentController
from modules.ventes.model import NouveauDocumentModel
from ui_utils.widgets.document_lines.document_lines_widget import (
    DocumentLineColumn,
    ColumnEditorType,
    LineType,
)

class NouveauDocumentView(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/ventes/nouveau_document.ui", self)

        self.model = NouveauDocumentModel()
        self.controller = NouveauDocumentController(self, self.model)

        self.setup()

    def setup(self):
        self.setup_table()

    def setup_table(self):
        # self.DocumentLines is created automatically from the .ui name=

        # Reference                 -> code_article <-> article_id
        # designation               -> designation <-> article_id
        # quantité                  -> quantite
        # unité de vente            -> nom_unite <-> unite_id
        # valeur remise             -> unitaire_remise
        # percentage remise         -> remise_percentage
        # marge unitaire ht         -> unitaire_marge
        # code TVA                  -> code_tva
        # percentage TVA            -> tva_percentage
        # Taux TVA                  -> unitaire_tva
        # Prix ht                   -> prix_unitaire_ht
        # Prix ttc                  -> prix_unitaire_ttc
        # Prix net ht               -> prix_unitaire_net_ht
        # Total TVA                 -> montant_tva
        # Total ht                  -> montant_ht
        # Total ttc                 -> montant_ttc
        # Total net ht              -> montant_net_ht
        # Remise total              -> montant_remise
        # Marge total               -> montant_marge
        # Affaire                   -> nom_projet <-> id_projet
        # Dépot                     -> nom_depot <-> id_depot

        # now create columns for the DocumentLinesWidget according comment above, the titles must be in French
        columns = [
            DocumentLineColumn("_index", "#", width=36, min_width=32,
                            editor_type=ColumnEditorType.READONLY,
                            align=Qt.AlignCenter, editable=False),
            DocumentLineColumn("_type", "TYPE", width=44, min_width=40,
                            editor_type=ColumnEditorType.READONLY,
                            align=Qt.AlignCenter, editable=False),
            DocumentLineColumn("reference_article", "REFERENCE", width=110, min_width=80),
            DocumentLineColumn("designation", "DESIGNATION", width=220,
                            min_width=120),
            DocumentLineColumn("quantite", "QTY", width=72, min_width=56,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter, decimals=4,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("nom_unite", "UNITE", width=72, min_width=56,
                            editor_type=ColumnEditorType.COMBO,
                            align=Qt.AlignCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("unitaire_remise", "REMISE", width=72, min_width=56,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter, decimals=2,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("remise_percentage", "REMISE %", width=72, min_width=56,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter, decimals=2,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("unitaire_marge", "MARGE HT", width=96, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn("code_tva", "CODE TVA", width=72, min_width=56,
                            editor_type=ColumnEditorType.READONLY,
                            align=Qt.AlignCenter, editable=False),
            DocumentLineColumn("tva_percentage", "TVA %", width=72, min_width=56,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter, decimals=2,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("unitaire_tva", "TAUX TVA", width=72, min_width=56,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter, decimals=2,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("prix_unitaire_ht", "PRIX HT", width=96, min_width=72,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("prix_unitaire_ttc", "PRIX TTC", width=96, min_width=72,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("prix_unitaire_net_ht", "PRIX NET HT", width=96, min_width=72,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("montant_tva", "TOTAL TVA", width=96, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn("montant_ht", "TOTAL HT", width=100, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn("montant_ttc", "TOTAL TTC", width=100, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn("montant_net_ht", "TOTAL NET HT", width=100, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn("montant_remise", "REMISE TOTAL", width=100, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn("montant_marge", "MARGE TOTAL", width=100, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn("nom_projet", "AFFAIRE", width=120, min_width=80,
                            editor_type=ColumnEditorType.COMBO,
                            align=Qt.AlignCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("nom_depot", "DEPOT", width=120, min_width=80,
                            editor_type=ColumnEditorType.COMBO,
                            align=Qt.AlignCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("_actions", "ACTIONS", width=52, min_width=48,
                            editor_type=ColumnEditorType.READONLY,
                            align=Qt.AlignCenter, editable=False),
        ]

        self.DocumentLinesWidget.set_columns(columns)
