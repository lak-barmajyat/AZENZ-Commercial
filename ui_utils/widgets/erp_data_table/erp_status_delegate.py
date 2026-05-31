"""Delegate that paints professional rounded status badges.

Status labels are matched case-insensitively against a customizable color map.
Each entry is a ``(container_color, text_color)`` pair. Parent pages can fully
override the palette via :meth:`ERPDataTable.set_status_colors`.
"""

from __future__ import annotations

from PyQt5.QtCore import QModelIndex, QRectF, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter
from PyQt5.QtWidgets import QStyle, QStyledItemDelegate, QStyleOptionViewItem

# Default badge palette: status label -> (container/background, text color).
DEFAULT_STATUS_COLORS: dict[str, tuple[str, str]] = {
    "non payé": ("#FFDAD6", "#93000A"),
    "impayé": ("#FFDAD6", "#93000A"),
    "payé": ("#D0E1FB", "#0B1C30"),
    "validé": ("#C8E6C9", "#1B5E20"),
    "brouillon": ("#E1E2E4", "#434655"),
    "annulé": ("#F9DEDC", "#BA1A1A"),
    "partiel": ("#FFE4B5", "#8A5300"),
}

# Fallback used when a status value is not present in the color map.
FALLBACK_COLORS: tuple[str, str] = ("#E1E2E4", "#434655")


class ERPStatusDelegate(QStyledItemDelegate):
    """Renders a cell's text as a rounded, colored status badge."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._colors: dict[str, tuple[str, str]] = dict(DEFAULT_STATUS_COLORS)
        self._radius = 10.0
        self._h_padding = 10
        self._v_padding = 3

    def set_colors(self, colors: dict[str, tuple[str, str]]) -> None:
        """Replace/extend the status palette. Keys are matched lowercased."""
        normalized = {str(k).lower(): v for k, v in colors.items()}
        self._colors.update(normalized)

    def _colors_for(self, status: str) -> tuple[str, str]:
        return self._colors.get(status.lower(), FALLBACK_COLORS)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        text = index.data(Qt.DisplayRole)

        # Paint the selection/hover background using the base implementation,
        # but without its text (we draw the badge ourselves).
        style_option = QStyleOptionViewItem(option)
        self.initStyleOption(style_option, index)
        style_option.text = ""
        widget = style_option.widget
        style = widget.style() if widget is not None else QStyle()
        style.drawControl(QStyle.CE_ItemViewItem, style_option, painter, widget)

        if not text or text == "-":
            return

        container_hex, text_hex = self._colors_for(str(text))

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)

        font = QFont(option.font)
        font.setPointSizeF(max(8.0, option.font.pointSizeF() - 0.5))
        font.setBold(True)
        painter.setFont(font)
        metrics = QFontMetrics(font)

        text_width = metrics.horizontalAdvance(str(text))
        text_height = metrics.height()
        badge_width = text_width + self._h_padding * 2
        badge_height = text_height + self._v_padding * 2

        # Center the badge inside the cell rect.
        cell = option.rect
        badge_x = cell.x() + (cell.width() - badge_width) / 2.0
        badge_y = cell.y() + (cell.height() - badge_height) / 2.0
        badge_rect = QRectF(badge_x, badge_y, badge_width, badge_height)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(container_hex))
        painter.drawRoundedRect(badge_rect, self._radius, self._radius)

        painter.setPen(QColor(text_hex))
        painter.drawText(badge_rect, Qt.AlignCenter, str(text))
        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        base = super().sizeHint(option, index)
        return QSize(base.width() + self._h_padding * 2, max(base.height(), 28))
