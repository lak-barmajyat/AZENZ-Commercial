from pathlib import Path

from PyQt5.uic import loadUi

_ROOT = Path(__file__).resolve().parent.parent


def load_ui(relative_ui_path: str, widget) -> object:
    """Load a .ui file located under the project root, from any CWD."""
    return loadUi(str(_ROOT / relative_ui_path), widget)
