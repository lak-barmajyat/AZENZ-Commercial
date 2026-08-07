import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt5.QtWidgets import QApplication

from window_manger.window_manager import Destination, WindowManager


class FakeWidget:
    def __init__(self, label=None):
        self.label = label
        self.show_calls = 0
        self.show_maximized_calls = 0
        self.hide_calls = 0
        self.close_calls = 0

    def show(self):
        self.show_calls += 1

    def showMaximized(self):
        self.show_maximized_calls += 1

    def hide(self):
        self.hide_calls += 1

    def close(self):
        self.close_calls += 1


class FakeHost(FakeWidget):
    def __init__(self):
        super().__init__("dashboard")
        self.pages = []

    def show_page(self, page_widget):
        self.pages.append(page_widget)

    def set_active_section(self, section):
        self.active_section = section


class FakeDocumentPage(FakeWidget):
    def __init__(self):
        super().__init__("document")
        self.controller = FakeDocumentController()


class FakeDocumentController:
    def __init__(self):
        self.document_id = None
        self.loaded = []
        self.prepared = 0

    def load_document(self, document_id):
        self.loaded.append(document_id)

    def prepare_new_document(self):
        self.prepared += 1


def _open_document(widget, kwargs):
    controller = getattr(widget, "controller", None)
    if controller is None:
        return

    document_id = kwargs.get("document_id")
    controller.document_id = document_id
    if document_id:
        controller.load_document(document_id)
        return

    prepare_new_document = getattr(controller, "prepare_new_document", None)
    if callable(prepare_new_document):
        prepare_new_document()


def _make_manager():
    manager = WindowManager()
    manager._windows = {
        "login": Destination(
            view=lambda: FakeWidget("login"),
            type="window",
        ),
        "table_de_bord.menu": Destination(
            view=FakeHost,
            type="window",
        ),
        "table_de_bord.widget": Destination(
            view=lambda: FakeWidget("dashboard_page"),
            type="page",
            section="table_de_bord",
        ),
        "ventes.list": Destination(
            view=lambda: FakeWidget("ventes"),
            type="page",
            section="ventes",
        ),
        "ventes.nouveau_doc": Destination(
            view=FakeDocumentPage,
            type="page",
            section="ventes",
            on_open=_open_document,
        ),
    }
    return manager


_APP = None


def _make_manager_with_app():
    global _APP
    _APP = QApplication.instance()
    if _APP is None:
        _APP = QApplication([])
    manager = _make_manager()
    _APP.window_manager = manager
    return manager


def test_open_window_creates_once_and_reuses():
    manager = _make_manager_with_app()

    first = manager.open("login")
    second = manager.open("login")

    assert first is second
    assert first.show_maximized_calls == 2
    assert manager.get_instance("login") is first


def test_open_page_uses_dashboard_host_and_syncs_active():
    manager = _make_manager_with_app()

    page = manager.open("ventes.list")

    dashboard = manager.get_instance("table_de_bord.menu")
    assert dashboard is not None
    assert dashboard.pages == [page]
    assert dashboard.active_section == "ventes"

    page_again = manager.open("ventes.list")
    assert page_again is page
    assert dashboard.pages == [page, page]


def test_open_page_creates_dashboard_host_when_needed():
    manager = _make_manager_with_app()

    page = manager.open("table_de_bord.widget")

    dashboard = manager.get_instance("table_de_bord.menu")
    assert dashboard is not None
    assert dashboard.pages == [page]
    assert dashboard.active_section == "table_de_bord"


def test_hide_and_close_delegate_to_instance():
    manager = _make_manager_with_app()

    widget = manager.open("login")

    manager.hide("login")
    manager.close("login")
    assert widget.hide_calls == 1
    assert widget.close_calls == 1

    manager.hide("table_de_bord.widget")
    assert manager.get_instance("table_de_bord.widget") is None


def test_open_unknown_destination_raises_key_error():
    manager = _make_manager_with_app()

    try:
        manager.open("unknown_destination")
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError for an unknown destination")


def test_document_page_kwargs_drive_on_open_hook():
    manager = _make_manager_with_app()

    page = manager.open("ventes.nouveau_doc", document_id=42)
    assert page.controller.document_id == 42
    assert page.controller.loaded == [42]

    manager.open("ventes.nouveau_doc")
    assert page.controller.document_id is None
    assert page.controller.prepared == 1


def _run_all():
    import traceback

    tests = [
        test_open_window_creates_once_and_reuses,
        test_open_page_uses_dashboard_host_and_syncs_active,
        test_open_page_creates_dashboard_host_when_needed,
        test_hide_and_close_delegate_to_instance,
        test_open_unknown_destination_raises_key_error,
        test_document_page_kwargs_drive_on_open_hook,
    ]

    failed = 0
    for test in tests:
        try:
            test()
        except Exception:
            failed += 1
            traceback.print_exc()
            print(f"FAILED: {test.__name__}")
        else:
            print(f"PASSED: {test.__name__}")

    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_run_all())
