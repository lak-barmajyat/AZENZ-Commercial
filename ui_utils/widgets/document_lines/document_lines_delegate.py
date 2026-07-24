"""Item delegates for :class:`DocumentLinesWidget`."""

from __future__ import annotations

from PyQt5.QtCore import QEvent, QModelIndex, QRect, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import (
    QAbstractItemDelegate,
    QCompleter,
    QDoubleSpinBox,
    QLineEdit,
    QListView,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QComboBox,
    QWidget,
)

from .document_line import LineType
from .document_line_column import COL_ACTIONS, COL_INDEX, COL_TYPE
from .document_lines_model import IsPlaceholderRole, LineTypeRole


class DocumentLinesTextDelegate(QStyledItemDelegate):
    """Standard single-line text editor."""

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index,
    ) -> QWidget:
        editor = QLineEdit(parent)
        editor.setFrame(False)
        return editor

    def setEditorData(self, editor: QWidget, index) -> None:
        if isinstance(editor, QLineEdit):
            value = index.model().data(index, Qt.EditRole)
            editor.setText("" if value is None else str(value))

    def setModelData(self, editor: QWidget, model, index) -> None:
        if isinstance(editor, QLineEdit):
            model.setData(index, editor.text(), Qt.EditRole)


class DocumentLinesNumericDelegate(QStyledItemDelegate):
    """Numeric editor using a spin box."""

    def __init__(
        self,
        decimals: int = 2,
        minimum: float = 0.0,
        maximum: float = 999_999_999.0,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._decimals = decimals
        self._minimum = minimum
        self._maximum = maximum

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index,
    ) -> QWidget:
        editor = QDoubleSpinBox(parent)
        editor.setFrame(False)
        editor.setDecimals(self._decimals)
        editor.setMinimum(self._minimum)
        editor.setMaximum(self._maximum)
        editor.setButtonSymbols(QDoubleSpinBox.NoButtons)
        editor.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        return editor

    def setEditorData(self, editor: QWidget, index) -> None:
        if isinstance(editor, QDoubleSpinBox):
            value = index.model().data(index, Qt.EditRole)
            try:
                editor.setValue(float(value or 0))
            except (TypeError, ValueError):
                editor.setValue(0.0)

    def setModelData(self, editor: QWidget, model, index) -> None:
        if isinstance(editor, QDoubleSpinBox):
            model.setData(index, editor.value(), Qt.EditRole)


class DocumentLinesComboDelegate(QStyledItemDelegate):
    """Combo box editor for enumerated values such as units."""

    def __init__(self, options: list[str] | None = None, parent=None) -> None:
        super().__init__(parent)
        self._options = options or ["Unit"]

    def set_options(self, options: list[str]) -> None:
        self._options = list(options) if options else ["Unit"]

    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index,
    ) -> QWidget:
        editor = QComboBox(parent)
        editor.setFrame(False)
        editor.addItems(self._options)
        return editor

    def setEditorData(self, editor: QWidget, index) -> None:
        if isinstance(editor, QComboBox):
            value = str(index.model().data(index, Qt.EditRole) or "")
            idx = editor.findText(value)
            editor.setCurrentIndex(max(idx, 0))

    def setModelData(self, editor: QWidget, model, index) -> None:
        if isinstance(editor, QComboBox):
            model.setData(index, editor.currentText(), Qt.EditRole)


class DocumentLinesSearchDelegate(QStyledItemDelegate):
    """Description/reference column editor with article search on the placeholder row.

    On the placeholder/search row the editor is a :class:`QLineEdit` backed by a
    :class:`QCompleter`. It works like a live database search box:

    * ``searchTextChanged(str)`` fires as the user types so the controller can
      query the database (by reference or article name).
    * The controller pushes results back into the shared completer model.
    * ``articleChosen(int)`` fires with the index of the selected suggestion
      (into the controller-provided results list) when the user picks one.

    On normal product/text rows the editor is a plain single-line text editor,
    so in-place editing keeps working everywhere else.
    """

    searchTextChanged = pyqtSignal(str)
    articleChosen = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._completer_model = None
        self._placeholder_text = "Search or type article..."
        self._active_editor: QLineEdit | None = None

    # -- configuration ------------------------------------------------- #
    def set_completer_model(self, model) -> None:
        self._completer_model = model

    def set_placeholder_text(self, text: str) -> None:
        self._placeholder_text = text or ""

    def active_editor(self) -> QLineEdit | None:
        return self._active_editor

    # -- editor lifecycle ---------------------------------------------- #
    def createEditor(
        self,
        parent: QWidget,
        option: QStyleOptionViewItem,
        index,
    ) -> QWidget:
        editor = QLineEdit(parent)
        editor.setFrame(False)

        if bool(index.data(IsPlaceholderRole)):
            editor.setPlaceholderText(self._placeholder_text)
            editor.setClearButtonEnabled(True)
            if self._completer_model is not None:
                completer = QCompleter(self._completer_model, editor)
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                completer.setFilterMode(Qt.MatchContains)
                completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
                popup = QListView()
                popup.setObjectName("DocumentLinesSearchPopup")
                completer.setPopup(popup)
                editor.setCompleter(completer)
                completer.activated[QModelIndex].connect(
                    lambda idx, ed=editor: self._on_completion_activated(ed, idx)
                )
            editor.textEdited.connect(self.searchTextChanged.emit)
            self._active_editor = editor
            editor.destroyed.connect(self._on_editor_destroyed)
        return editor

    def setEditorData(self, editor: QWidget, index) -> None:
        if isinstance(editor, QLineEdit):
            value = index.model().data(index, Qt.EditRole)
            editor.setText("" if value is None else str(value))

    def setModelData(self, editor: QWidget, model, index) -> None:
        if isinstance(editor, QLineEdit):
            model.setData(index, editor.text(), Qt.EditRole)

    # -- internal ------------------------------------------------------ #
    def _on_completion_activated(self, editor: QLineEdit, proxy_index) -> None:
        # ``QCompleter`` exposes the source row via the completion model role.
        completer = editor.completer()
        source_row = proxy_index.row()
        if completer is not None:
            mapped = completer.completionModel().mapToSource(proxy_index)
            if mapped.isValid():
                source_row = mapped.row()
        # Cancel the in-cell edit so the raw text is not written to the line,
        # then let the widget turn the chosen article into a product line.
        self.closeEditor.emit(editor, QAbstractItemDelegate.RevertModelCache)
        self.articleChosen.emit(source_row)

    def _on_editor_destroyed(self, *_args) -> None:
        self._active_editor = None


class DocumentLinesTypeDelegate(QStyledItemDelegate):
    """Paints a small icon for the line type column."""

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index,
    ) -> None:
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        is_placeholder = bool(index.data(IsPlaceholderRole))
        line_type = index.data(LineTypeRole)

        rect = option.rect.adjusted(0, 0, 0, -1)
        center_x = rect.center().x()
        center_y = rect.center().y()

        if is_placeholder:
            self._paint_plus_circle(painter, center_x, center_y)
        elif line_type == LineType.TEXT:
            self._paint_text_icon(painter, center_x, center_y)
        elif line_type == LineType.SEPARATOR:
            self._paint_separator_icon(painter, rect)
        else:
            self._paint_product_icon(painter, center_x, center_y)

        painter.restore()

    def _paint_product_icon(self, painter: QPainter, cx: int, cy: int) -> None:
        pen = QPen(QColor("#434655"))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(QColor("#F3F4F6"))
        painter.drawRoundedRect(cx - 8, cy - 7, 16, 14, 2, 2)
        painter.drawLine(cx - 5, cy - 2, cx + 5, cy - 2)

    def _paint_text_icon(self, painter: QPainter, cx: int, cy: int) -> None:
        pen = QPen(QColor("#9CA3AF"))
        pen.setWidth(2)
        painter.setPen(pen)
        for offset in (-4, 0, 4):
            painter.drawLine(cx - 6, cy + offset, cx + 6, cy + offset)

    def _paint_separator_icon(self, painter: QPainter, rect: QRect) -> None:
        pen = QPen(QColor("#C3C5D8"))
        pen.setWidth(1)
        painter.setPen(pen)
        y = rect.center().y()
        painter.drawLine(rect.left() + 8, y, rect.right() - 8, y)

    def _paint_plus_circle(self, painter: QPainter, cx: int, cy: int) -> None:
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#EFF4FF"))
        painter.drawEllipse(cx - 10, cy - 10, 20, 20)
        pen = QPen(QColor("#0051DF"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(cx - 4, cy, cx + 4, cy)
        painter.drawLine(cx, cy - 4, cx, cy + 4)


class DocumentLinesIndexDelegate(QStyledItemDelegate):
    """Paints row index; placeholder row shows ``*``."""

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index,
    ) -> None:
        painter.save()
        text = str(index.data(Qt.DisplayRole) or "")
        is_placeholder = bool(index.data(IsPlaceholderRole))

        if is_placeholder:
            color = QColor("#9CA3AF")
            font = QFont(option.font)
            font.setItalic(True)
            painter.setFont(font)
        else:
            color = QColor("#434655")

        painter.setPen(color)
        rect = option.rect.adjusted(4, 0, -4, 0)
        painter.drawText(rect, int(Qt.AlignCenter), text)
        painter.restore()


class DocumentLinesActionsDelegate(QStyledItemDelegate):
    """Action column with an add button on the placeholder row.

    Emits ``actionTriggered(str, int)`` with action name and row index.
    """

    actionTriggered = pyqtSignal(str, int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._hover_row: int | None = None

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index,
    ) -> None:
        if not bool(index.data(IsPlaceholderRole)):
            return

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        rect = option.rect.adjusted(6, 6, -6, -6)
        color = QColor("#0051DF")
        if option.state & QStyle.State_MouseOver:
            color = QColor("#003FB0")

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawRoundedRect(rect, 4, 4)

        pen = QPen(QColor("#FFFFFF"))
        pen.setWidth(2)
        painter.setPen(pen)
        cx, cy = rect.center().x(), rect.center().y()
        painter.drawLine(cx - 4, cy, cx + 4, cy)
        painter.drawLine(cx, cy - 4, cx, cy + 4)
        painter.restore()

    def editorEvent(
        self,
        event: QEvent,
        model,
        option: QStyleOptionViewItem,
        index,
    ) -> bool:
        if not bool(index.data(IsPlaceholderRole)):
            return False

        if event.type() == QEvent.MouseButtonRelease:
            self.actionTriggered.emit("add_from_placeholder", index.row())
            return True
        return False

    def sizeHint(
        self,
        option: QStyleOptionViewItem,
        index,
    ) -> QSize:
        return QSize(44, 36)
