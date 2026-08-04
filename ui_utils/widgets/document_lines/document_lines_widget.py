"""DocumentLinesWidget - reusable editable document lines table for ERP documents.

Qt Designer promotion::

    Promoted class name : DocumentLinesWidget
    Header file         : ui_utils.widgets.document_lines.document_lines_widget
"""

from __future__ import annotations

import os
from collections import deque
from collections.abc import Iterable, Mapping
from types import MappingProxyType
from typing import Any, Callable

from PyQt5.QtCore import (
    QEvent,
    QModelIndex,
    QPoint,
    QSettings,
    QStringListModel,
    Qt,
    QTimer,
    pyqtSignal,
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QMenu,
    QPushButton,
    QScrollArea,
    QShortcut,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .calculations import DocumentTotals, recalculate_document_totals, recalculate_line
from .document_line import DocumentLine, LineType
from .document_line_column import (
    COL_ACTIONS,
    COL_INDEX,
    COL_TYPE,
    ColumnEditorType,
    DocumentLineColumn,
    default_columns,
)
from .document_lines_delegate import (
    DocumentLinesActionsDelegate,
    DocumentLinesComboDelegate,
    DocumentLinesIndexDelegate,
    DocumentLinesNumericDelegate,
    DocumentLinesSearchDelegate,
    DocumentLinesTextDelegate,
    DocumentLinesTypeDelegate,
)
from .document_lines_model import DocumentLinesModel

_QSS_PATH = os.path.join(os.path.dirname(__file__), "document_lines_styles.qss")


class _ColumnSettingsDialog(QDialog):
    """Small column chooser used by :class:`DocumentLinesWidget`."""

    def __init__(self, columns, defaults, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Background")
        self.setWindowTitle("Visible columns")
        self.setModal(True)
        self.resize(340, 430)
        self._checks: dict[str, QCheckBox] = {}
        self._defaults = dict(defaults)
        self._load_stylesheet()

        layout = QVBoxLayout(self)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        content = QWidget(scroll)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(8, 8, 8, 8)
        for column in columns:
            check = QCheckBox(column.title or column.key, content)
            check.setChecked(column.visible)
            check.setToolTip(column.key)
            check.toggled.connect(self._update_apply_state)
            self._checks[column.key] = check
            content_layout.addWidget(check)
        content_layout.addStretch(1)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        quick_actions = QHBoxLayout()
        select_all = QPushButton("Select all", self)
        select_all.setProperty("class", "outlined")
        select_all.clicked.connect(
            lambda: self._set_all_checked(True)
        )
        quick_actions.addWidget(select_all)
        quick_actions.addStretch(1)
        layout.addLayout(quick_actions)

        self._buttons = QDialogButtonBox(
            QDialogButtonBox.Reset
            | QDialogButtonBox.Apply
            | QDialogButtonBox.Cancel,
            parent=self,
        )
        self._buttons.rejected.connect(self.reject)
        apply_button = self._buttons.button(QDialogButtonBox.Apply)
        reset_button = self._buttons.button(QDialogButtonBox.Reset)
        cancel_button = self._buttons.button(QDialogButtonBox.Cancel)
        apply_button.setProperty("class", "primary")
        reset_button.setProperty("class", "outlined")
        cancel_button.setProperty("class", "outlined")
        apply_button.clicked.connect(self.accept)
        reset_button.clicked.connect(
            self._reset_defaults
        )
        layout.addWidget(self._buttons)
        self._update_apply_state()

    def selected_columns(self) -> list[str]:
        return [key for key, check in self._checks.items() if check.isChecked()]

    def _set_all_checked(self, checked: bool) -> None:
        for check in self._checks.values():
            check.setChecked(checked)

    def _reset_defaults(self) -> None:
        for key, check in self._checks.items():
            check.setChecked(self._defaults.get(key, True))

    def _update_apply_state(self) -> None:
        apply_button = self._buttons.button(QDialogButtonBox.Apply)
        if apply_button is not None:
            apply_button.setEnabled(any(c.isChecked() for c in self._checks.values()))

    def _load_stylesheet(self) -> None:
        try:
            with open(_QSS_PATH, encoding="utf-8") as fh:
                self.setStyleSheet(fh.read())
        except OSError:
            pass

class DocumentLinesWidget(QWidget):
    """Reusable editable document lines table.

    Signals:
        lineAdded(DocumentLine, int): A real line was inserted.
        lineRemoved(DocumentLine, int): A real line was removed.
        lineChanged(DocumentLine, int): A real line was edited or recalculated.
        lineSelected(DocumentLine, int): Selection moved to a real line.
        totalsChanged(dict): Document totals were recomputed.
        columnUpdateFailed(int, str, str, str): A dependency callback failed;
            arguments are row, source column, rule name, and error message.
        articleSearchRequested(str): User typed in the placeholder row.
        barcodeScanRequested(): Toolbar / shortcut requested barcode scan.
        stockCheckRequested(): Toolbar / shortcut requested stock check.
    """

    lineAdded = pyqtSignal(object, int)
    lineRemoved = pyqtSignal(object, int)
    lineChanged = pyqtSignal(object, int)
    lineSelected = pyqtSignal(object, int)
    totalsChanged = pyqtSignal(dict)
    columnUpdateFailed = pyqtSignal(int, str, str, str)
    columnVisibilityChanged = pyqtSignal(list)
    articleSearchRequested = pyqtSignal(str)
    articleCodeSubmitted = pyqtSignal(str)
    barcodeScanRequested = pyqtSignal()
    stockCheckRequested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("DocumentLinesWidget")

        self._columns: list[DocumentLineColumn] = default_columns()
        self._default_column_visibility = {
            column.key: column.visible for column in self._columns
        }
        self._column_settings_key: str | None = None
        self._feature_hidden_columns: set[str] = set()
        self._editable = True
        self._read_only = False
        self._tax_enabled = True
        self._discount_enabled = True
        self._default_vat_percent = 20.0
        self._default_unit = "Unit"
        self._units: list[str] = ["Unit", "Kg", "L", "m", "h"]
        self._vat_rates: list[float] = [0.0, 5.5, 10.0, 20.0]
        self._currency_symbol = ""
        self._number_decimals = 2
        self._thousands_sep = " "
        self._validation_rules: list[Callable[[DocumentLine, int], str | None]] = []
        self._emitting_totals = False
        self._placeholder_search_connected = False
        self._list_configs: dict[str, dict[str, Any]] = {}
        self._column_update_rules: dict[str, dict[str, Any]] = {}

        self._toolbar_actions: dict[str, dict[str, Any]] = {
            "add_text": {
                "text": "Add Text Line",
                "visible": True,
                "enabled": True,
                "callback": lambda: self.add_text_line(edit=True),
            },
            "barcode_scan": {
                "text": "Barcode Scan",
                "visible": True,
                "enabled": True,
                "callback": self._emit_barcode_scan,
            },
            "check_stock": {
                "text": "Check Stock",
                "visible": True,
                "enabled": True,
                "callback": self._emit_stock_check,
            },
        }

        self._model = DocumentLinesModel(self)
        self._model.set_columns(self._columns)
        self._model.set_units(self._units)

        self._view = QTableView(self)
        self._view.setObjectName("DocumentLinesTableView")
        self._view.setModel(self._model)
        self._view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._view.setSelectionMode(QAbstractItemView.SingleSelection)
        self._view.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed
        )
        self._view.setAlternatingRowColors(False)
        self._view.setShowGrid(False)
        self._view.setWordWrap(False)
        self._view.setMouseTracking(True)
        self._view.verticalHeader().setVisible(False)
        self._view.verticalHeader().setDefaultSectionSize(44)
        self._view.horizontalHeader().setHighlightSections(False)
        self._view.horizontalHeader().setStretchLastSection(False)
        self._view.horizontalHeader().setDefaultAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )
        self._view.setContextMenuPolicy(Qt.CustomContextMenu)
        self._view.viewport().installEventFilter(self)

        self._text_delegate = DocumentLinesTextDelegate(self._view)
        self._numeric_delegate = DocumentLinesNumericDelegate(parent=self._view)
        self._combo_delegate = DocumentLinesComboDelegate(self._units, self._view)
        self._type_delegate = DocumentLinesTypeDelegate(self._view)
        self._index_delegate = DocumentLinesIndexDelegate(self._view)
        self._actions_delegate = DocumentLinesActionsDelegate(self._view)

        # Article search (live, database-backed via signals).
        self._search_results: list[dict[str, Any]] = []
        self._search_completer_model = QStringListModel(self)
        self._search_delegate = DocumentLinesSearchDelegate(self._view)
        self._search_delegate.set_completer_model(self._search_completer_model)
        self._search_min_chars = 1
        self._search_debounce = QTimer(self)
        self._search_debounce.setSingleShot(True)
        self._search_debounce.setInterval(250)
        self._pending_search_text = ""
        self._pending_search_row = -1
        self._pending_search_column = ""
        self._active_list_column = ""

        self._toolbar = self._build_toolbar()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._view)
        layout.addWidget(self._toolbar)

        self._configure_header()
        self._configure_delegates()
        self._wire_model()
        self._wire_view()
        self._setup_shortcuts()
        self._load_stylesheet()
        self._apply_configuration_to_model()
        self._emit_totals_changed()

    # ================================================================== #
    # Public API - configuration                                         #
    # ================================================================== #
    def set_columns(self, columns: list[DocumentLineColumn]) -> None:
        self._columns = list(columns)
        self._default_column_visibility = {
            column.key: column.visible for column in self._columns
        }
        saved_columns = self._load_saved_visible_columns()
        if saved_columns:
            for column in self._columns:
                column.visible = column.key in saved_columns
        self._model.set_columns(self._columns)
        self._configure_header()
        self._configure_delegates()

    def show_column(self, key: str) -> None:
        visible = set(self.visible_columns())
        visible.add(key)
        self.set_visible_columns(visible)

    def hide_column(self, key: str) -> None:
        visible = set(self.visible_columns())
        visible.discard(key)
        self.set_visible_columns(visible)

    def visible_columns(self) -> list[str]:
        """Return visible column keys in their configured order."""
        return [column.key for column in self._columns if column.visible]

    def set_visible_columns(self, column_names: Iterable[str]) -> None:
        """Apply column visibility in one model reset."""
        visible = set(column_names)
        known = {column.key for column in self._columns}
        unknown = visible - known
        if unknown:
            raise ValueError(
                f"Unknown column(s): {', '.join(sorted(unknown))}"
            )
        if not visible:
            raise ValueError("At least one column must remain visible")
        for column in self._columns:
            column.visible = column.key in visible
        self._model.set_columns(self._columns)
        self._configure_header()
        self._configure_delegates()
        self._save_visible_columns()
        self.columnVisibilityChanged.emit(self.visible_columns())

    def set_column_settings_key(self, key: str | None) -> None:
        """Set the QSettings key used to persist visible columns.

        Configure this before :meth:`set_columns` so saved visibility is
        restored as the page defines its columns.
        """
        self._column_settings_key = str(key).strip() if key else None

    def open_column_settings(self) -> None:
        """Open the footer column chooser dialog."""
        dialog = _ColumnSettingsDialog(
            self._columns, self._default_column_visibility, self
        )
        if dialog.exec_() == QDialog.Accepted:
            self.set_visible_columns(dialog.selected_columns())

    def set_column_width(self, key: str, width: int) -> None:
        col_idx = self._model.column_index_for_key(key)
        if col_idx is None:
            return
        self._view.setColumnWidth(col_idx, width)
        for col in self._columns:
            if col.key == key:
                col.width = width

    def set_editable(self, editable: bool) -> None:
        self._editable = editable
        self._read_only = not editable
        self._model.set_read_only(self._read_only)
        triggers = (
            QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed
            if editable
            else QAbstractItemView.NoEditTriggers
        )
        self._view.setEditTriggers(triggers)

    def set_read_only(self, read_only: bool) -> None:
        self.set_editable(not read_only)

    def set_tax_enabled(self, enabled: bool) -> None:
        self._tax_enabled = enabled
        self._model.set_tax_enabled(enabled)
        if not enabled:
            self._hide_existing_columns(("vat_percent", "tva_percentage"))
        else:
            self._restore_feature_columns(("vat_percent", "tva_percentage"))

    def set_discount_enabled(self, enabled: bool) -> None:
        self._discount_enabled = enabled
        self._model.set_discount_enabled(enabled)
        if not enabled:
            self._hide_existing_columns(
                ("discount_percent", "remise_percentage")
            )
        else:
            self._restore_feature_columns(
                ("discount_percent", "remise_percentage")
            )

    def set_default_vat_percent(self, percent: float) -> None:
        self._default_vat_percent = float(percent)

    def set_default_unit(self, unit: str) -> None:
        self._default_unit = unit or "Unit"

    def set_units(self, units: list[str]) -> None:
        self._units = list(units) if units else ["Unit"]
        self._model.set_units(self._units)
        self._combo_delegate.set_options(self._units)

    def set_vat_rates(self, rates: list[float]) -> None:
        self._vat_rates = list(rates)

    def set_currency_symbol(self, symbol: str) -> None:
        self._currency_symbol = symbol or ""
        self._model.set_currency_symbol(symbol)

    def set_number_format(self, decimals: int = 2, thousands_sep: str = " ") -> None:
        self._number_decimals = decimals
        self._thousands_sep = thousands_sep
        self._model.set_number_format(decimals, thousands_sep)

    def set_toolbar_visible(self, visible: bool) -> None:
        self._toolbar.setVisible(visible)
        self._view.setProperty("toolbar", "true" if visible else "false")
        self._view.style().unpolish(self._view)
        self._view.style().polish(self._view)

    def set_toolbar_action_enabled(self, action_key: str, enabled: bool) -> None:
        action = self._toolbar_actions.get(action_key)
        if action and action.get("button"):
            action["enabled"] = enabled
            action["button"].setEnabled(enabled)

    def set_toolbar_action_visible(self, action_key: str, visible: bool) -> None:
        action = self._toolbar_actions.get(action_key)
        if action and action.get("button"):
            action["visible"] = visible
            action["button"].setVisible(visible)

    def set_placeholder_text(self, text: str) -> None:
        self._model.set_placeholder_text(text)
        self._search_delegate.set_placeholder_text(text)

    def set_validation_rules(
        self,
        rules: list[Callable[[DocumentLine, int], str | None]],
    ) -> None:
        self._validation_rules = list(rules)

    def set_list(
        self,
        column_name: str,
        provider: Callable[[str], list[Any]] | list[Any] | tuple[Any, ...],
        *,
        display_fields: str | tuple[str, ...] | list[str] | None = None,
        selected_display_field: str | None = None,
        min_chars: int = 1,
        debounce_ms: int = 250,
    ) -> None:
        """Attach a searchable data source to any editable column.

        The provider is a static sequence or a callable receiving the search
        text. Dictionary result keys must use the same names as the widget's
        columns; matching cells are populated automatically. Database queries
        stay in the page model, so callers pass a model method rather than SQL.
        When one ``display_fields`` value is supplied, it is also used as the
        rendered label for an ID-backed cell unless ``selected_display_field``
        explicitly selects a different label field.
        """
        if not callable(provider) and not isinstance(provider, (list, tuple)):
            raise TypeError("provider must be a callable or a list/tuple of options")
        normalized_display_fields = (
            (display_fields,)
            if isinstance(display_fields, str)
            else tuple(display_fields or ())
        )
        if selected_display_field is None and len(normalized_display_fields) == 1:
            selected_display_field = normalized_display_fields[0]
        self._list_configs[column_name] = {
            "provider": provider,
            "display_fields": normalized_display_fields,
            "selected_display_field": selected_display_field,
            "min_chars": max(0, int(min_chars)),
            "debounce_ms": max(0, int(debounce_ms)),
        }
        self._model.set_searchable_columns(self._list_configs)
        self._sync_list_display_fields()
        self._configure_delegates()

    def remove_list(self, column_name: str) -> None:
        """Remove a list previously registered with :meth:`set_list`."""
        self._list_configs.pop(column_name, None)
        self._model.set_searchable_columns(self._list_configs)
        self._sync_list_display_fields()
        self._configure_delegates()

    def set_column_updates(
        self,
        source_columns: str | Iterable[str],
        updates: Mapping[str, Callable[[Mapping[str, Any]], Any]]
        | Callable[[Mapping[str, Any]], Mapping[str, Any]],
        *,
        name: str | None = None,
        run_on_load: bool | None = None,
    ) -> str:
        """Register a cascading row update rule using exact column names.

        A mapping calculates each target from the same immutable row snapshot.
        A single callable acts as an external resolver and returns a dictionary
        of target column values. Resolver callbacks may query a page model; raw
        SQL is intentionally not accepted by the widget.
        """
        sources = (
            (source_columns,)
            if isinstance(source_columns, str)
            else tuple(dict.fromkeys(source_columns))
        )
        if not sources or any(not isinstance(source, str) for source in sources):
            raise ValueError("source_columns must contain at least one column name")

        allowed = self._configured_column_names()
        unknown_sources = set(sources) - allowed
        if unknown_sources:
            raise ValueError(
                f"Unknown source column(s): {', '.join(sorted(unknown_sources))}"
            )

        is_mapping = isinstance(updates, Mapping)
        if is_mapping:
            normalized_updates = dict(updates)
            if not normalized_updates:
                raise ValueError("updates mapping cannot be empty")
            unknown_targets = set(normalized_updates) - allowed
            if unknown_targets:
                raise ValueError(
                    f"Unknown target column(s): {', '.join(sorted(unknown_targets))}"
                )
            if any(not callable(callback) for callback in normalized_updates.values()):
                raise TypeError("Every mapped column update must be callable")
        elif callable(updates):
            normalized_updates = updates
        else:
            raise TypeError("updates must be a callback or a mapping of callbacks")

        rule_name = name or f"updates:{','.join(sources)}"
        rule = {
            "name": rule_name,
            "sources": frozenset(sources),
            "updates": normalized_updates,
            "is_mapping": is_mapping,
            "run_on_load": is_mapping if run_on_load is None else bool(run_on_load),
        }
        previous = self._column_update_rules.get(rule_name)
        self._column_update_rules[rule_name] = rule
        try:
            self._validate_static_update_cycles()
        except Exception:
            if previous is None:
                self._column_update_rules.pop(rule_name, None)
            else:
                self._column_update_rules[rule_name] = previous
            raise
        return rule_name

    def remove_column_updates(self, name: str) -> bool:
        """Remove a registered column update rule by name."""
        return self._column_update_rules.pop(name, None) is not None

    def clear_column_updates(self) -> None:
        """Remove all registered column update rules."""
        self._column_update_rules.clear()

    # ================================================================== #
    # Public API - line operations                                       #
    # ================================================================== #
    def add_product_line(
        self,
        line: DocumentLine | None = None,
        *,
        position: int | None = None,
    ) -> int:
        new_line = line or self._default_product_line()
        self._run_column_updates(
            new_line,
            position if position is not None else self._model.real_row_count(),
            self._configured_column_names(),
        )
        row = self._model.add_line(
            new_line, position=position, recalculate=False
        )
        self.lineAdded.emit(new_line, row)
        self._emit_totals_changed()
        return row

    def add_text_line(
        self,
        text: str = "",
        *,
        position: int | None = None,
        edit: bool = False,
    ) -> int:
        new_line = DocumentLine.text(text)
        recalculate_line(new_line)
        row = self._model.add_line(
            new_line, position=position, recalculate=False
        )
        self.lineAdded.emit(new_line, row)
        self._emit_totals_changed()
        if edit:
            self.edit_line_field(row, "description")
        return row

    def edit_line_field(self, row: int, key: str = "description") -> bool:
        """Focus the table and start editing ``key`` on ``row`` immediately."""
        col = self._model.column_index_for_key(key)
        if col is None or not (0 <= row < self._model.rowCount()):
            return False
        index = self._model.index(row, col)
        if not (self._model.flags(index) & Qt.ItemIsEditable):
            return False
        self._view.setFocus()
        self._view.setCurrentIndex(index)
        self._view.scrollTo(index)
        self._view.edit(index)
        return True

    def add_empty_line(self, *, position: int | None = None) -> int:
        return self.add_product_line(None, position=position)

    def remove_line(self, row: int | None = None) -> bool:
        row = row if row is not None else self.selected_row_index()
        if row is None or self._model.is_placeholder_row(row):
            return False
        removed = self._model.remove_line(row)
        if removed is None:
            return False
        self.lineRemoved.emit(removed, row)
        self._emit_totals_changed()
        return True

    def duplicate_line(self, row: int | None = None) -> int | None:
        row = row if row is not None else self.selected_row_index()
        if row is None or self._model.is_placeholder_row(row):
            return None
        source = self._model.line_at(row)
        if source is None:
            return None
        clone = source.clone()
        return self.add_product_line(clone, position=row + 1)

    def clear_lines(self) -> None:
        self._model.clear_lines()
        self._emit_totals_changed()

    def move_line_up(self, row: int | None = None) -> bool:
        row = row if row is not None else self.selected_row_index()
        if row is None or row <= 0:
            return False
        ok = self._model.move_line(row, row - 1)
        if ok:
            self._select_row(row - 1)
        return ok

    def move_line_down(self, row: int | None = None) -> bool:
        row = row if row is not None else self.selected_row_index()
        if row is None or row >= self._model.real_row_count() - 1:
            return False
        ok = self._model.move_line(row, row + 1)
        if ok:
            self._select_row(row + 1)
        return ok

    def set_lines(
        self,
        lines: list[DocumentLine] | list[dict[str, Any]],
        *,
        recalculate: bool = True,
    ) -> None:
        parsed = [
            line if isinstance(line, DocumentLine) else DocumentLine.from_dict(line)
            for line in lines
        ]
        if recalculate:
            all_columns = self._configured_column_names()
            for row, line in enumerate(parsed):
                self._run_column_updates(
                    line, row, all_columns, on_load=True
                )
        self._model.set_lines(parsed, recalculate=False)
        self._emit_totals_changed()

    def get_lines(self) -> list[DocumentLine]:
        return self._model.lines()

    def get_lines_as_dicts(self) -> list[dict[str, Any]]:
        return [line.to_dict() for line in self._model.lines()]

    def get_line(self, row: int) -> DocumentLine | None:
        return self._model.line_at(row)

    def update_line(self, row: int, line: DocumentLine | dict[str, Any]) -> None:
        parsed = line if isinstance(line, DocumentLine) else DocumentLine.from_dict(line)
        self._run_column_updates(
            parsed, row, self._configured_column_names()
        )
        self._model.update_line(row, parsed, recalculate=False)

    def selected_row_index(self) -> int | None:
        index = self._view.currentIndex()
        if not index.isValid() or self._model.is_placeholder_row(index.row()):
            return None
        return index.row()

    def selected_line(self) -> DocumentLine | None:
        row = self.selected_row_index()
        return self._model.line_at(row) if row is not None else None

    def recalculate_totals(self) -> DocumentTotals:
        all_columns = self._configured_column_names()
        for row, line in enumerate(self._model.lines()):
            self._run_column_updates(line, row, all_columns, on_load=True)
        totals = recalculate_document_totals(self._model.lines())
        if self._model.real_row_count():
            self._model._refresh_all_rows()
        else:
            self._emit_totals_changed(totals)
        return totals

    def get_document_totals(self) -> DocumentTotals:
        return recalculate_document_totals(self._model.lines())

    def validate(self) -> tuple[bool, list[str]]:
        errors: list[str] = []
        for row, line in enumerate(self._model.lines()):
            errors.extend(self._validate_line(line, row))
        return (len(errors) == 0, errors)

    def apply_article_to_placeholder(self, article_data: dict[str, Any]) -> int:
        """Helper for controllers: turn placeholder input into a product line."""
        line = self._line_from_article(article_data)
        row = self.add_product_line(line)
        self._model.clear_placeholder()
        return row

    def apply_article_to_line(self, row: int, article_data: dict[str, Any]) -> bool:
        """Replace an existing product row with the selected article data."""
        current = self._model.line_at(row)
        if current is None or self._model.is_placeholder_row(row):
            return False

        replacement = self._line_from_article(article_data)
        # Quantity and document-specific values belong to the line, not to the
        # article master record, so keep them while refreshing article fields.
        replacement.quantity = current.quantity
        replacement.discount_percent = current.discount_percent
        replacement.metadata = {**current.metadata, **replacement.metadata}
        self.update_line(row, replacement)
        self._select_row(row)
        return True

    # ----- Article search (database-backed via signals) --------------- #
    def set_article_search_results(self, results: list[dict[str, Any]]) -> None:
        """Feed database search results back to the placeholder search box.

        Call this from the controller after handling ``articleSearchRequested``.
        Each result is a dict; ``reference`` and ``designation`` (or
        ``name``/``description``) are used to build the suggestion label. When
        the user picks a suggestion, it is converted into a product line.
        """
        self._search_results = list(results or [])
        labels = [
            self._format_list_result(r, self._active_list_column)
            for r in self._search_results
        ]
        self._search_completer_model.setStringList(labels)
        editor = self._search_delegate.active_editor()
        completer = editor.completer() if editor is not None else None
        if completer is not None:
            completer.complete()

    def clear_article_search_results(self) -> None:
        self._search_results = []
        self._search_completer_model.setStringList([])

    def set_search_min_chars(self, count: int) -> None:
        """Minimum typed characters before a search is requested (default 1)."""
        self._search_min_chars = max(0, int(count))

    def set_search_debounce_ms(self, milliseconds: int) -> None:
        """Delay before emitting ``articleSearchRequested`` while typing."""
        self._search_debounce.setInterval(max(0, int(milliseconds)))

    def view(self) -> QTableView:
        return self._view

    def model(self) -> DocumentLinesModel:
        return self._model

    # ================================================================== #
    # Internal wiring                                                    #
    # ================================================================== #
    def _build_toolbar(self) -> QFrame:
        frame = QFrame(self)
        frame.setObjectName("DocumentLinesToolbar")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        for idx, (key, action) in enumerate(self._toolbar_actions.items()):
            if idx > 0:
                sep = QFrame(frame)
                sep.setObjectName("DocumentLinesToolbarSeparator")
                sep.setFrameShape(QFrame.VLine)
                layout.addWidget(sep)

            button = QPushButton(action["text"], frame)
            button.setObjectName("DocumentLinesToolbarButton")
            button.clicked.connect(action["callback"])
            button.setEnabled(action["enabled"])
            button.setVisible(action["visible"])
            action["button"] = button
            layout.addWidget(button)

        layout.addStretch(1)
        self._column_settings_button = QPushButton("Columns…", frame)
        self._column_settings_button.setObjectName("DocumentLinesToolbarButton")
        self._column_settings_button.setToolTip("Choose visible columns")
        self._column_settings_button.clicked.connect(self.open_column_settings)
        layout.addWidget(self._column_settings_button)
        return frame

    def _wire_model(self) -> None:
        self._model.cellEdited.connect(self._on_model_cell_edited)
        self._model.dataChanged.connect(self._on_model_data_changed)

    def _wire_view(self) -> None:
        self._view.clicked.connect(self._on_view_clicked)
        self._view.customContextMenuRequested.connect(self._on_context_menu)
        selection = self._view.selectionModel()
        if selection is not None:
            selection.currentChanged.connect(self._on_current_changed)
        self._actions_delegate.actionTriggered.connect(
            self._on_placeholder_add_clicked
        )
        self._search_delegate.searchTextChanged.connect(self._on_search_text_changed)
        self._search_delegate.searchSubmittedForRow.connect(
            self._on_search_submitted
        )
        self._search_delegate.itemChosen.connect(self._on_list_item_chosen)
        self._search_debounce.timeout.connect(self._emit_pending_search)

    def _setup_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+N"), self, activated=self.add_empty_line)
        QShortcut(QKeySequence("Ctrl+Insert"), self, activated=self.add_empty_line)
        QShortcut(
            QKeySequence("Ctrl+Shift+T"),
            self,
            activated=lambda: self.add_text_line(edit=True),
        )
        QShortcut(QKeySequence("Delete"), self, activated=self.remove_line)
        QShortcut(QKeySequence("Ctrl+D"), self, activated=self.duplicate_line)
        QShortcut(QKeySequence("Ctrl+Up"), self, activated=self.move_line_up)
        QShortcut(QKeySequence("Ctrl+Down"), self, activated=self.move_line_down)

    def _configure_header(self) -> None:
        header = self._view.horizontalHeader()
        stretch_col: int | None = None
        for visual_idx, col in enumerate(self._model.columns()):
            header.setSectionResizeMode(visual_idx, QHeaderView.Interactive)
            self._view.setColumnWidth(visual_idx, col.width)
            header.resizeSection(visual_idx, col.width)
            if col.stretch:
                stretch_col = visual_idx
        if stretch_col is not None:
            header.setSectionResizeMode(stretch_col, QHeaderView.Stretch)

    def _configure_delegates(self) -> None:
        for visual_idx, col in enumerate(self._model.columns()):
            if col.key == COL_TYPE:
                self._view.setItemDelegateForColumn(visual_idx, self._type_delegate)
            elif col.key == COL_INDEX:
                self._view.setItemDelegateForColumn(visual_idx, self._index_delegate)
            elif col.key == COL_ACTIONS:
                self._view.setItemDelegateForColumn(visual_idx, self._actions_delegate)
            elif col.key in self._list_configs:
                self._view.setItemDelegateForColumn(
                    visual_idx, self._search_delegate
                )
            elif col.editor_type == ColumnEditorType.NUMERIC:
                delegate = DocumentLinesNumericDelegate(
                    decimals=col.decimals,
                    minimum=0.0 if col.key != "discount_percent" else 0.0,
                    maximum=100.0
                    if col.key in ("discount_percent", "vat_percent")
                    else 999_999_999.0,
                    parent=self._view,
                )
                self._view.setItemDelegateForColumn(visual_idx, delegate)
            elif col.editor_type == ColumnEditorType.COMBO:
                self._view.setItemDelegateForColumn(visual_idx, self._combo_delegate)
            elif col.editor_type in (
                ColumnEditorType.TEXT,
                ColumnEditorType.READONLY,
                ColumnEditorType.COMPUTED,
            ):
                if col.key not in (COL_INDEX, COL_TYPE, COL_ACTIONS):
                    self._view.setItemDelegateForColumn(visual_idx, self._text_delegate)

    def _apply_configuration_to_model(self) -> None:
        self._model.set_read_only(self._read_only)
        self._model.set_tax_enabled(self._tax_enabled)
        self._model.set_discount_enabled(self._discount_enabled)
        self._model.set_currency_symbol(self._currency_symbol)
        self._model.set_number_format(self._number_decimals, self._thousands_sep)
        self._model.set_units(self._units)

    def _load_stylesheet(self) -> None:
        try:
            with open(_QSS_PATH, encoding="utf-8") as fh:
                self.setStyleSheet(fh.read())
        except OSError:
            pass

    def _default_product_line(self) -> DocumentLine:
        return DocumentLine.product(
            quantity=1.0,
            unit=self._default_unit,
            price_ht=0.0,
            discount_percent=0.0,
            vat_percent=self._default_vat_percent if self._tax_enabled else 0.0,
        )

    def _line_from_article(self, data: dict[str, Any]) -> DocumentLine:
        return DocumentLine.product(
            article_id=data.get("article_id") or data.get("id"),
            reference=str(
                data.get("reference")
                or data.get("code_article")
                or ""
            ),
            designation=str(data.get("designation") or ""),
            description=str(
                data.get("notes")
                or data.get("description")
                or data.get("designation")
                or ""
            ),
            quantity=float(data.get("quantity") or 1),
            unit=str(data.get("unit") or data.get("nom_unite") or self._default_unit),
            unit_id=data.get("unite_id") or data.get("unit_id"),
            price_ht=float(
                data.get("price_ht")
                or data.get("prix_unitaire_ht")
                or data.get("prix_vente_ht")
                or 0
            ),
            discount_percent=float(
                data.get("discount_percent") or data.get("remise_percentage") or 0
            ),
            vat_percent=float(
                data.get("vat_percent")
                or data.get("tva_percentage")
                or data.get("taux")
                or self._default_vat_percent
            ),
            vat_id=data.get("vat_id") or data.get("tva_id"),
            metadata={
                k: v
                for k, v in data.items()
                if k
                not in {
                    "article_id",
                    "id",
                    "reference",
                    "code_article",
                    "designation",
                    "description",
                    "quantity",
                    "unit",
                    "unit_id",
                    "price_ht",
                    "prix_unitaire_ht",
                    "prix_vente_ht",
                    "discount_percent",
                    "remise_percentage",
                    "vat_percent",
                    "tva_percentage",
                    "vat_id",
                    "tva_id",
                }
            },
        )

    def _validate_line(self, line: DocumentLine, row: int) -> list[str]:
        errors: list[str] = []
        prefix = f"Line {row + 1}"

        if line.line_type == LineType.PRODUCT:
            desc = (line.description or line.designation or "").strip()
            if not desc:
                errors.append(f"{prefix}: description is required for product lines.")
            if line.quantity <= 0:
                errors.append(f"{prefix}: quantity must be greater than zero.")
            if line.price_ht < 0:
                errors.append(f"{prefix}: price cannot be negative.")
            if not 0 <= line.discount_percent <= 100:
                errors.append(f"{prefix}: discount must be between 0 and 100.")
            if self._tax_enabled and not 0 <= line.vat_percent <= 100:
                errors.append(f"{prefix}: VAT must be between 0 and 100.")

        elif line.line_type == LineType.TEXT:
            if not (line.description or line.designation or "").strip():
                errors.append(f"{prefix}: text line cannot be empty.")

        for rule in self._validation_rules:
            message = rule(line, row)
            if message:
                errors.append(message)

        return errors

    def _emit_totals_changed(self, totals: DocumentTotals | None = None) -> None:
        if self._emitting_totals:
            return
        self._emitting_totals = True
        try:
            payload = (totals or self.get_document_totals()).to_dict()
            self.totalsChanged.emit(payload)
        finally:
            self._emitting_totals = False

    def _format_search_result(self, result: dict[str, Any]) -> str:
        reference = str(
            result.get("reference")
            or result.get("code_article")
            or ""
        ).strip()
        name = str(
            result.get("designation")
            or result.get("description")
            or result.get("name")
            or ""
        ).strip()
        if reference and name:
            return f"{reference}  —  {name}"
        return reference or name or str(result)

    def _format_list_result(self, result: Any, column_name: str) -> str:
        config = self._list_configs.get(column_name, {})
        fields = config.get("display_fields", ())
        if isinstance(result, dict):
            if fields:
                values = [str(result.get(field) or "").strip() for field in fields]
                return "  —  ".join(value for value in values if value)
            return self._format_search_result(result)
        return str(result)

    def _on_search_text_changed(
        self, text: str, row: int, column_name: str
    ) -> None:
        config = self._list_configs.get(column_name)
        if config is None:
            return
        self._pending_search_text = text
        self._pending_search_row = row
        self._pending_search_column = column_name
        self._active_list_column = column_name
        if len(text.strip()) < config["min_chars"]:
            self._search_debounce.stop()
            self.clear_article_search_results()
            return
        self._search_debounce.setInterval(config["debounce_ms"])
        self._search_debounce.start()

    def _emit_pending_search(self) -> None:
        text = self._pending_search_text.strip()
        config = self._list_configs.get(self._pending_search_column)
        if not text or config is None:
            return
        provider = config["provider"]
        if callable(provider):
            results = provider(text) or []
        else:
            needle = text.casefold()
            results = [
                item
                for item in provider
                if needle
                in self._format_list_result(
                    item, self._pending_search_column
                ).casefold()
            ]
        self.set_article_search_results(list(results))

    def _on_list_item_chosen(
        self, result_index: int, edited_row: int, column_name: str
    ) -> None:
        if 0 <= result_index < len(self._search_results):
            self._apply_list_result(
                edited_row, column_name, self._search_results[result_index]
            )
        self.clear_article_search_results()

    def _on_search_submitted(
        self, text: str, edited_row: int, column_name: str
    ) -> None:
        """Apply an unambiguous result when Enter closes the editor."""
        needle = text.strip().casefold()
        exact_matches = [
            (idx, result)
            for idx, result in enumerate(self._search_results)
            if needle == self._format_list_result(result, column_name).casefold()
            or (
                isinstance(result, dict)
                and needle
                in {str(value).strip().casefold() for value in result.values()}
            )
        ]
        if len(exact_matches) == 1:
            self._on_list_item_chosen(
                exact_matches[0][0], edited_row, column_name
            )
            return

        self._pending_search_text = text
        self._pending_search_row = edited_row
        self._pending_search_column = column_name
        self._emit_pending_search()
        refreshed_matches = [
            idx
            for idx, result in enumerate(self._search_results)
            if needle == self._format_list_result(result, column_name).casefold()
            or (
                isinstance(result, dict)
                and needle
                in {str(value).strip().casefold() for value in result.values()}
            )
        ]
        if len(refreshed_matches) == 1:
            self._on_list_item_chosen(
                refreshed_matches[0], edited_row, column_name
            )
        elif len(self._search_results) == 1:
            # Enter also confirms the only available filtered option.
            self._on_list_item_chosen(0, edited_row, column_name)

    def _apply_list_result(
        self, row: int, column_name: str, result: Any
    ) -> None:
        is_placeholder = self._model.is_placeholder_row(row)
        current = None if is_placeholder else self._model.line_at(row)
        if current is None and not is_placeholder:
            return
        line = self._default_product_line() if is_placeholder else current.clone()
        if current is not None:
            line.line_id = current.line_id
        if isinstance(result, dict):
            # Providers use the declared/database column names directly. Keep
            # every returned value: visible fields update their cells and
            # auxiliary database fields remain available in line metadata.
            for field_name, value in result.items():
                self._model._assign_value(line, field_name, value)
        else:
            self._model._assign_value(line, column_name, result)
        if is_placeholder:
            self.add_product_line(line)
            self._model.clear_placeholder()
        else:
            self.update_line(row, line)
            self._select_row(row)

    def _configured_column_names(self) -> set[str]:
        return {
            column.key
            for column in self._columns
            if column.key not in (COL_INDEX, COL_TYPE, COL_ACTIONS)
        }

    def _sync_list_display_fields(self) -> None:
        self._model.set_display_fields(
            {
                column_name: config["selected_display_field"]
                for column_name, config in self._list_configs.items()
                if config.get("selected_display_field")
                and config["selected_display_field"] != column_name
            }
        )

    def _settings_path(self) -> str | None:
        if not self._column_settings_key:
            return None
        return f"DocumentLinesWidget/{self._column_settings_key}/visible_columns"

    def _load_saved_visible_columns(self) -> set[str] | None:
        path = self._settings_path()
        if path is None:
            return None
        value = QSettings("AZENZ", "AZENZ").value(path)
        if value is None:
            return None
        if isinstance(value, str):
            value = [value]
        saved = {str(column) for column in value}
        known = {column.key for column in self._columns}
        saved &= known
        return saved or None

    def _save_visible_columns(self) -> None:
        path = self._settings_path()
        if path is None:
            return
        settings = QSettings("AZENZ", "AZENZ")
        settings.setValue(path, self.visible_columns())
        settings.sync()

    def _hide_existing_columns(self, column_names: Iterable[str]) -> None:
        existing = {column.key for column in self._columns}
        targets = set(column_names) & existing
        if not targets:
            return
        visible = set(self.visible_columns()) - targets
        if not visible:
            return
        self._feature_hidden_columns.update(
            targets & set(self.visible_columns())
        )
        for column in self._columns:
            if column.key in targets:
                column.visible = False
        self._model.set_columns(self._columns)
        self._configure_header()
        self._configure_delegates()

    def _restore_feature_columns(self, column_names: Iterable[str]) -> None:
        targets = set(column_names) & self._feature_hidden_columns
        if not targets:
            return
        for column in self._columns:
            if column.key in targets:
                column.visible = True
        self._feature_hidden_columns -= targets
        self._model.set_columns(self._columns)
        self._configure_header()
        self._configure_delegates()

    def _validate_static_update_cycles(self) -> None:
        graph: dict[str, set[str]] = {}
        for rule in self._column_update_rules.values():
            if not rule["is_mapping"]:
                continue
            targets = set(rule["updates"])
            for source in rule["sources"]:
                graph.setdefault(source, set()).update(targets)

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(column: str) -> None:
            if column in visiting:
                raise ValueError(
                    f"Column update dependency cycle detected at {column!r}"
                )
            if column in visited:
                return
            visiting.add(column)
            for target in graph.get(column, ()):
                visit(target)
            visiting.remove(column)
            visited.add(column)

        for source in graph:
            visit(source)

    def _row_values(self, line: DocumentLine) -> dict[str, Any]:
        values = dict(line.metadata)
        serialized = line.to_dict()
        serialized.pop("metadata", None)
        values.update(serialized)
        for column in self._columns:
            if column.key not in (COL_INDEX, COL_TYPE, COL_ACTIONS):
                values[column.key] = self._model._raw_value(line, column.key)
        return values

    def _run_column_updates(
        self,
        line: DocumentLine,
        row: int,
        changed_columns: Iterable[str],
        *,
        on_load: bool = False,
    ) -> None:
        before_core = self._row_values(line)
        recalculate_line(line)
        after_core = self._row_values(line)
        initial_sources = set(changed_columns)
        initial_sources.update(
            key
            for key in self._configured_column_names()
            if before_core.get(key) != after_core.get(key)
        )
        if not self._column_update_rules:
            return

        queue = deque(initial_sources)
        last_signatures: dict[str, tuple[Any, ...]] = {}
        execution_count = 0
        max_executions = max(
            10,
            len(self._column_update_rules)
            * (len(self._configured_column_names()) + 1),
        )

        while queue:
            source_column = queue.popleft()
            for rule in self._column_update_rules.values():
                if source_column not in rule["sources"]:
                    continue
                if on_load and not rule["run_on_load"]:
                    continue

                snapshot_dict = self._row_values(line)
                signature = tuple(
                    snapshot_dict.get(source)
                    for source in sorted(rule["sources"])
                )
                if last_signatures.get(rule["name"]) == signature:
                    continue
                last_signatures[rule["name"]] = signature
                execution_count += 1
                if execution_count > max_executions:
                    self.columnUpdateFailed.emit(
                        row,
                        source_column,
                        rule["name"],
                        "Runtime column dependency cycle detected",
                    )
                    return

                snapshot = MappingProxyType(snapshot_dict)
                try:
                    if rule["is_mapping"]:
                        result = {
                            target: callback(snapshot)
                            for target, callback in rule["updates"].items()
                        }
                    else:
                        result = rule["updates"](snapshot)
                        if not isinstance(result, Mapping):
                            raise TypeError(
                                "An update resolver must return a mapping"
                            )
                        result = dict(result)
                    unknown = set(result) - self._configured_column_names()
                    if unknown:
                        raise ValueError(
                            "Unknown returned column(s): "
                            + ", ".join(sorted(unknown))
                        )
                except Exception as exc:
                    self.columnUpdateFailed.emit(
                        row,
                        source_column,
                        rule["name"],
                        str(exc),
                    )
                    continue

                changed_targets: list[str] = []
                for target, value in result.items():
                    old_value = self._model._raw_value(line, target)
                    self._model._assign_value(line, target, value)
                    new_value = self._model._raw_value(line, target)
                    if old_value != new_value:
                        changed_targets.append(target)
                queue.extend(changed_targets)

    def _on_model_cell_edited(self, row: int, column_name: str) -> None:
        line = self._model.line_at(row)
        if line is not None:
            self._run_column_updates(line, row, (column_name,))

    def _emit_barcode_scan(self) -> None:
        self.barcodeScanRequested.emit()

    def _emit_stock_check(self) -> None:
        self.stockCheckRequested.emit()

    def _select_row(self, row: int) -> None:
        if 0 <= row < self._model.rowCount():
            index = self._model.index(row, 0)
            self._view.setCurrentIndex(index)
            self._view.selectRow(row)

    # ================================================================== #
    # Event handlers                                                     #
    # ================================================================== #
    def _on_model_data_changed(
        self,
        top_left: QModelIndex,
        bottom_right: QModelIndex,
        roles=None,
    ) -> None:
        for row in range(top_left.row(), bottom_right.row() + 1):
            if self._model.is_placeholder_row(row):
                # Live search is driven by the search delegate's textChanged
                # signal, so committing the placeholder must not re-query.
                continue

            line = self._model.line_at(row)
            if line is not None:
                self.lineChanged.emit(line, row)

        self._emit_totals_changed()

    def _on_view_clicked(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        if self._model.is_placeholder_row(index.row()):
            col = self._model.columns()[index.column()]
            if col.key in ("reference", "code_article", "description", "designation"):
                self._view.edit(index)
            return

        line = self._model.line_at(index.row())
        if line is not None:
            self.lineSelected.emit(line, index.row())

    def _on_current_changed(
        self,
        current: QModelIndex,
        previous: QModelIndex,
    ) -> None:
        if not current.isValid() or self._model.is_placeholder_row(current.row()):
            return
        line = self._model.line_at(current.row())
        if line is not None:
            self.lineSelected.emit(line, current.row())

    def _on_context_menu(self, pos: QPoint) -> None:
        index = self._view.indexAt(pos)
        if not index.isValid() or self._model.is_placeholder_row(index.row()):
            return

        line = self._model.line_at(index.row())
        if line is None:
            return

        row = index.row()
        menu = QMenu(self)
        menu.addAction("Duplicate", lambda: self.duplicate_line(row))
        menu.addAction("Move Up", lambda: self.move_line_up(row))
        menu.addAction("Move Down", lambda: self.move_line_down(row))
        menu.addSeparator()
        menu.addAction("Remove", lambda: self.remove_line(row))
        menu.exec_(self._view.viewport().mapToGlobal(pos))

    def _on_placeholder_add_clicked(self, action: str, row: int) -> None:
        if action != "add_from_placeholder":
            return
        text = self._model.placeholder_search_text().strip()
        if text:
            self.articleSearchRequested.emit(text)
            return
        self.add_empty_line()
        self._model.clear_placeholder()

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if obj is self._view.viewport() and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                index = self._view.currentIndex()
                if index.isValid() and self._model.is_placeholder_row(index.row()):
                    self._on_placeholder_add_clicked("add_from_placeholder", index.row())
                    return True
        return super().eventFilter(obj, event)
