import logging

from modules.table_de_bord.widget.model import DashboardWidgetModel


class DashboardWidgetController:
    def __init__(self, view):
        self.view = view
        self.model = DashboardWidgetModel()
        self.logger = logging.getLogger("app.table_de_bord.widget")

        self.setup()

    def setup(self):
        self.connect_signals()

    def connect_signals(self):
        pass
