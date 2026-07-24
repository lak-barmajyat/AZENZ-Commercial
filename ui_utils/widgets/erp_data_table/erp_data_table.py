"""ERPDataTable - a reusable, page-agnostic ERP table widget.

This widget wraps a :class:`QTableView` + :class:`ERPTableModel` and provides a
clean public API for ERP list pages (Liste Ventes, Liste Clients, Liste
Articles, Liste Paiements, Liste Stock, Liste Fournisseurs, ...). It contains
**no** business logic, database access, or page-specific code: pages configure
it with columns + rows and listen to its signals.

------------------------------------------------------------------------------
Qt Designer "Promote to..." instructions
------------------------------------------------------------------------------
1. Drop a plain ``QWidget`` onto your form where the table should appear.
2. Right-click it -> "Promote to...".
3. Fill in:
       Promoted class name : ERPDataTable
       Header file         : ui_utils.widgets.erp_data_table.erp_data_table
4. Click "Add", then "Promote".

Because Qt Designer cannot pass constructor arguments, ``ERPDataTable`` has a
plain ``__init__(self, parent=None)`` signature and starts empty. Configure it
later in code via ``set_columns(...)`` / ``set_rows(...)``.
"""

from __future__ import annotations

import os
from typing import Any, Callable

from PyQt5.QtCore import (
    QEvent,
    QItemSelection,
    QItemSelectionModel,
    QModelIndex,
    QPoint,
    QSortFilterProxyModel,
    Qt,
    pyqtSignal,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMenu,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .erp_checkbox import (
    CHECKBOX_COLUMN_WIDTH,
    ERPCheckboxDelegate,
    ERPCheckHeaderView,
)
from .erp_status_delegate import ERPStatusDelegate
from .erp_table_column import ERPTableColumn
from .erp_table_model import RawValueRole, ERPTableModel

_QSS_PATH = os.path.join(os.path.dirname(__file__), "erp_table_styles.qss")


class ERPDataTable(QWidget):
    """Reusable ERP data table built on QTableView + QAbstractTableModel.

    Signals:
        rowClicked(dict): Emitted with the row dict when a row is clicked.
        rowDoubleClicked(dict): Emitted with the row dict on double click.
        selectionChangedData(dict): Emitted with the current (last) selected
            row when the selection changes.
        selectionChangedRows(list): Emitted with the full list of selected row
            dicts (i.e. the checked rows) whenever the selection changes.
        contextMenuRequested(dict, QPoint): Emitted on right-click.
        cellClicked(dict, str): Emitted with (row, column_key) on cell click.
        linkClicked(dict, str): Emitted with (row, column_key) when a link
            column cell is clicked.
        refreshRequested(): Emitted when the footer refresh button is clicked.
    """

    rowClicked = pyqtSignal(dict)
    rowDoubleClicked = pyqtSignal(dict)
    selectionChangedData = pyqtSignal(dict)
    selectionChangedRows = pyqtSignal(list)
    contextMenuRequested = pyqtSignal(dict, QPoint)
    cellClicked = pyqtSignal(dict, str)
    linkClicked = pyqtSignal(dict, str)
    refreshRequested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._columns: list[ERPTableColumn] = []
        # Checkbox selection column is shown first by default.
        self._checkbox_enabled = True
        self._context_actions: list[dict] = []
        self._syncing_header = False

        # --- Models -------------------------------------------------------
        self._model = ERPTableModel(self)
        self._model.set_checkbox_enabled(True)
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setSourceModel(self._model)
        self._proxy.setSortRole(RawValueRole)
        self._proxy.setDynamicSortFilter(False)

        # --- View ---------------------------------------------------------
        self._view = QTableView(self)
        self._view.setModel(self._proxy)
        self._view.setObjectName("ERPTableView")
        self._view.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Extended selection enables native Ctrl / Shift multi-selection.
        self._view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._view.setAlternatingRowColors(True)
        self._view.setShowGrid(False)
        self._view.setWordWrap(False)
        self._view.setMouseTracking(True)
        self._view.verticalHeader().setVisible(False)
        self._view.verticalHeader().setDefaultSectionSize(40)

        # Custom header paints the "select all" tri-state checkbox.
        self._header = ERPCheckHeaderView(self._view)
        self._view.setHorizontalHeader(self._header)
        self._header.setVisible(True)
        self._header.setHighlightSections(False)
        self._header.setSectionsClickable(True)
        self._header.setStretchLastSection(False)
        self._header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._header.set_checkbox_enabled(True)
        self._header.toggled.connect(self._on_header_toggled)

        # Enable sorting after installing the custom header so the sort
        # signals are wired to it.
        self._view.setSortingEnabled(True)

        self._view.setContextMenuPolicy(Qt.CustomContextMenu)
        self._view.viewport().installEventFilter(self)

        # --- Delegates ----------------------------------------------------
        self._status_delegate = ERPStatusDelegate(self._view)
        self._checkbox_delegate = ERPCheckboxDelegate(self._view)

        # --- Empty-state overlay -----------------------------------------
        self._empty_label = QLabel(
            "Aucune donnée disponible", self._view.viewport()
        )
        self._empty_label.setObjectName("ERPTableEmptyLabel")
        self._empty_label.setAlignment(Qt.AlignCenter)
        self._empty_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self._empty_label.hide()

        # --- Footer / status bar -----------------------------------------
        self._footer = self._build_footer()

        # --- Layout -------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._view)
        layout.addWidget(self._footer)

        # --- Wiring -------------------------------------------------------
        self._view.clicked.connect(self._on_clicked)
        self._view.doubleClicked.connect(self._on_double_clicked)
        self._view.customContextMenuRequested.connect(self._on_context_menu)
        selection_model = self._view.selectionModel()
        if selection_model is not None:
            selection_model.selectionChanged.connect(
                self._on_selection_changed
            )
        self._model.modelReset.connect(self._update_empty_state)
        self._model.modelReset.connect(self._sync_header_check_state)
        self._model.modelReset.connect(self._update_footer)
        self._model.rowsInserted.connect(self._update_empty_state)
        self._model.rowsInserted.connect(self._update_footer)
        self._model.rowsRemoved.connect(self._update_empty_state)
        self._model.rowsRemoved.connect(self._update_footer)

        self._load_stylesheet()
        self._update_empty_state()
        self._sync_header_check_state()
        self._update_footer()

    # ====================================================================== #
    # Public API                                                             #
    # ====================================================================== #
    def set_columns(self, columns: list[ERPTableColumn]) -> None:
        """Define the columns. Can be called any time after construction."""
        self._columns = [c for c in columns if c.visible]
        self._model.set_columns(self._columns)
        self._configure_header()
        self._configure_delegates()
        self._update_empty_state()

    def set_rows(self, rows: list[dict]) -> None:
        """Replace all rows."""
        self._model.set_rows(rows)
        self._update_empty_state()

    def append_row(self, row: dict) -> None:
        self._model.append_row(row)
        self._update_empty_state()

    def update_row(self, row_index: int, row: dict) -> None:
        self._model.update_row(row_index, row)

    def remove_selected_row(self) -> None:
        index = self.selected_row_index()
        if index is not None:
            self._model.remove_row(index)
            self._update_empty_state()

    def clear(self) -> None:
        self._model.clear()
        self._update_empty_state()

    def selected_row(self) -> dict | None:
        index = self.selected_row_index()
        if index is None:
            return None
        return self._model.get_row(index)

    def selected_rows(self) -> list[dict]:
        rows: list[dict] = []
        selection_model = self._view.selectionModel()
        if selection_model is None:
            return rows
        for proxy_index in selection_model.selectedRows():
            source_index = self._proxy.mapToSource(proxy_index)
            row = self._model.get_row(source_index.row())
            if row is not None:
                rows.append(row)
        return rows

    def selected_row_index(self) -> int | None:
        """Returns the *source* (data) row index of the current selection."""
        selection_model = self._view.selectionModel()
        if selection_model is None:
            return None
        indexes = selection_model.selectedRows()
        if not indexes:
            current = self._view.currentIndex()
            if not current.isValid():
                return None
            return self._proxy.mapToSource(current).row()
        return self._proxy.mapToSource(indexes[0]).row()

    def refresh(self) -> None:
        """Force a repaint/relayout of the view."""
        self._view.viewport().update()
        self._update_empty_state()

    def set_empty_text(self, text: str) -> None:
        self._empty_label.setText(text)

    def set_status_colors(self, colors: dict) -> None:
        """Customize the status badge palette (see ERPStatusDelegate)."""
        self._status_delegate.set_colors(colors)
        self._view.viewport().update()

    def enable_checkbox_column(self, enabled: bool) -> None:
        """Show/hide the leading checkbox selection column (shown by default).

        The checkbox column is selection-driven: each row's checkbox reflects
        whether the row is selected, and clicking it toggles that row. When
        enabled, the view uses extended selection so ``Ctrl`` / ``Shift``
        multi-selection works; when disabled it falls back to single
        selection.
        """
        self._checkbox_enabled = enabled
        self._model.set_checkbox_enabled(enabled)
        self._header.set_checkbox_enabled(enabled)
        self._view.setSelectionMode(
            QAbstractItemView.ExtendedSelection
            if enabled
            else QAbstractItemView.SingleSelection
        )
        self._configure_header()
        self._configure_delegates()
        self._sync_header_check_state()

    def check_all(self) -> None:
        """Select (check) every row."""
        self._select_all_rows(True)

    def clear_selection(self) -> None:
        """Deselect (uncheck) every row."""
        selection_model = self._view.selectionModel()
        if selection_model is not None:
            selection_model.clearSelection()

    def checked_rows(self) -> list[dict]:
        """Alias of :meth:`selected_rows` (the checked rows)."""
        return self.selected_rows()

    def set_footer_visible(self, visible: bool) -> None:
        """Show/hide the bottom status bar (counts + refresh button)."""
        self._footer.setVisible(visible)
        self._apply_footer_corner_style(visible)

    def set_refresh_button_text(self, text: str) -> None:
        self._refresh_button.setText(text)

    def set_refresh_button_icon(self, icon: QIcon) -> None:
        self._refresh_button.setIcon(icon)

    def row_count(self) -> int:
        """Total number of rows currently in the table."""
        return self._model.rowCount()

    def selected_count(self) -> int:
        """Number of currently selected (checked) rows."""
        selection_model = self._view.selectionModel()
        if selection_model is None:
            return 0
        return len(selection_model.selectedRows())

    def set_context_menu_actions(self, actions: list[dict]) -> None:
        """Provide a default context menu.

        Each action is a dict: ``{"text": str, "icon": str | QIcon | None,
        "callback": Callable[[dict], None]}``. The callback receives the row
        dict that was right-clicked. Pages that need richer behavior can
        instead listen to the ``contextMenuRequested`` signal.
        """
        self._context_actions = actions or []

    # ------------------------------------------------------------------ #
    # Extra configuration helpers (optional, still generic)              #
    # ------------------------------------------------------------------ #
    def set_selection_mode(
        self, mode: QAbstractItemView.SelectionMode
    ) -> None:
        self._view.setSelectionMode(mode)

    def view(self) -> QTableView:
        """Expose the underlying view for advanced/rare customizations."""
        return self._view

    def model(self) -> ERPTableModel:
        return self._model

    # ====================================================================== #
    # Internal helpers                                                       #
    # ====================================================================== #
    def _load_stylesheet(self) -> None:
        try:
            with open(_QSS_PATH, "r", encoding="utf-8") as handle:
                self.setStyleSheet(handle.read())
        except OSError:
            # Styling is non-critical; the widget still works unstyled.
            pass
        # Square off the table's bottom corners so it meets the footer cleanly.
        self._apply_footer_corner_style(True)

    def _build_footer(self) -> QFrame:
        footer = QFrame(self)
        footer.setObjectName("ERPTableFooter")

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(12, 6, 12, 6)
        footer_layout.setSpacing(18)

        self._rows_label = QLabel(footer)
        self._rows_label.setObjectName("ERPTableFooterLabel")
        self._selected_label = QLabel(footer)
        self._selected_label.setObjectName("ERPTableFooterLabel")

        self._refresh_button = QPushButton("Actualiser", footer)
        self._refresh_button.setObjectName("ERPTableRefreshButton")
        self._refresh_button.setCursor(Qt.PointingHandCursor)
        self._refresh_button.setFocusPolicy(Qt.NoFocus)
        self._refresh_button.clicked.connect(self.refreshRequested.emit)

        footer_layout.addWidget(self._rows_label)
        footer_layout.addWidget(self._selected_label)
        footer_layout.addStretch(1)
        footer_layout.addWidget(self._refresh_button)
        return footer

    def _update_footer(self, *args: Any) -> None:
        total = self._model.rowCount()
        selected = self.selected_count()
        self._rows_label.setText(f"Total : {total}")
        self._selected_label.setText(f"Sélection : {selected}")

    def _apply_footer_corner_style(self, footer_visible: bool) -> None:
        # Toggle a dynamic property the QSS uses to round the table's bottom
        # corners only when the footer is hidden.
        self._view.setProperty("footer", "true" if footer_visible else "false")
        self._view.style().unpolish(self._view)
        self._view.style().polish(self._view)

    def _configure_header(self) -> None:
        header = self._view.horizontalHeader()
        header.setMinimumSectionSize(30)
        offset = self._model.column_offset()

        if offset:
            header.setSectionResizeMode(0, QHeaderView.Fixed)
            self._view.setColumnWidth(0, CHECKBOX_COLUMN_WIDTH)

        for data_index, column in enumerate(self._columns):
            model_index = data_index + offset
            if column.stretch:
                header.setSectionResizeMode(model_index, QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(
                    model_index, QHeaderView.Interactive
                )
                self._view.setColumnWidth(model_index, column.width)

    def _configure_delegates(self) -> None:
        offset = self._model.column_offset()
        if offset:
            self._view.setItemDelegateForColumn(0, self._checkbox_delegate)
        for data_index, column in enumerate(self._columns):
            model_index = data_index + offset
            if column.is_status:
                self._view.setItemDelegateForColumn(
                    model_index, self._status_delegate
                )
            else:
                self._view.setItemDelegateForColumn(model_index, None)

    def _column_at(self, column_index: int) -> ERPTableColumn | None:
        data_col = column_index - self._model.column_offset()
        if 0 <= data_col < len(self._columns):
            return self._columns[data_col]
        return None

    def _row_dict_from_proxy(self, proxy_index: QModelIndex) -> dict | None:
        source_index = self._proxy.mapToSource(proxy_index)
        return self._model.get_row(source_index.row())

    def _update_empty_state(self, *args: Any) -> None:
        is_empty = self._model.rowCount() == 0
        if is_empty:
            self._empty_label.resize(self._view.viewport().size())
            self._empty_label.move(0, 0)
            self._empty_label.show()
            self._empty_label.raise_()
        else:
            self._empty_label.hide()

    # ------------------------------------------------------------------ #
    # Event handlers                                                     #
    # ------------------------------------------------------------------ #
    def _on_clicked(self, proxy_index: QModelIndex) -> None:
        row = self._row_dict_from_proxy(proxy_index)
        if row is None:
            return
        self.rowClicked.emit(row)
        column = self._column_at(proxy_index.column())
        if column is not None:
            self.cellClicked.emit(row, column.key)
            if column.is_link:
                self.linkClicked.emit(row, column.key)

    def _on_double_clicked(self, proxy_index: QModelIndex) -> None:
        row = self._row_dict_from_proxy(proxy_index)
        if row is not None:
            self.rowDoubleClicked.emit(row)

    def _on_selection_changed(
        self, selected: QItemSelection, deselected: QItemSelection
    ) -> None:
        self._sync_header_check_state()
        self._update_footer()
        self.selectionChangedRows.emit(self.selected_rows())
        row = self.selected_row()
        if row is not None:
            self.selectionChangedData.emit(row)

    # ------------------------------------------------------------------ #
    # Checkbox / multi-selection helpers                                 #
    # ------------------------------------------------------------------ #
    def eventFilter(self, obj, event):  # noqa: N802 (Qt naming)
        if (
            obj is self._view.viewport()
            and event.type() == QEvent.MouseButtonPress
            and event.button() == Qt.LeftButton
            and self._model.column_offset()
        ):
            proxy_index = self._view.indexAt(event.pos())
            if proxy_index.isValid() and proxy_index.column() == 0:
                # Toggle just this row's selection (like a checkbox), without
                # clearing the rest of the multi-selection.
                self._toggle_row_selection(proxy_index.row())
                return True
        return super().eventFilter(obj, event)

    def _row_selection(self, proxy_row: int) -> QItemSelection:
        last_col = max(0, self._proxy.columnCount() - 1)
        left = self._proxy.index(proxy_row, 0)
        right = self._proxy.index(proxy_row, last_col)
        return QItemSelection(left, right)

    def _toggle_row_selection(self, proxy_row: int) -> None:
        selection_model = self._view.selectionModel()
        if selection_model is None:
            return
        selection_model.select(
            self._row_selection(proxy_row),
            QItemSelectionModel.Toggle | QItemSelectionModel.Rows,
        )
        selection_model.setCurrentIndex(
            self._proxy.index(proxy_row, 0),
            QItemSelectionModel.NoUpdate,
        )

    def _select_all_rows(self, select: bool) -> None:
        selection_model = self._view.selectionModel()
        if selection_model is None:
            return
        if not select:
            selection_model.clearSelection()
            return
        row_count = self._proxy.rowCount()
        if row_count == 0:
            return
        last_col = max(0, self._proxy.columnCount() - 1)
        whole = QItemSelection(
            self._proxy.index(0, 0),
            self._proxy.index(row_count - 1, last_col),
        )
        selection_model.select(
            whole, QItemSelectionModel.Select | QItemSelectionModel.Rows
        )

    def _on_header_toggled(self, want_checked: bool) -> None:
        self._select_all_rows(want_checked)

    def _sync_header_check_state(self, *args: Any) -> None:
        if self._syncing_header:
            return
        self._syncing_header = True
        try:
            total = self._proxy.rowCount()
            selection_model = self._view.selectionModel()
            selected = (
                len(selection_model.selectedRows())
                if selection_model is not None
                else 0
            )
            if total == 0 or selected == 0:
                state = Qt.Unchecked
            elif selected >= total:
                state = Qt.Checked
            else:
                state = Qt.PartiallyChecked
            self._header.set_check_state(state)
        finally:
            self._syncing_header = False

    def _on_context_menu(self, pos: QPoint) -> None:
        proxy_index = self._view.indexAt(pos)
        row = None
        if proxy_index.isValid():
            row = self._row_dict_from_proxy(proxy_index)
        global_pos = self._view.viewport().mapToGlobal(pos)

        # Always notify listeners so pages can build fully custom menus.
        self.contextMenuRequested.emit(row or {}, global_pos)

        if not self._context_actions or row is None:
            return

        menu = QMenu(self)
        for action_def in self._context_actions:
            text = action_def.get("text", "")
            if text == "-" or action_def.get("separator"):
                menu.addSeparator()
                continue
            action = menu.addAction(text)
            icon = action_def.get("icon")
            if isinstance(icon, QIcon):
                action.setIcon(icon)
            elif isinstance(icon, str) and icon:
                action.setIcon(QIcon(icon))
            callback: Callable[[dict], None] | None = (
                action_def.get("callback")
            )
            if callback is not None:
                action.triggered.connect(
                    lambda _checked=False, cb=callback, r=row: cb(r)
                )
        menu.exec_(global_pos)

    # Keep the empty-state overlay sized with the viewport.
    def resizeEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        super().resizeEvent(event)
        self._update_empty_state()
