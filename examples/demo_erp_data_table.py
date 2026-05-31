"""Runnable demo for the reusable :class:`ERPDataTable` component.

Run from the project root::

    python -m examples.demo_erp_data_table
    # or
    python examples/demo_erp_data_table.py
"""

from __future__ import annotations

import os
import sys

# Allow running the file directly (``python examples/demo_erp_data_table.py``)
# by making the project root importable.
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, _ROOT)

from PyQt5.QtCore import Qt  # noqa: E402
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget  # noqa: E402

from ui_utils.widgets.erp_data_table import (  # noqa: E402
    ERPDataTable,
    ERPTableColumn,
)


def build_columns() -> list[ERPTableColumn]:
    return [
        ERPTableColumn("type", "TYPE", width=100),
        ERPTableColumn(
            "numero_document", "N° DOCUMENT", width=150, is_link=True
        ),
        ERPTableColumn("date", "DATE", width=110, is_date=True),
        ERPTableColumn("client", "CLIENT", width=260, min_width=100, stretch=True),
        ERPTableColumn(
            "total_ht", "TOTAL HT", width=130,
            align=Qt.AlignRight, is_money=True,
        ),
        ERPTableColumn(
            "total_ttc", "TOTAL TTC", width=130,
            align=Qt.AlignRight, is_money=True,
        ),
        ERPTableColumn(
            "solde", "SOLDE", width=130, align=Qt.AlignRight, is_money=True
        ),
        ERPTableColumn(
            "statut", "STATUT", width=130,
            align=Qt.AlignCenter, is_status=True,
        ),
    ]


def build_rows() -> list[dict]:
    return [
        {
            "type": "Facture",
            "numero_document": "FAC-2023-001",
            "date": "12/10/2023",
            "client": "Tech Solutions Inc.",
            "total_ht": 1250.00,
            "total_ttc": 1500.00,
            "solde": 1500.00,
            "statut": "Non payé",
        },
        {
            "type": "Facture",
            "numero_document": "FAC-2023-002",
            "date": "14/10/2023",
            "client": "Global Logistics SARL",
            "total_ht": 3400.00,
            "total_ttc": 4080.00,
            "solde": 0.00,
            "statut": "Payé",
        },
        {
            "type": "Devis",
            "numero_document": "DEV-2023-045",
            "date": "15/10/2023",
            "client": "Design Studio",
            "total_ht": 850.00,
            "total_ttc": 1020.00,
            "solde": None,
            "statut": "Brouillon",
        },
        {
            "type": "Facture",
            "numero_document": "FAC-2023-003",
            "date": "18/10/2023",
            "client": "Northwind Traders",
            "total_ht": 9200.00,
            "total_ttc": 11040.00,
            "solde": 11040.00,
            "statut": "Validé",
        },
    ]


def main() -> int:
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("ERPDataTable - Demo (Liste de ventes)")
    layout = QVBoxLayout(window)
    layout.setContentsMargins(16, 16, 16, 16)

    table = ERPDataTable()
    table.set_columns(build_columns())
    table.set_rows(build_rows())

    # Demonstrate the public signals.
    table.rowDoubleClicked.connect(
        lambda row: print(
            "Double-clicked document:", row.get("numero_document")
        )
    )
    table.linkClicked.connect(
        lambda row, key: print(
            f"Link clicked [{key}]:", row.get("numero_document")
        )
    )
    table.selectionChangedData.connect(
        lambda row: print("Selection changed:", row.get("numero_document"))
    )
    # Checkbox column + Ctrl/Shift multi-selection: list every checked row.
    table.selectionChangedRows.connect(
        lambda rows: print(
            "Checked rows:",
            [r.get("numero_document") for r in rows],
        )
    )
    # Footer refresh button: reload the demo rows.
    table.refreshRequested.connect(
        lambda: (print("Refresh requested"), table.set_rows(build_rows()))
    )

    # Demonstrate a customizable context menu.
    table.set_context_menu_actions(
        [
            {
                "text": "Ouvrir",
                "callback": lambda r: print("Ouvrir", r.get("numero_document")),
            },
            {
                "text": "Modifier",
                "callback": lambda r: print(
                    "Modifier", r.get("numero_document")
                ),
            },
            {"separator": True, "text": "-"},
            {
                "text": "Supprimer",
                "callback": lambda r: print(
                    "Supprimer", r.get("numero_document")
                ),
            },
        ]
    )

    layout.addWidget(table)
    window.resize(1000, 500)
    window.show()

    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
