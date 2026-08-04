import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from ui_utils.widgets.document_lines import (
    ColumnEditorType,
    DocumentLine,
    DocumentLineColumn,
    DocumentLinesWidget,
)


def make_widget():
    widget = DocumentLinesWidget()
    widget.set_columns(
        [
            DocumentLineColumn(
                "quantity", "Q", editor_type=ColumnEditorType.NUMERIC
            ),
            DocumentLineColumn(
                "price_ht", "P", editor_type=ColumnEditorType.NUMERIC
            ),
            DocumentLineColumn(
                "total_ht",
                "T",
                editor_type=ColumnEditorType.COMPUTED,
                editable=False,
            ),
            DocumentLineColumn(
                "tax_amount",
                "VAT",
                editor_type=ColumnEditorType.COMPUTED,
                editable=False,
            ),
        ]
    )
    return widget


def edit(widget, column_name, value):
    column = widget.model().column_index_for_key(column_name)
    assert widget.model().setData(
        widget.model().index(0, column), value, Qt.EditRole
    )


class ColumnUpdateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])

    def test_cascades_and_emits_one_row_change(self):
        widget = make_widget()
        widget.set_column_updates(
            "quantity",
            {"price_ht": lambda row: row["quantity"] * 2},
            name="price",
        )
        widget.set_column_updates(
            "price_ht",
            {"total_ht": lambda row: row["quantity"] * row["price_ht"]},
            name="total",
        )
        widget.set_lines([DocumentLine.product(quantity=2, price_ht=1)])
        changes = []
        widget.lineChanged.connect(lambda *args: changes.append(args))

        edit(widget, "quantity", 3)

        line = widget.get_line(0)
        self.assertEqual((line.quantity, line.price_ht, line.total_ht), (3, 6, 18))
        self.assertEqual(len(changes), 1)

    def test_resolver_load_policy_and_failure_behavior(self):
        widget = make_widget()
        calls = []
        errors = []
        widget.columnUpdateFailed.connect(lambda *args: errors.append(args))
        widget.set_column_updates(
            "quantity",
            lambda row: calls.append(row["quantity"])
            or {"tax_amount": row["quantity"] + 5},
            name="resolver",
        )
        widget.set_lines([DocumentLine.product(quantity=4)])
        self.assertEqual(calls, [])

        edit(widget, "quantity", 5)
        self.assertEqual(calls, [5])
        self.assertEqual(widget.get_line(0).tax_amount, 10)

        def broken(_row):
            raise RuntimeError("lookup failed")

        widget.set_column_updates("price_ht", broken, name="broken")
        edit(widget, "price_ht", 12)
        self.assertEqual(widget.get_line(0).price_ht, 12)
        self.assertTrue(
            any(error[2:] == ("broken", "lookup failed") for error in errors)
        )

    def test_validation_rejects_unknown_columns_and_static_cycles(self):
        widget = make_widget()
        widget.set_column_updates(
            "quantity", {"price_ht": lambda _row: 1}, name="forward"
        )
        with self.assertRaisesRegex(ValueError, "cycle"):
            widget.set_column_updates(
                "price_ht", {"quantity": lambda _row: 1}, name="backward"
            )
        with self.assertRaisesRegex(ValueError, "Unknown source"):
            widget.set_column_updates(
                "missing", {"total_ht": lambda _row: 1}
            )

    def test_dynamic_resolver_cycle_is_stopped(self):
        widget = make_widget()
        errors = []
        widget.columnUpdateFailed.connect(lambda *args: errors.append(args))
        widget.set_column_updates(
            "quantity",
            lambda row: {"price_ht": row["price_ht"] + 1},
            name="dynamic_a",
        )
        widget.set_column_updates(
            "price_ht",
            lambda row: {"quantity": row["quantity"] + 1},
            name="dynamic_b",
        )
        widget.set_lines([DocumentLine.product(quantity=1, price_ht=1)])

        edit(widget, "quantity", 2)

        self.assertTrue(
            any("cycle" in error[3].lower() for error in errors), errors
        )


if __name__ == "__main__":
    unittest.main()
