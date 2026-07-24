"""Table model for :class:`DocumentLinesWidget`."""

from __future__ import annotations

from typing import Any

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QColor

from .calculations import recalculate_line
from .document_line import DocumentLine, LineType
from .document_line_column import (
    COL_ACTIONS,
    COL_INDEX,
    COL_TYPE,
    ColumnEditorType,
    DocumentLineColumn,
)

# Custom roles
LineTypeRole = Qt.UserRole + 1
IsPlaceholderRole = Qt.UserRole + 2
RawValueRole = Qt.UserRole + 3
LineObjectRole = Qt.UserRole + 4

COLOR_TEXT = QColor("#191C1E")
COLOR_MUTED = QColor("#9CA3AF")
COLOR_PRIMARY = QColor("#0051DF")


def format_number(value: Any, decimals: int = 2, thousands_sep: str = " ") -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    fmt = f"{{:,.{decimals}f}}"
    return fmt.format(number).replace(",", thousands_sep)


class DocumentLinesModel(QAbstractTableModel):
    """Editable model backed by :class:`DocumentLine` objects.

    The last row is always a UI-only placeholder/search row and must never be
    exported as business data.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._columns: list[DocumentLineColumn] = []
        self._lines: list[DocumentLine] = []
        self._read_only = False
        self._tax_enabled = True
        self._discount_enabled = True
        self._currency_symbol = ""
        self._number_decimals = 2
        self._thousands_sep = " "
        self._units: list[str] = ["Unit"]
        self._placeholder_text = "Search or type article..."
        self._recalculating = False
        self._placeholder_state: dict[str, str] = {
            "reference": "",
            "description": "",
            "designation": "",
        }

    # ------------------------------------------------------------------ #
    # Configuration                                                      #
    # ------------------------------------------------------------------ #
    def set_columns(self, columns: list[DocumentLineColumn]) -> None:
        self.beginResetModel()
        self._columns = [c for c in columns if c.visible]
        self.endResetModel()

    def columns(self) -> list[DocumentLineColumn]:
        return list(self._columns)

    def column_by_key(self, key: str) -> DocumentLineColumn | None:
        for col in self._columns:
            if col.key == key:
                return col
        return None

    def column_index_for_key(self, key: str) -> int | None:
        for idx, col in enumerate(self._columns):
            if col.key == key:
                return idx
        return None

    def set_read_only(self, read_only: bool) -> None:
        self._read_only = read_only

    def set_tax_enabled(self, enabled: bool) -> None:
        self._tax_enabled = enabled
        self._refresh_all_rows()

    def set_discount_enabled(self, enabled: bool) -> None:
        self._discount_enabled = enabled
        self._refresh_all_rows()

    def set_currency_symbol(self, symbol: str) -> None:
        self._currency_symbol = symbol or ""
        self._refresh_all_rows()

    def set_number_format(self, decimals: int = 2, thousands_sep: str = " ") -> None:
        self._number_decimals = decimals
        self._thousands_sep = thousands_sep
        self._refresh_all_rows()

    def set_units(self, units: list[str]) -> None:
        self._units = list(units) if units else ["Unit"]

    def units(self) -> list[str]:
        return list(self._units)

    def set_placeholder_text(self, text: str) -> None:
        self._placeholder_text = text
        row = self.placeholder_row_index()
        if row >= 0:
            idx = self.index(row, 0)
            self.dataChanged.emit(idx, self.index(row, self.columnCount() - 1))

    # ------------------------------------------------------------------ #
    # Line access                                                        #
    # ------------------------------------------------------------------ #
    def lines(self) -> list[DocumentLine]:
        return list(self._lines)

    def line_at(self, row: int) -> DocumentLine | None:
        if self.is_placeholder_row(row):
            return None
        if 0 <= row < len(self._lines):
            return self._lines[row]
        return None

    def placeholder_row_index(self) -> int:
        return len(self._lines)

    def is_placeholder_row(self, row: int) -> bool:
        return row == len(self._lines)

    def real_row_count(self) -> int:
        return len(self._lines)

    # ------------------------------------------------------------------ #
    # QAbstractTableModel                                                #
    # ------------------------------------------------------------------ #
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._lines) + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._columns)

    def headerData(  # noqa: N802
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.DisplayRole,
    ) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if 0 <= section < len(self._columns):
                return self._columns[section].title
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:  # noqa: N802
        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        row, col = index.row(), index.column()
        column = self._columns[col]

        if column.key in (COL_INDEX, COL_TYPE, COL_ACTIONS):
            return flags

        if self._read_only:
            return flags

        if self.is_placeholder_row(row):
            if column.key in ("reference", "description", "designation"):
                return flags | Qt.ItemIsEditable
            return flags

        line = self.line_at(row)
        if line is None:
            return flags

        if column.editor_type in (
            ColumnEditorType.READONLY,
            ColumnEditorType.COMPUTED,
        ):
            return flags

        if column.key == "discount_percent" and not self._discount_enabled:
            return flags
        if column.key in ("vat_percent", "tax_amount") and not self._tax_enabled:
            return flags

        if line.line_type == LineType.TEXT:
            if column.key in ("description", "designation"):
                return flags | Qt.ItemIsEditable
            return flags

        if line.line_type == LineType.SEPARATOR:
            return flags

        if column.is_editable_for(line.line_type):
            return flags | Qt.ItemIsEditable

        return flags

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:  # noqa: N802
        if not index.isValid():
            return None

        row, col = index.row(), index.column()
        column = self._columns[col]

        if self.is_placeholder_row(row):
            return self._placeholder_data(column, role)

        line = self.line_at(row)
        if line is None:
            return None

        if role == LineTypeRole:
            return line.line_type
        if role == IsPlaceholderRole:
            return False
        if role == LineObjectRole:
            return line

        if column.key == COL_INDEX:
            if role in (Qt.DisplayRole, Qt.EditRole):
                return row + 1
            return None

        if column.key == COL_TYPE:
            if role == Qt.DisplayRole:
                return line.line_type.value
            return None

        if column.key == COL_ACTIONS:
            return None

        raw = self._raw_value(line, column.key)

        if role == RawValueRole:
            return raw

        if role == Qt.TextAlignmentRole:
            return int(column.align)

        if role == Qt.ForegroundRole:
            if line.line_type == LineType.TEXT and column.key in (
                "description",
                "designation",
            ):
                return COLOR_MUTED
            return COLOR_TEXT

        if role == Qt.FontRole:
            from PyQt5.QtGui import QFont

            font = QFont()
            if line.line_type == LineType.TEXT and column.key in (
                "description",
                "designation",
            ):
                font.setItalic(True)
            elif line.line_type == LineType.PRODUCT and column.key in (
                "description",
                "designation",
                "total_ht",
            ):
                font.setBold(column.key == "total_ht" or column.key == "description")
            return font

        if role in (Qt.DisplayRole, Qt.EditRole):
            if line.line_type == LineType.TEXT and column.key not in (
                "description",
                "designation",
                "reference",
            ):
                return "" if role == Qt.DisplayRole else None

            if line.line_type == LineType.SEPARATOR:
                if column.key in ("description", "designation"):
                    return "—" if role == Qt.DisplayRole else ""
                return "" if role == Qt.DisplayRole else None

            if column.editor_type == ColumnEditorType.COMPUTED:
                return self._format_computed(line, column.key)
            if column.editor_type == ColumnEditorType.NUMERIC:
                if raw is None or raw == "":
                    return "" if role == Qt.DisplayRole else 0.0
                if role == Qt.EditRole:
                    return float(raw)
                decimals = column.decimals
                return format_number(raw, decimals, self._thousands_sep)
            if column.editor_type == ColumnEditorType.COMBO:
                return str(raw or "")
            return str(raw or "")

        return None

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:  # noqa: N802
        if role != Qt.EditRole or not index.isValid():
            return False

        row, col = index.row(), index.column()
        column = self._columns[col]

        if column.key in (COL_INDEX, COL_TYPE, COL_ACTIONS):
            return False

        if self.is_placeholder_row(row):
            return self._set_placeholder_data(column.key, value)

        line = self.line_at(row)
        if line is None:
            return False

        if not self._assign_value(line, column.key, value):
            return False

        self._recalculate_and_emit(row)
        return True

    # ------------------------------------------------------------------ #
    # Mutations                                                          #
    # ------------------------------------------------------------------ #
    def set_lines(self, lines: list[DocumentLine], *, recalculate: bool = True) -> None:
        self.beginResetModel()
        self._lines = [line.clone() if hasattr(line, "clone") else line for line in lines]
        if recalculate:
            for line in self._lines:
                recalculate_line(line)
        self.endResetModel()

    def add_line(self, line: DocumentLine, *, position: int | None = None) -> int:
        recalculate_line(line)
        if position is None or position < 0 or position > len(self._lines):
            position = len(self._lines)
        self.beginInsertRows(QModelIndex(), position, position)
        self._lines.insert(position, line)
        self.endInsertRows()
        return position

    def remove_line(self, row: int) -> DocumentLine | None:
        if self.is_placeholder_row(row) or not (0 <= row < len(self._lines)):
            return None
        self.beginRemoveRows(QModelIndex(), row, row)
        removed = self._lines.pop(row)
        self.endRemoveRows()
        return removed

    def update_line(self, row: int, line: DocumentLine) -> None:
        if self.is_placeholder_row(row) or not (0 <= row < len(self._lines)):
            return
        recalculate_line(line)
        self._lines[row] = line
        left = self.index(row, 0)
        right = self.index(row, self.columnCount() - 1)
        self.dataChanged.emit(left, right)

    def move_line(self, from_row: int, to_row: int) -> bool:
        if (
            self.is_placeholder_row(from_row)
            or self.is_placeholder_row(to_row)
            or not (0 <= from_row < len(self._lines))
            or not (0 <= to_row < len(self._lines))
            or from_row == to_row
        ):
            return False

        line = self._lines.pop(from_row)
        self._lines.insert(to_row, line)

        dest_from = min(from_row, to_row)
        dest_to = max(from_row, to_row)
        top_left = self.index(dest_from, 0)
        bottom_right = self.index(dest_to, self.columnCount() - 1)
        self.dataChanged.emit(top_left, bottom_right)
        return True

    def clear_lines(self) -> None:
        if not self._lines:
            return
        self.beginResetModel()
        self._lines.clear()
        self.endResetModel()

    def recalculate_all(self) -> None:
        for line in self._lines:
            recalculate_line(line)
        self._refresh_all_rows()

    # ------------------------------------------------------------------ #
    # Placeholder row state (UI-only, never exported)                    #
    # ------------------------------------------------------------------ #
    def clear_placeholder(self) -> None:
        self._placeholder_state = {
            "reference": "",
            "description": "",
            "designation": "",
        }
        row = self.placeholder_row_index()
        if row >= 0:
            self.dataChanged.emit(
                self.index(row, 0),
                self.index(row, self.columnCount() - 1),
            )

    def placeholder_search_text(self) -> str:
        return (
            self._placeholder_state.get("reference", "")
            or self._placeholder_state.get("description", "")
            or self._placeholder_state.get("designation", "")
        )

    # ------------------------------------------------------------------ #
    # Internal helpers                                                   #
    # ------------------------------------------------------------------ #
    def _raw_value(self, line: DocumentLine, key: str) -> Any:
        if key == "description" and line.description:
            return line.description
        if key == "designation" and line.designation:
            return line.designation
        if hasattr(line, key):
            return getattr(line, key)
        return line.metadata.get(key)

    def _format_computed(self, line: DocumentLine, key: str) -> str:
        mapping = {
            "amount_ht": line.amount_ht,
            "discount_amount": line.discount_amount,
            "total_ht": line.total_ht,
            "tax_amount": line.tax_amount,
            "total_ttc": line.total_ttc,
        }
        value = mapping.get(key, getattr(line, key, 0))
        text = format_number(value, self._number_decimals, self._thousands_sep)
        if self._currency_symbol and key in (
            "amount_ht",
            "discount_amount",
            "total_ht",
            "tax_amount",
            "total_ttc",
            "price_ht",
        ):
            return f"{text} {self._currency_symbol}".strip()
        return text

    def _assign_value(self, line: DocumentLine, key: str, value: Any) -> bool:
        numeric_keys = {
            "quantity",
            "price_ht",
            "discount_percent",
            "vat_percent",
            "amount_ht",
            "discount_amount",
            "total_ht",
            "tax_amount",
            "total_ttc",
        }
        if key in numeric_keys:
            try:
                converted: Any = float(value)
            except (TypeError, ValueError):
                converted = 0.0
        elif key == "article_id" or key == "unit_id" or key == "vat_id":
            try:
                converted = int(value) if value not in (None, "") else None
            except (TypeError, ValueError):
                converted = None
        else:
            converted = str(value) if value is not None else ""

        if hasattr(line, key):
            setattr(line, key, converted)
        else:
            line.metadata[key] = converted
        return True

    def _placeholder_data(self, column: DocumentLineColumn, role: int) -> Any:
        if role == IsPlaceholderRole:
            return True
        if role == LineTypeRole:
            return None

        if column.key == COL_INDEX:
            if role in (Qt.DisplayRole, Qt.EditRole):
                return "*"
            return None

        if column.key == COL_TYPE:
            if role == Qt.DisplayRole:
                return "placeholder"
            return None

        if role == Qt.TextAlignmentRole:
            return int(column.align)

        if role == Qt.ForegroundRole:
            return COLOR_MUTED

        if role == Qt.FontRole:
            from PyQt5.QtGui import QFont

            font = QFont()
            font.setItalic(True)
            return font

        if role in (Qt.DisplayRole, Qt.EditRole):
            if column.key == COL_INDEX:
                return "*"
            if column.key in ("reference", "description", "designation"):
                stored = self._placeholder_state.get(column.key, "")
                if role == Qt.EditRole:
                    return stored
                return stored or (
                    self._placeholder_text if column.key == "description" else ""
                )
            if column.editor_type == ColumnEditorType.NUMERIC:
                if column.key == "quantity":
                    return "1" if role == Qt.DisplayRole else 1.0
                return "0.00" if role == Qt.DisplayRole else 0.0
            if column.key == "unit":
                return "Unit"
            return ""

        return None

    def _set_placeholder_data(self, key: str, value: Any) -> bool:
        if key not in ("reference", "description", "designation"):
            return False
        self._placeholder_state[key] = str(value or "")
        row = self.placeholder_row_index()
        col = self.column_index_for_key(key)
        if col is not None:
            idx = self.index(row, col)
            self.dataChanged.emit(idx, idx)
        return True

    def _recalculate_and_emit(self, row: int) -> None:
        if self._recalculating:
            return
        self._recalculating = True
        try:
            line = self.line_at(row)
            if line is not None:
                recalculate_line(line)
            left = self.index(row, 0)
            right = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(left, right)
        finally:
            self._recalculating = False

    def _refresh_all_rows(self) -> None:
        if self.rowCount() == 0:
            return
        self.dataChanged.emit(
            self.index(0, 0),
            self.index(self.rowCount() - 1, self.columnCount() - 1),
        )
