from dataclasses import dataclass
from typing import Any, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from modules.login.view import LoginView
from modules.table_de_bord.menu.view import DashboardMenuView
from modules.table_de_bord.widget.view import DashboardWidget
from modules.ventes.liste_ventes.view import VentesView
from modules.ventes.nouveau_doc.view import NouveauDocumentView
from modules.achats.liste_achats.view import AchatsView
from modules.achats.nouveau_doc.view import NouveauAchatDocumentView
from modules.reglements.liste_reglements.view import ReglementsView
from modules.reglements.nouveau_reglement.view import NouveauReglementView
from modules.articles.liste_articles.view import ListeArticlesView
from modules.articles.nouveau_article.view import NouveauArticleView
from modules.familles.liste_familles.view import ListeFamillesView
from modules.familles.nouveau_famille.view import NouveauFamilleView
from modules.stockage.liste_stockage.view import ListeStockageView
from modules.stockage.nouveau_mouvement.view import NouveauMouvementView
from modules.clients.liste_clients.view import ListeClientsView
from modules.clients.nouveau_client.view import NouveauClientView
from modules.fournisseurs.liste_fournisseurs.view import ListeFournisseursView
from modules.fournisseurs.nouveau_fournisseur.view import NouveauFournisseurView
from modules.parameters.liste_parameters.view import ListeParametersView


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
                NouveauAchatDocumentView,
                "page",
                section="achats",
            ),

            "articles.list": Destination(
                ListeArticlesView,
                "page",
                section="articles",
            ),

            "articles.nouveau_article": Destination(
                NouveauArticleView,
                "page",
                section="articles",
            ),

            "familles.list": Destination(
                ListeFamillesView,
                "page",
                section="familles",
            ),

            "familles.nouveau_famille": Destination(
                NouveauFamilleView,
                "page",
                section="familles",
            ),

            "stockage.list": Destination(
                ListeStockageView,
                "page",
                section="stockage",
            ),

            "stockage.nouveau_mouvement": Destination(
                NouveauMouvementView,
                "page",
                section="stockage",
            ),

            "clients.list": Destination(
                ListeClientsView,
                "page",
                section="clients",
            ),

            "clients.nouveau_client": Destination(
                NouveauClientView,
                "page",
                section="clients",
            ),

            "fournisseurs.list": Destination(
                ListeFournisseursView,
                "page",
                section="fournisseurs",
            ),

            "fournisseurs.nouveau_fournisseur": Destination(
                NouveauFournisseurView,
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
                ListeParametersView,
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