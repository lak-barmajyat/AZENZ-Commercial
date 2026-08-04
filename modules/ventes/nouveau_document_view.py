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
from ui_utils.widgets.document_lines.document_lines_widget import (
    DocumentLineColumn,
    ColumnEditorType,
    LineType,
)

class NouveauDocumentView(QWidget):
    def __init__(self, document_id=None):
        super().__init__()
        loadUi("modules/ventes/nouveau_document.ui", self)

        self.model = NouveauDocumentModel()
        self.controller = NouveauDocumentController(self, self.model, document_id=document_id)
        self.setup()
        self.show()

    def setup(self):
        self.setup_table()
        self.setup_client_searchable_combo()

    def setup_table(self):
        # self.DocumentLines is created automatically from the .ui name=

        # Reference                 -> code_article <-> article_id
        # designation               -> designation <-> article_id
        # quantité                  -> quantite
        # unité de vente            -> unite_id
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
        # Affaire                   -> projet_id
        # Dépot                     -> depot_id

        # now create columns for the DocumentLinesWidget according comment above, the titles must be in French
        columns = [
            DocumentLineColumn("_index", "#", width=36, min_width=32,
                            editor_type=ColumnEditorType.READONLY,
                            align=Qt.AlignCenter, editable=False),
            DocumentLineColumn("_type", "TYPE", width=44, min_width=40,
                            editor_type=ColumnEditorType.READONLY,
                            align=Qt.AlignCenter, editable=False),
            DocumentLineColumn("code_article", "REFERENCE", width=110, min_width=80),
            DocumentLineColumn("designation", "DESIGNATION", width=220,
                            min_width=120),
            DocumentLineColumn("quantite", "QTY", width=72, min_width=56,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter, decimals=4,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("unite_id", "UNITE", width=72, min_width=56,
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
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, decimals=2,
                            editable=False),
            DocumentLineColumn("prix_unitaire_ht", "PRIX HT", width=96, min_width=72,
                            editor_type=ColumnEditorType.NUMERIC,
                            align=Qt.AlignRight | Qt.AlignVCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("prix_revient_unitaire", "PRIX REVIENT", visible=False,
                            editor_type=ColumnEditorType.NUMERIC),
            DocumentLineColumn("prix_unitaire_ttc", "PRIX TTC", width=96, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter,
                            editable=False),
            DocumentLineColumn("prix_unitaire_net_ht", "PRIX NET HT", width=96, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter,
                            editable=False),
            DocumentLineColumn("prix_unitaire_net_ttc", "PRIX NET TTC", width=96, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
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
            DocumentLineColumn("montant_net_ttc", "TOTAL NET TTC", width=100, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn("montant_remise", "REMISE TOTAL", width=100, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn("montant_marge", "MARGE TOTAL", width=100, min_width=72,
                            editor_type=ColumnEditorType.COMPUTED,
                            align=Qt.AlignRight | Qt.AlignVCenter, editable=False),
            DocumentLineColumn("projet_id", "AFFAIRE", width=120, min_width=80,
                            align=Qt.AlignCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("depot_id", "DEPOT", width=120, min_width=80,
                            align=Qt.AlignCenter,
                            editable_for=[LineType.PRODUCT, LineType.SERVICE]),
            DocumentLineColumn("_actions", "ACTIONS", width=52, min_width=48,
                            editor_type=ColumnEditorType.READONLY,
                            align=Qt.AlignCenter, editable=False),
        ]

        self.DocumentLinesWidget.set_column_settings_key(
            "ventes/nouveau_document/document_lines"
        )
        self.DocumentLinesWidget.set_columns(columns)

        # Searchable lists are page configuration, not widget-specific logic.
        # Any other page can attach its own provider and mapping to any column.
        self.DocumentLinesWidget.set_list(
            "code_article", self.model.search_articles,
            display_fields=("code_article",),
        )
        self.DocumentLinesWidget.set_list(
            "designation", self.model.search_articles,
            display_fields=("designation",),
        )
        self.DocumentLinesWidget.set_list(
            "unite_id", self.model.search_units,
            display_fields=("nom_unite",),
        )
        self.DocumentLinesWidget.set_list(
            "projet_id", self.model.search_projects,
            display_fields=("nom_projet",),
        )
        self.DocumentLinesWidget.set_list(
            "depot_id", self.model.search_depots,
            display_fields=("nom_depot",),
        )

        def number(row, column_name):
            try:
                return float(row.get(column_name) or 0)
            except (TypeError, ValueError):
                return 0.0

        def unit_ht(row):
            return number(row, "prix_unitaire_ht")

        def quantity(row):
            return max(number(row, "quantite"), 0.0)

        def discount_rate(row):
            return min(max(number(row, "remise_percentage"), 0.0), 100.0)

        def vat_rate(row):
            return min(max(number(row, "tva_percentage"), 0.0), 100.0)

        def unit_discount(row):
            return unit_ht(row) * discount_rate(row) / 100.0

        def unit_ttc(row):
            return unit_ht(row) * (1.0 + vat_rate(row) / 100.0)

        def unit_net_ht(row):
            return unit_ht(row) - unit_discount(row)

        def unit_net_ttc(row):
            return unit_ttc(row) * (1.0 - discount_rate(row) / 100.0)

        def unit_margin(row):
            return unit_net_ht(row) - number(row, "prix_revient_unitaire")

        def unit_vat(row):
            return unit_ht(row) * vat_rate(row) / 100.0

        self.DocumentLinesWidget.set_column_updates(
            source_columns=(
                "quantite",
                "prix_unitaire_ht",
                "remise_percentage",
                "tva_percentage",
                "prix_revient_unitaire",
            ),
            updates={
                "prix_unitaire_ttc": lambda row: round(unit_ttc(row), 6),
                "prix_unitaire_net_ht": lambda row: round(unit_net_ht(row), 6),
                "prix_unitaire_net_ttc": lambda row: round(unit_net_ttc(row), 6),
                "unitaire_remise": lambda row: round(unit_discount(row), 6),
                "unitaire_marge": lambda row: round(unit_margin(row), 6),
                "unitaire_tva": lambda row: round(unit_vat(row), 2),
                "montant_ht": lambda row: round(quantity(row) * unit_ht(row), 6),
                "montant_ttc": lambda row: round(quantity(row) * unit_ttc(row), 6),
                "montant_net_ht": lambda row: round(quantity(row) * unit_net_ht(row), 6),
                "montant_net_ttc": lambda row: round(quantity(row) * unit_net_ttc(row), 6),
                "montant_remise": lambda row: round(quantity(row) * unit_discount(row), 6),
                "montant_marge": lambda row: round(quantity(row) * unit_margin(row), 6),
                "montant_tva": lambda row: round(quantity(row) * unit_vat(row), 6),
            },
            name="sales_line_generated_columns",
        )

    def setup_client_searchable_combo(self):
        self.ClientcomboBox.setEditable(True)
        self.ClientcomboBox.setInsertPolicy(self.ClientcomboBox.NoInsert)
        self.ClientcomboBox.setCurrentIndex(-1)
        self.ClientcomboBox.lineEdit().setPlaceholderText("Type to search...")
