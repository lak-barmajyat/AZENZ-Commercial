from ui_utils.effects import set_drop_shadow

from ui_utils.loader import load_ui as loadUi
from PyQt5.QtWidgets import QApplication, QWidget

from modules.table_de_bord.widget.controller import DashboardWidgetController


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/table_de_bord/widget/dashboard_widget.ui", self)

        self.setup()
        self.controller = DashboardWidgetController(self)

    def setup(self):
        self.setup_effects()
        self.setup_navigation()

    def setup_effects(self):
        card_frames = [
            self.CardArticles,
            self.CardClients,
            self.CardDocuments,
            self.CardPaiements,
        ]
        for frame in card_frames:
            set_drop_shadow(frame, 15, 0, 1, 35)

    def setup_navigation(self):
        app = QApplication.instance()
        if app is None or not hasattr(app, "window_manager"):
            return

        window_manager = app.window_manager
        self.ListeVentesButton.clicked.connect(
            lambda: window_manager.open("ventes.list")
        )
        self.NouveauDocButton.clicked.connect(
            lambda: window_manager.open("ventes.nouveau_doc")
        )
        self.AjouterPaiementButton.clicked.connect(
            lambda: window_manager.open("reglements.nouveau_reglement")
        )
