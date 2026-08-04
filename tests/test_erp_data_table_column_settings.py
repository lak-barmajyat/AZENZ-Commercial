import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import QPoint, QPointF, Qt
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QApplication, QDialog

from ui_utils.widgets.erp_data_table import ERPDataTable, ERPTableColumn


class ERPDataTableColumnSettingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])

    def make_widget(self):
        widget = ERPDataTable()
        widget.set_columns(
            [
                ERPTableColumn("id", "ID", visible=False),
                ERPTableColumn("code", "Code"),
                ERPTableColumn("name", "Name", stretch=True),
            ]
        )
        return widget

    def test_footer_contains_refresh_and_columns_buttons(self):
        widget = self.make_widget()
        footer_layout = widget._footer.layout()
        button_texts = [
            footer_layout.itemAt(index).widget().text()
            for index in range(footer_layout.count())
            if footer_layout.itemAt(index).widget() is not None
        ]

        self.assertIn("Actualiser", button_texts)
        self.assertIn("Colonnes…", button_texts)
        self.assertLess(
            button_texts.index("Actualiser"), button_texts.index("Colonnes…")
        )

    def test_column_settings_updates_visible_columns(self):
        widget = self.make_widget()

        class FakeDialog:
            def __init__(self, columns, parent=None):
                self._columns = columns

            def exec_(self):
                return QDialog.Accepted

            def selected_columns(self):
                return ["name"]

        with patch(
            "ui_utils.widgets.erp_data_table.erp_data_table._ColumnSettingsDialog",
            FakeDialog,
        ):
            widget.open_column_settings()

        self.assertEqual(widget.visible_columns(), ["name"])
        self.assertEqual(widget.model().columnCount(), 2)

    def test_column_settings_reset_restores_defaults(self):
        from ui_utils.widgets.erp_data_table.erp_data_table import _ColumnSettingsDialog

        dialog = _ColumnSettingsDialog(
            [
                ERPTableColumn("code", "Code", visible=False),
                ERPTableColumn("name", "Name", visible=True),
            ]
        )
        dialog._checks["code"].setChecked(True)
        dialog._checks["name"].setChecked(False)

        dialog._reset_defaults()

        self.assertEqual(dialog.selected_columns(), ["name"])

    def test_shift_wheel_scrolls_horizontally(self):
        widget = ERPDataTable()
        widget.set_columns(
            [
                ERPTableColumn(f"col_{index}", f"Column {index}", width=240)
                for index in range(6)
            ]
        )
        widget.resize(360, 240)
        widget.show()
        self.application.processEvents()

        scrollbar = widget.view().horizontalScrollBar()
        self.assertGreater(scrollbar.maximum(), 0)

        scrollbar.setValue(scrollbar.maximum() // 2)
        start_value = scrollbar.value()
        position = widget.view().viewport().rect().center()
        wheel_event = QWheelEvent(
            QPointF(position),
            QPointF(position),
            QPoint(),
            QPoint(0, 120),
            0,
            Qt.Vertical,
            Qt.NoButton,
            Qt.ShiftModifier,
        )

        QApplication.sendEvent(widget.view().viewport(), wheel_event)

        self.assertLess(scrollbar.value(), start_value)


if __name__ == "__main__":
    unittest.main()
