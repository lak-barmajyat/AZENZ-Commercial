import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QApplication

from ui_utils.widgets.document_lines import (
    DocumentLine,
    DocumentLineColumn,
    DocumentLinesWidget,
)


class ColumnSettingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])

    def make_widget(self):
        widget = DocumentLinesWidget()
        widget.set_columns(
            [
                DocumentLineColumn("designation", "Designation"),
                DocumentLineColumn("projet_id", "Project"),
                DocumentLineColumn("depot_id", "Depot"),
            ]
        )
        return widget

    def test_visibility_can_be_applied_as_one_configuration(self):
        widget = self.make_widget()
        changes = []
        widget.columnVisibilityChanged.connect(changes.append)

        widget.set_visible_columns(["designation", "depot_id"])

        self.assertEqual(widget.visible_columns(), ["designation", "depot_id"])
        self.assertIsNone(widget.model().column_index_for_key("projet_id"))
        self.assertEqual(changes, [["designation", "depot_id"]])

    def test_id_columns_render_configured_name_fields(self):
        widget = self.make_widget()
        widget.set_list(
            "projet_id",
            [{"projet_id": 7, "nom_projet": "Project Atlas"}],
            display_fields="nom_projet",
        )
        widget.set_list(
            "depot_id",
            [{"depot_id": 4, "nom_depot": "Central depot"}],
            display_fields=("nom_depot",),
        )
        widget.set_lines(
            [
                DocumentLine.product(
                    metadata={
                        "projet_id": 7,
                        "nom_projet": "Project Atlas",
                        "depot_id": 4,
                        "nom_depot": "Central depot",
                    }
                )
            ],
            recalculate=False,
        )

        for key, label, raw in (
            ("projet_id", "Project Atlas", "7"),
            ("depot_id", "Central depot", "4"),
        ):
            column = widget.model().column_index_for_key(key)
            index = widget.model().index(0, column)
            self.assertEqual(widget.model().data(index, Qt.DisplayRole), label)
            self.assertEqual(widget.model().data(index, Qt.EditRole), raw)

    def test_visibility_is_restored_from_qsettings(self):
        key = "tests/document_lines/column_visibility"
        path = f"DocumentLinesWidget/{key}/visible_columns"
        settings = QSettings("AZENZ", "AZENZ")
        settings.remove(path)
        try:
            first = self.make_widget()
            first.set_column_settings_key(key)
            first.set_visible_columns(["designation", "depot_id"])

            second = DocumentLinesWidget()
            second.set_column_settings_key(key)
            second.set_columns(
                [
                    DocumentLineColumn("designation", "Designation"),
                    DocumentLineColumn("projet_id", "Project"),
                    DocumentLineColumn("depot_id", "Depot"),
                ]
            )
            self.assertEqual(
                second.visible_columns(), ["designation", "depot_id"]
            )
        finally:
            settings.remove(path)
            settings.sync()

    def test_tax_toggle_accepts_database_column_name(self):
        widget = DocumentLinesWidget()
        widget.set_columns(
            [
                DocumentLineColumn("designation", "Designation"),
                DocumentLineColumn("tva_percentage", "TVA"),
            ]
        )
        widget.set_tax_enabled(True)
        self.assertIn("tva_percentage", widget.visible_columns())
        widget.set_tax_enabled(False)
        self.assertNotIn("tva_percentage", widget.visible_columns())
        widget.set_tax_enabled(True)
        self.assertIn("tva_percentage", widget.visible_columns())


if __name__ == "__main__":
    unittest.main()
