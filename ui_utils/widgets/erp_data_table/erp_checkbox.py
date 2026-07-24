"""Checkbox-column helpers for :class:`ERPDataTable`.

The checkbox column is *selection-driven*: a row's checkbox is checked when the
row is selected in the view's selection model, and toggling it toggles the
row's selection. This keeps a single source of truth, so native ``Ctrl`` /
``Shift`` multi-selection and the checkboxes always stay in sync.

This module provides:
    * :class:`ERPCheckboxDelegate` - paints the per-row checkbox indicator.
    * :class:`ERPCheckHeaderView`  - a header view that paints a tri-state
      "select all" checkbox in the first section and emits ``toggled`` when it
      is clicked.
"""

from __future__ import annotations

from PyQt5.QtCore import QEvent, QRect, QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QHeaderView,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionButton,
    QStyleOptionViewItem,
)

# Default fixed width of the checkbox column.
CHECKBOX_COLUMN_WIDTH = 44


def _indicator_size(style: QStyle, widget) -> QSize:
    width = style.pixelMetric(QStyle.PM_IndicatorWidth, None, widget)
    height = style.pixelMetric(QStyle.PM_IndicatorHeight, None, widget)
    return QSize(width or 16, height or 16)


def _centered_indicator_rect(rect: QRect, size: QSize) -> QRect:
    x = rect.x() + (rect.width() - size.width()) // 2
    y = rect.y() + (rect.height() - size.height()) // 2
    return QRect(x, y, size.width(), size.height())


class ERPCheckboxDelegate(QStyledItemDelegate):
    """Paints a centered checkbox reflecting the row's selection state."""

    def paint(self, painter, option, index) -> None:
        # Draw the cell background (incl. selection/hover highlight) but no text.
        style_option = QStyleOptionViewItem(option)
        self.initStyleOption(style_option, index)
        style_option.text = ""
        widget = style_option.widget
        style = widget.style() if widget is not None else QApplication.style()
        style.drawControl(QStyle.CE_ItemViewItem, style_option, painter, widget)

        checked = bool(option.state & QStyle.State_Selected)

        check_option = QStyleOptionButton()
        check_option.state = QStyle.State_Enabled
        check_option.state |= QStyle.State_On if checked else QStyle.State_Off
        check_option.rect = _centered_indicator_rect(
            option.rect, _indicator_size(style, widget)
        )
        style.drawPrimitive(
            QStyle.PE_IndicatorCheckBox, check_option, painter, widget
        )

    def editorEvent(self, event, model, option, index) -> bool:
        # Toggling is handled at the view level (so it cooperates with the
        # selection model); never enter an editor here.
        return False

    def sizeHint(self, option, index) -> QSize:
        return QSize(CHECKBOX_COLUMN_WIDTH, 30)


class ERPCheckHeaderView(QHeaderView):
    """Horizontal header with a tri-state checkbox in its first section.

    Emits :pyattr:`toggled` (``bool`` -> desired "all checked" state) when the
    checkbox is clicked. The owning widget decides how to apply it to the
    selection model and pushes the resulting state back via
    :meth:`set_check_state`.
    """

    toggled = pyqtSignal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__(Qt.Horizontal, parent)
        self._check_state = Qt.Unchecked
        self._checkbox_enabled = True
        self.setSectionsClickable(True)
        self.setHighlightSections(False)

    def set_checkbox_enabled(self, enabled: bool) -> None:
        self._checkbox_enabled = enabled
        if self.count():
            self.updateSection(0)

    def set_check_state(self, state: Qt.CheckState) -> None:
        if state != self._check_state:
            self._check_state = state
            if self.count():
                self.updateSection(0)

    def paintSection(self, painter, rect, logical_index) -> None:
        super().paintSection(painter, rect, logical_index)
        if logical_index != 0 or not self._checkbox_enabled:
            return

        style = self.style()
        check_option = QStyleOptionButton()
        check_option.state = QStyle.State_Enabled
        if self._check_state == Qt.Checked:
            check_option.state |= QStyle.State_On
        elif self._check_state == Qt.PartiallyChecked:
            check_option.state |= QStyle.State_NoChange
        else:
            check_option.state |= QStyle.State_Off
        check_option.rect = _centered_indicator_rect(
            rect, _indicator_size(style, self)
        )
        style.drawPrimitive(
            QStyle.PE_IndicatorCheckBox, check_option, painter, self
        )

    def mousePressEvent(self, event) -> None:
        if self._checkbox_enabled and self.logicalIndexAt(event.pos()) == 0:
            # Consume the press so the section is not sorted; request a toggle.
            want_checked = self._check_state != Qt.Checked
            self.toggled.emit(want_checked)
            event.accept()
            return
        super().mousePressEvent(event)
