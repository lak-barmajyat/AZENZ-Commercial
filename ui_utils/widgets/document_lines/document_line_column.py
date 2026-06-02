"""Column configuration for :class:`DocumentLinesWidget`."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from PyQt5.QtCore import Qt

from .document_line import LineType


class ColumnEditorType(str, Enum):
    """Editor / display strategy for a column."""

    TEXT = "text"
    NUMERIC = "numeric"
    COMBO = "combo"
    READONLY = "readonly"
    COMPUTED = "computed"


# Synthetic column keys managed internally by the widget.
COL_INDEX = "_index"
COL_TYPE = "_type"
COL_ACTIONS = "_actions"


@dataclass
class DocumentLineColumn:
    """Describes one configurable column in the document lines table.

    Attributes:
        key: Stable identifier used to read/write line data.
        title: Header label.
        width: Default column width in pixels.
        min_width: Minimum resize width.
        align: Cell text alignment.
        editor_type: Which delegate/editor to use.
        visible: Whether the column is shown.
        stretch: Whether the column stretches to fill free space.
        editable: Whether the column accepts user edits (when not read-only).
        decimals: Decimal places for numeric columns.
        editable_for: Line types allowed to edit this column. Empty means all
            applicable types for the editor.
        combo_key: Optional metadata key for combo options override.
    """

    key: str
    title: str
    width: int = 100
    min_width: int = 48
    align: Qt.AlignmentFlag = Qt.AlignLeft | Qt.AlignVCenter
    editor_type: ColumnEditorType = ColumnEditorType.TEXT
    visible: bool = True
    stretch: bool = False
    editable: bool = True
    decimals: int = 2
    editable_for: list[LineType] = field(default_factory=list)
    combo_key: str = ""

    def is_editable_for(self, line_type: LineType) -> bool:
        if not self.editable:
            return False
        if not self.editable_for:
            return True
        return line_type in self.editable_for


def default_columns() -> list[DocumentLineColumn]:
    """Sensible default column set for generic ERP documents."""
    return [
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
