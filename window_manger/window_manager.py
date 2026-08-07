from dataclasses import dataclass
from typing import Any, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from modules.login.login_view import LoginView
from modules.table_de_bord.table_de_bord_view import (
    DashboardMenuView,
    DashboardWidget,
)
from modules.ventes.liste_ventes.view import VentesView
from modules.ventes.nouveau_doc.view import NouveauDocumentView
from modules.achats.achats_view import AchatsView
from modules.reglements.reglements_view import (
    NouveauReglementView,
    ReglementsView,
)


@dataclass
class Destination:
    view: Callable[[], QWidget] | None
    type: str
    section: str | None = None

    on_open: Callable | None = None
    on_close: Callable | None = None
    on_hide: Callable | None = None

    instance: QWidget | None = None


class WindowManager:
    def __init__(self):
        self._windows: dict[str, Destination] = {

            "login": Destination(
                LoginView,
                "window",
            ),

            "table_de_bord.menu": Destination(
                DashboardMenuView,
                "window",
            ),

            "table_de_bord.widget": Destination(
                DashboardWidget,
                "page",
                section="table_de_bord",
            ),

            "ventes.list": Destination(
                VentesView,
                "page",
                section="ventes",
            ),

            "ventes.nouveau_doc": Destination(
                NouveauDocumentView,
                "page",
                section="ventes",
                on_open=self._open_nouveau_document,
            ),

            "achats.list": Destination(
                AchatsView,
                "page",
                section="achats",
            ),

            "achats.nouveau_doc": Destination(
                None,
                "page",
                section="achats",
            ),

            "articles.list": Destination(
                None,
                "page",
                section="articles",
            ),

            "articles.nouveau_article": Destination(
                None,
                "page",
                section="articles",
            ),

            "familles.list": Destination(
                None,
                "page",
                section="familles",
            ),

            "familles.nouveau_famille": Destination(
                None,
                "page",
                section="familles",
            ),

            "stockage.list": Destination(
                None,
                "page",
                section="stockage",
            ),

            "stockage.nouveau_mouvement": Destination(
                None,
                "page",
                section="stockage",
            ),

            "clients.list": Destination(
                None,
                "page",
                section="clients",
            ),

            "clients.nouveau_client": Destination(
                None,
                "page",
                section="clients",
            ),

            "fournisseurs.list": Destination(
                None,
                "page",
                section="fournisseurs",
            ),

            "fournisseurs.nouveau_fournisseur": Destination(
                None,
                "page",
                section="fournisseurs",
            ),

            "reglements.list": Destination(
                ReglementsView,
                "page",
                section="reglements",
            ),

            "reglements.nouveau_reglement": Destination(
                NouveauReglementView,
                "page",
                section="reglements",
            ),

            "parameters.list": Destination(
                None,
                "page",
                section="parameters",
            ),
        }

    def open(self, name: str, **kwargs) -> QWidget:
        destination = self._windows[name]
        instance = self._get_or_create(name)

        if destination.on_open:
            destination.on_open(instance, kwargs)

        if destination.type == "window":
            instance.showMaximized()
            return instance

        dashboard = self._get_or_create("table_de_bord.menu")
        dashboard.show_page(instance)

        dashboard.set_active_section(
            destination.section or name
        )

        return instance

    def hide(self, name: str) -> None:
        destination = self._windows[name]

        if destination.instance is None:
            return

        if destination.on_hide:
            destination.on_hide(destination.instance)

        destination.instance.hide()

    def close(self, name: str) -> None:
        destination = self._windows[name]

        if destination.instance is None:
            return

        if destination.on_close:
            destination.on_close(destination.instance)

        destination.instance.close()

    def get_instance(self, name: str) -> QWidget | None:
        return self._windows[name].instance

    def _get_or_create(self, name: str) -> QWidget:
        destination = self._windows[name]

        if destination.instance is None:
            if destination.view is None:
                destination.instance = self._placeholder(name)
            else:
                destination.instance = destination.view()

        return destination.instance

    @staticmethod
    def _placeholder(name: str) -> QWidget:
        widget = QWidget()

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(
            f"{name}\n\n"
            "This page will be implemented in the next version inchaallah"
        )
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)

        return widget

    def _open_nouveau_document(
        self,
        widget: NouveauDocumentView,
        kwargs: dict[str, Any],
    ) -> None:
        document_id = kwargs.get("document_id")

        widget.controller.document_id = document_id

        if document_id:
            widget.controller.load_document(document_id)
        else:
            widget.controller.prepare_new_document()