from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolButton

from ui_utils.canvas import get_colored_icon


class _DangerHoverFilter(QObject):
    def __init__(self, button):
        super().__init__(button)
        self._button = button
        self._original = None

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            if self._original is None:
                self._original = QIcon(self._button.icon())
            self._button.setIcon(get_colored_icon(self._original, "#dc2626"))
        elif event.type() == QEvent.Leave:
            if self._original is not None:
                self._button.setIcon(self._original)
        return False


def install_danger_icon_hover(button):
    if button is None:
        return
    if button.icon() is None or button.icon().isNull():
        return
    button.installEventFilter(_DangerHoverFilter(button))
