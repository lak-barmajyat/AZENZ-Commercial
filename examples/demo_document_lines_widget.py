"""Runnable demo for :class:`DocumentLinesWidget`.

Run from the project root::

    python -m examples.demo_document_lines_widget
    # or
    python examples/demo_document_lines_widget.py
"""

from __future__ import annotations

import json
import os
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, _ROOT)

from PyQt5.QtWidgets import (  # noqa: E402
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui_utils.widgets.document_lines import (  # noqa: E402
    DocumentLine,
    DocumentLinesWidget,
    default_columns,
)


def build_demo_lines() -> list[DocumentLine]:
    return [
        DocumentLine.product(
            reference="ART-001",
            designation="Consulting day",
            description="Consulting day",
            quantity=2,
            unit="h",
            price_ht=450.0,
            discount_percent=0.0,
            vat_percent=20.0,
            article_id=101,
        ),
        DocumentLine.text("Internal note: deliver before month end."),
        DocumentLine.product(
            reference="ART-014",
            designation="Cable management kit",
            description="Cable management kit",
            quantity=5,
            unit="Unit",
            price_ht=18.5,
            discount_percent=10.0,
            vat_percent=20.0,
            article_id=114,
        ),
    ]


def main() -> int:
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("DocumentLinesWidget - Demo")
    root = QVBoxLayout(window)
    root.setContentsMargins(16, 16, 16, 16)
    root.setSpacing(12)

    widget = DocumentLinesWidget()
    widget.set_columns(default_columns())
    widget.set_currency_symbol("€")
    widget.set_default_vat_percent(20.0)
    widget.set_default_unit("Unit")
    widget.set_units(["Unit", "Kg", "L", "m", "h"])
    widget.set_lines(build_demo_lines())

    totals_label = QLabel("Totals: —")
    totals_label.setObjectName("DemoTotalsLabel")

    def on_totals(totals: dict) -> None:
        totals_label.setText(
            "Totals: HT {total_ht:.2f} € | Discount {total_discount:.2f} € | "
            "TVA {total_tva:.2f} € | TTC {total_ttc:.2f} € | "
            "Lines {line_count} ({product_line_count} products, qty {total_quantity})".format(
                **totals
            )
        )

    widget.totalsChanged.connect(on_totals)
    on_totals(widget.get_document_totals().to_dict())

    widget.lineAdded.connect(
        lambda line, row: print(f"[signal] lineAdded row={row} type={line.line_type.value}")
    )
    widget.lineChanged.connect(
        lambda line, row: print(f"[signal] lineChanged row={row} total_ht={line.total_ht:.2f}")
    )
    widget.lineRemoved.connect(
        lambda line, row: print(f"[signal] lineRemoved row={row}")
    )
    widget.lineSelected.connect(
        lambda line, row: print(f"[signal] lineSelected row={row} ref={line.reference!r}")
    )
    widget.barcodeScanRequested.connect(
        lambda: print("[signal] barcodeScanRequested")
    )
    widget.stockCheckRequested.connect(
        lambda: print("[signal] stockCheckRequested")
    )

    # Simulate a provider whose keys match the configured/default columns.
    fake_catalog = [
        {"article_id": 101, "reference": "LAP-001", "description": "MacBook Pro 14\"", "price_ht": 1999.0, "unit": "pcs", "vat_percent": 20.0},
        {"article_id": 102, "reference": "LAP-002", "description": "Dell XPS 13", "price_ht": 1299.0, "unit": "pcs", "vat_percent": 20.0},
        {"article_id": 103, "reference": "ACC-052", "description": "USB-C Hub", "price_ht": 89.0, "unit": "pcs", "vat_percent": 20.0},
        {"article_id": 104, "reference": "ACC-101", "description": "Wireless Mouse", "price_ht": 29.9, "unit": "pcs", "vat_percent": 20.0},
        {"article_id": 105, "reference": "SRV-001", "description": "On-site support hour", "price_ht": 75.0, "unit": "h", "vat_percent": 20.0},
    ]

    def fake_article_search(query: str) -> list[dict]:
        q = query.lower().strip()
        matches = [
            a
            for a in fake_catalog
            if q in a["reference"].lower() or q in a["description"].lower()
        ]
        print(f"[db] search {query!r} -> {len(matches)} result(s)")
        return matches

    for column_name in ("reference", "description"):
        widget.set_list(
            column_name,
            fake_article_search,
            display_fields=("reference", "description"),
        )

    buttons = QHBoxLayout()
    validate_btn = QPushButton("Validate")
    export_btn = QPushButton("Export lines (dict)")
    clear_btn = QPushButton("Clear")

    def run_validate() -> None:
        ok, errors = widget.validate()
        if ok:
            print("Validation OK")
        else:
            print("Validation errors:")
            for err in errors:
                print(" -", err)

    def run_export() -> None:
        payload = widget.get_lines_as_dicts()
        print("Export payload (placeholder excluded):")
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    validate_btn.clicked.connect(run_validate)
    export_btn.clicked.connect(run_export)
    clear_btn.clicked.connect(widget.clear_lines)

    buttons.addWidget(validate_btn)
    buttons.addWidget(export_btn)
    buttons.addWidget(clear_btn)
    buttons.addStretch(1)

    root.addWidget(widget, stretch=1)
    root.addWidget(totals_label)
    root.addLayout(buttons)

    window.resize(1100, 520)
    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
