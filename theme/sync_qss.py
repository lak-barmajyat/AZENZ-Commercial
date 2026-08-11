#!/usr/bin/env python3
"""Sync theme/style/base.qss into the top-level styleSheet of every window.

The top-level styleSheet of each .ui is replaced with the current content of
theme/style/base.qss (marker-wrapped), so editing the master QSS once and
running this tool propagates the change to all windows.

Commands:
  sync            (default) embed the current base.qss into every window.
  check           report windows whose embedded QSS differs from base.qss.
  diff            show a unified diff between base.qss and each window's QSS.
  back [1|2]      restore base.qss from theme/backups/base.qss.1 (previous)
                  or base.qss.2 (previous-previous), then re-sync.
  list            show available backups.

Options:
  --ui PATH       restrict sync/check/diff to a single .ui file.

Only the TOP-LEVEL widget's styleSheet property is managed. Per-widget
styleSheet properties (icons, logos, ...) are left untouched.

Before each sync a snapshot of the previous base.qss is rotated into
theme/backups/ (last 2 versions kept).
"""

import argparse
import difflib
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

THEME_DIR = Path(__file__).resolve().parent
BASE_ = THEME_DIR / "style" / "base.qss"
BACKUP_DIR = THEME_DIR / "backups"
MODULES_DIR = THEME_DIR.parent / "modules"

START_MARKER = "AUTO-SYNCED QSS START"


def ui_files():
    return sorted(MODULES_DIR.rglob("*.ui"))


def read_base():
    return BASE_QSS.read_text(encoding="utf-8")


def top_style_sheet(ui):
    """Return (property_exists, current_text) of the top-level widget."""
    try:
        root = ET.parse(str(ui)).getroot()
    except ET.ParseError:
        return False, None
    top = next(root.iter("widget"), None)
    if top is None:
        return False, None
    for prop in top.findall("property"):
        if prop.get("name") == "styleSheet":
            string = prop.find("string")
            return True, "" if string is None or string.text is None else string.text
    return False, None


def _insert_top_style_sheet(ui, text, content):
    """Insert a styleSheet property into the top-level widget (missing case)."""
    widget = text.find("<widget ")
    gt = text.find(">", widget)
    if widget == -1 or gt == -1:
        return False
    block = (
        '\n  <property name="styleSheet">\n'
        '   <string notr="true">' + content + "</string>\n"
        "  </property>"
    )
    ui.write_text(text[: gt + 1] + block + text[gt + 1:], encoding="utf-8")
    return True


def set_top_style_sheet(ui, content):
    """Replace the top-level styleSheet content. Returns True if changed."""
    text = ui.read_text(encoding="utf-8")
    exists, current = top_style_sheet(ui)
    if not exists:
        return _insert_top_style_sheet(ui, text, content)

    prop_idx = text.find('<property name="styleSheet">')
    if prop_idx == -1:
        return _insert_top_style_sheet(ui, text, content)

    string_idx = text.find("<string", prop_idx)
    if string_idx == -1:
        return _insert_top_style_sheet(ui, text, content)
    gt = text.find(">", string_idx)
    if gt == -1:
        return _insert_top_style_sheet(ui, text, content)

    if gt > 0 and text[gt - 1] == "/":
        # self-closing placeholder: <string notr="true"/>
        if content == "":
            return False
        ui.write_text(
            text[: gt - 1] + ">" + content + "</string>" + text[gt + 1:],
            encoding="utf-8",
        )
        return True

    close = text.find("</string>", gt + 1)
    if close == -1:
        return _insert_top_style_sheet(ui, text, content)

    old = text[gt + 1:close]
    if old != current:  # safety: raw text must match the parsed top-level property
        raise RuntimeError(f"styleSheet mismatch while editing {ui}")
    if old == content:
        return False
    ui.write_text(text[: gt + 1] + content + text[close:], encoding="utf-8")
    return True


def _first_embedded():
    """Return the base.qss content currently embedded in the first window."""
    for ui in ui_files():
        exists, text = top_style_sheet(ui)
        if exists and text and START_MARKER in text:
            return text
    return None


def rotate_backup():
    """Snapshot the currently-embedded QSS before it gets overwritten.

    .1 keeps the version about to be replaced (the ``back 1`` target),
    .2 the one before it. Versions already in the chain are shifted down.
    """
    prev = _first_embedded()
    if prev is None or prev == read_base():
        return False
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    v1 = BACKUP_DIR / "base.qss.1"
    v2 = BACKUP_DIR / "base.qss.2"
    old_v1 = v1.read_text(encoding="utf-8") if v1.exists() else None
    if old_v1 is not None:
        v2.write_text(old_v1, encoding="utf-8")
    else:
        v2.unlink(missing_ok=True)
    v1.write_text(prev, encoding="utf-8")
    return True


def sync(only=None):
    content = escape(read_base())
    files = [only] if only else ui_files()
    changed = []
    for ui in files:
        exists, _ = top_style_sheet(ui)
        if set_top_style_sheet(ui, content):
            changed.append(ui)
    return changed


def check(only=None):
    base = read_base()
    files = [only] if only else ui_files()
    return [ui for ui in files if top_style_sheet(ui) != (True, base)]


def diff(only=None):
    base_lines = read_base().splitlines()
    files = [only] if only else ui_files()
    shown = 0
    for ui in files:
        exists, current = top_style_sheet(ui)
        if not exists or current == read_base():
            continue
        print(f"--- {BASE_QSS}")
        print(f"+++ {ui}")
        for line in difflib.unified_diff(
            base_lines, current.splitlines(), lineterm=""
        ):
            print(line)
        shown += 1
    return shown


def restore(level):
    src = BACKUP_DIR / f"base.qss.{level}"
    if not src.exists():
        print(f"no backup {src.name}; nothing to restore", file=sys.stderr)
        return False
    BASE_QSS.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return True


def list_backups():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for level in (1, 2):
        path = BACKUP_DIR / f"base.qss.{level}"
        if path.exists():
            stamp = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(path.stat().st_mtime)
            )
            print(f"{path.name:12} {stamp}  {len(path.read_text())} chars")
        else:
            print(f"{path.name:12} (none)")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Sync theme/style/base.qss into every window's embedded QSS."
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="sync",
        choices=["sync", "check", "diff", "back", "list", "backups"],
        help="command to run (default: sync)",
    )
    parser.add_argument(
        "level",
        nargs="?",
        type=int,
        default=1,
        help="backup level for 'back': 1 = previous, 2 = previous-previous",
    )
    parser.add_argument("--ui", help="restrict sync/check/diff to a single .ui file")
    args = parser.parse_args(argv)

    only = Path(args.ui) if args.ui else None

    if args.command == "sync":
        rotate_backup()
        changed = sync(only)
        for ui in changed:
            print(f"updated {ui}")
        print(f"{len(changed)} window(s) updated")
    elif args.command == "check":
        stale = check(only)
        for ui in stale:
            print(f"stale  {ui}")
        print(f"{len(stale)} window(s) out of date")
        return 1 if stale else 0
    elif args.command == "diff":
        shown = diff(only)
        print(f"{shown} window(s) differ from base.qss")
    elif args.command == "back":
        if not restore(args.level):
            return 1
        print(f"restored theme/style/base.qss from backup level {args.level}")
        changed = sync(only)
        for ui in changed:
            print(f"updated {ui}")
        print(f"{len(changed)} window(s) updated")
    elif args.command in ("list", "backups"):
        list_backups()
    return 0


if __name__ == "__main__":
    sys.exit(main())
