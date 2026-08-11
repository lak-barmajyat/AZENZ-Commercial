from pathlib import Path

_BASE_QSS = Path(__file__).resolve().parent.parent / "theme" / "style" / "base.qss"


def load_base_qss() -> str:
    return _BASE_QSS.read_text(encoding="utf-8")
