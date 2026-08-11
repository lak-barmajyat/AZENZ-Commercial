"""SearchLineEdit - a small reusable search box for ERP pages.

It is a thin :class:`QLineEdit` subclass that:

* picks up the **global** styling already defined in ``theme/style/base.qss``
  (the ``QLineEdit[class="icon-lineedit"]`` rules) instead of carrying its own
  stylesheet, so it always matches the rest of the application;
* shows a leading search icon and a built-in clear button;
* emits a debounced :pyattr:`searchChanged` signal while typing and a
  :pyattr:`searchSubmitted` signal when the user presses Enter.

It contains no business logic: pages connect to its signals and run the
actual search/query themselves.

------------------------------------------------------------------------------
Qt Designer "Promote to..." instructions
------------------------------------------------------------------------------
1. Drop a plain ``QLineEdit`` onto your form.
2. Right-click it -> "Promote to...".
3. Fill in:
       Promoted class name : SearchLineEdit
       Header file         : ui_utils.widgets.search_line_edit
4. Click "Add", then "Promote".
"""

from __future__ import annotations

from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QWidget

from ui_utils.canvas import get_colored_icon

_ICON_RESOURCE = ":/icons/icons/rechercher.svg"

_ICON_COLOR = "#9CA3AF"


class SearchLineEdit(QLineEdit):
    """Reusable search line edit styled by the global ``base.qss``.

    Signals:
        searchChanged(str): Emitted (debounced) while the text changes.
        searchSubmitted(str): Emitted when Enter/Return is pressed.
    """

    searchChanged = pyqtSignal(str)
    searchSubmitted = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # Inherit the global "icon-lineedit" look from theme/style/base.qss.
        self.setProperty("class", "icon-lineedit")

        self.setPlaceholderText("Rechercher...")
        self.setClearButtonEnabled(True)

        # Leading search icon (recolored to a muted gray).
        self._search_action = self.addAction(
            self._load_icon(), QLineEdit.LeadingPosition
        )

        # Debounce typing so connected slots are not spammed per keystroke.
        self._debounce = QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(250)
        self._debounce.timeout.connect(self._emit_search_changed)

        self.textChanged.connect(self._on_text_changed)
        self.returnPressed.connect(
            lambda: self.searchSubmitted.emit(self.text().strip())
        )

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #
    def set_debounce_ms(self, milliseconds: int) -> None:
        """Set the typing debounce delay before ``searchChanged`` fires."""
        self._debounce.setInterval(max(0, int(milliseconds)))

    def search_text(self) -> str:
        """Current trimmed search text."""
        return self.text().strip()

    def clear_search(self) -> None:
        """Clear the field without emitting a debounced search."""
        self._debounce.stop()
        self.clear()

    # ------------------------------------------------------------------ #
    # Internal                                                           #
    # ------------------------------------------------------------------ #
    def _load_icon(self):
        return get_colored_icon(_ICON_RESOURCE, _ICON_COLOR)

    def _on_text_changed(self, _text: str) -> None:
        self._debounce.start()

    def _emit_search_changed(self) -> None:
        self.searchChanged.emit(self.text().strip())
