"""Generic table model used by :class:`ERPDataTable`.

The model is intentionally dumb: it stores ``list[dict]`` rows and a list of
:class:`ERPTableColumn` descriptions, and exposes them through the standard
``QAbstractTableModel`` interface. No database access, no page-specific logic.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QColor

from .erp_table_column import ERPTableColumn

# Custom role used to retrieve the raw (unformatted) value of a cell.
RawValueRole = Qt.UserRole + 1

# Color palette (mirrors the QSS / HTML design).
COLOR_PRIMARY = QColor("#0051DF")
COLOR_TEXT = QColor("#191C1E")
COLOR_MUTED = QColor("#434655")
COLOR_ERROR = QColor("#BA1A1A")


def format_money(value: Any) -> str:
    """Format a number as ``1 500.00`` (space separator, 2 decimals)."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    # Format with comma thousands separator then swap to a thin/regular space.
    return f"{number:,.2f}".replace(",", " ")


def _date_sort_key(value: Any) -> Any:
    """Best-effort parsing of common date formats for sorting."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    return value


class ERPTableModel(QAbstractTableModel):
    """A table model backed by ``list[dict]`` rows and column descriptors."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._columns: list[ERPTableColumn] = []
        self._rows: list[dict] = []
        # When enabled, column 0 is a synthetic, selection-driven checkbox
        # column and the data columns are shifted right by one.
        self._checkbox_enabled = False

    # ------------------------------------------------------------------ #
    # Configuration                                                      #
    # ------------------------------------------------------------------ #
    def set_columns(self, columns: list[ERPTableColumn]) -> None:
        self.beginResetModel()
        self._columns = list(columns)
        self.endResetModel()

    def set_checkbox_enabled(self, enabled: bool) -> None:
        if enabled == self._checkbox_enabled:
            return
        self.beginResetModel()
        self._checkbox_enabled = enabled
        self.endResetModel()

    def checkbox_enabled(self) -> bool:
        return self._checkbox_enabled

    def column_offset(self) -> int:
        """Number of leading synthetic columns (1 if checkbox is shown)."""
        return 1 if self._checkbox_enabled else 0

    def is_checkbox_column(self, column_index: int) -> bool:
        return self._checkbox_enabled and column_index == 0

    def _data_column(self, column_index: int) -> int:
        """Map a model column index to an index into ``self._columns``."""
        return column_index - self.column_offset()

    def columns(self) -> list[ERPTableColumn]:
        return self._columns

    def set_rows(self, rows: list[dict]) -> None:
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def append_row(self, row: dict) -> None:
        position = len(self._rows)
        self.beginInsertRows(QModelIndex(), position, position)
        self._rows.append(row)
        self.endInsertRows()

    def update_row(self, row_index: int, row: dict) -> None:
        if not (0 <= row_index < len(self._rows)):
            return
        self._rows[row_index] = row
        top_left = self.index(row_index, 0)
        bottom_right = self.index(row_index, max(0, self.columnCount() - 1))
        self.dataChanged.emit(top_left, bottom_right)

    def remove_row(self, row_index: int) -> None:
        if not (0 <= row_index < len(self._rows)):
            return
        self.beginRemoveRows(QModelIndex(), row_index, row_index)
        del self._rows[row_index]
        self.endRemoveRows()

    def clear(self) -> None:
        self.beginResetModel()
        self._rows = []
        self.endResetModel()

    # ------------------------------------------------------------------ #
    # Row access helpers                                                 #
    # ------------------------------------------------------------------ #
    def get_row(self, row_index: int) -> dict | None:
        if 0 <= row_index < len(self._rows):
            return self._rows[row_index]
        return None

    def get_value(self, row_index: int, column_index: int) -> Any:
        row = self.get_row(row_index)
        data_col = self._data_column(column_index)
        if row is None or not (0 <= data_col < len(self._columns)):
            return None
        return row.get(self._columns[data_col].key)

    # ------------------------------------------------------------------ #
    # QAbstractTableModel interface                                      #
    # ------------------------------------------------------------------ #
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._columns) + self.column_offset()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None

        # Synthetic checkbox column: no text/value; selection-driven painting.
        if self.is_checkbox_column(index.column()):
            if role == Qt.TextAlignmentRole:
                return int(Qt.AlignCenter)
            return None

        data_col = self._data_column(index.column())
        if not (0 <= data_col < len(self._columns)):
            return None
        column = self._columns[data_col]
        raw_value = self._rows[index.row()].get(column.key)

        if role == RawValueRole:
            return raw_value

        if role == Qt.DisplayRole:
            return self._display_text(column, raw_value)

        if role == Qt.TextAlignmentRole:
            return int(self._alignment(column))

        if role == Qt.ForegroundRole:
            return self._foreground(column, raw_value)

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.DisplayRole,
    ) -> Any:
        if orientation == Qt.Horizontal:
            if self.is_checkbox_column(section):
                if role == Qt.TextAlignmentRole:
                    return int(Qt.AlignCenter)
                return None
            data_col = self._data_column(section)
            if 0 <= data_col < len(self._columns):
                if role == Qt.DisplayRole:
                    return self._columns[data_col].title
                if role == Qt.TextAlignmentRole:
                    return int(Qt.AlignVCenter | Qt.AlignLeft)
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def sort(
        self, column: int, order: Qt.SortOrder = Qt.AscendingOrder
    ) -> None:
        if self.is_checkbox_column(column) or not self._rows:
            return
        data_col = self._data_column(column)
        if not (0 <= data_col < len(self._columns)):
            return
        col = self._columns[data_col]
        reverse = order == Qt.DescendingOrder

        def key(row: dict) -> Any:
            value = row.get(col.key)
            if value is None:
                # Push empty values to the end regardless of order.
                return (1, "")
            if col.is_money:
                try:
                    return (0, float(value))
                except (TypeError, ValueError):
                    return (0, str(value))
            if col.is_date:
                return (0, _date_sort_key(value))
            if isinstance(value, (int, float)):
                return (0, value)
            return (0, str(value).lower())

        self.layoutAboutToBeChanged.emit()
        self._rows.sort(key=key, reverse=reverse)
        self.layoutChanged.emit()

    # ------------------------------------------------------------------ #
    # Rendering helpers                                                  #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _display_text(column: ERPTableColumn, raw_value: Any) -> str:
        if raw_value is None or raw_value == "":
            return "-"
        if column.is_money:
            return format_money(raw_value)
        return str(raw_value)

    @staticmethod
    def _alignment(column: ERPTableColumn) -> Qt.AlignmentFlag:
        if column.is_money:
            return Qt.AlignRight | Qt.AlignVCenter
        if column.is_status:
            return Qt.AlignCenter
        return column.align | Qt.AlignVCenter

    @staticmethod
    def _foreground(column: ERPTableColumn, raw_value: Any) -> QColor | None:
        if column.is_link:
            return COLOR_PRIMARY
        if column.key == "solde":
            try:
                if float(raw_value) > 0:
                    return COLOR_ERROR
            except (TypeError, ValueError):
                pass
            return COLOR_MUTED
        return COLOR_TEXT
