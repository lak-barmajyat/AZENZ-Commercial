"""Column configuration for :class:`ERPDataTable`.

A column is a pure data description: it tells the table *how* to render a key
from a row dict, but contains no business logic of its own. This keeps the
reusable table widget completely generic across ERP pages (Ventes, Clients,
Articles, Paiements, Stock, Fournisseurs, ...).
"""

from __future__ import annotations

from dataclasses import dataclass

from PyQt5.QtCore import Qt


@dataclass
class ERPTableColumn:
    """Describes a single column rendered by :class:`ERPDataTable`.

    Attributes:
        key: Key used to read the value from each row ``dict``.
        title: Header label displayed for the column.
        width: Default/initial column width in pixels.
        min_width: Minimum width the column can be resized to.
        align: Text alignment for the cells of this column.
        is_money: Render the value as a formatted amount (e.g. ``1 500.00``).
        is_status: Render the value as a rounded status badge (delegate).
        is_link: Render the value with the primary link style (blue).
        is_date: Marks the column as a date column (used for sorting/format).
        visible: Whether the column is shown.
        stretch: Whether this column should stretch to fill remaining space.
    """

    key: str
    title: str
    width: int = 120
    min_width: int = 60
    align: Qt.AlignmentFlag = Qt.AlignLeft
    is_money: bool = False
    is_status: bool = False
    is_link: bool = False
    is_date: bool = False
    visible: bool = True
    stretch: bool = False
