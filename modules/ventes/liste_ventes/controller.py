import logging

from modules.ventes.liste_ventes.model import VentesModel


class VentesController:
    def __init__(self, view):
        self.view = view
        self.model = VentesModel()
        self.logger = logging.getLogger("app.ventes.list")

        self.setup()

    def setup(self):
        self.connect_signals()
        self.load_ventes()

    def connect_signals(self):
        pass

    def load_ventes(self):
        try:
            result = self.model.get_ventes_documents()
            for row in result:
                self.view.VentesTable.append_row(row)
            self.logger.info("Loaded %d sale documents", len(result))
        except Exception:
            self.logger.exception("Failed to load sale documents")
