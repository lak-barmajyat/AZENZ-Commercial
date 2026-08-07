from services.sql.db_connection import with_cursor
from datetime import datetime

from PyQt5.QtCore import QStringListModel, Qt, QDate
from PyQt5.QtWidgets import QCompleter


class VentesController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.setup()

    def setup(self):
        self.load_ventes()

    def load_ventes(self):
        result = self.model.get_ventes_documents()
        for row in result:
            self.view.VentesTable.append_row(
                row
            )
