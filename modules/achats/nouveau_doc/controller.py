import logging

from modules.achats.nouveau_doc.model import NouveauAchatDocumentModel


class NouveauAchatDocumentController:
    def __init__(self, view):
        self.view = view
        self.model = NouveauAchatDocumentModel()
        self.logger = logging.getLogger("app.achats.nouveau_doc")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
