from ui.tools.effects import set_drop_shadow
from ui.tools.canvas import create_uniform_icon, get_colored_icon

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui

from PyQt5.QtWidgets import (
    QAction, QFrame, QMainWindow, QWidget,
    QLineEdit, QToolButton)


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("ui/screens/dashboard/dashboard_widget.ui", self)
        self.setup()

    def setup(self):
        self.setup_widgets()

    def setup_widgets(self):
        cards = [self.CardClients, self.CardDocuments, self.CardPaiements, self.CardArticles]
        for card in cards:
            card.setProperty("class", "card")
            for child in card.findChildren(QToolButton):
                child.setProperty("class", "card-button")


class DashboardMenuUI(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/screens/dashboard/dashboard_menu.ui", self)
        self.setup()

    def setup(self):
        self.setup_widgets()
        # self.setup_icons()
        self.setup_sidebar_buttons()
        self.mark_button(self.DashboardButton)
        self.setup_widgets_stock()

    def setup_widgets(self):
        sidebar_buttons = self.SidebarFrame.findChildren(QToolButton)
        sidebar_buttons += self.FootSidebarFrame.findChildren(QToolButton)
        for widget in sidebar_buttons:
            widget.setProperty("class", "sidebar-button")
        self.RechercherEntry.setProperty("class", "icon-lineedit")
        self.HelpButton.setProperty("class", "icon-button")

        # For Rechercher Field
        rechercher_icon = QAction(self)
        rechercher_icon.setIcon(create_uniform_icon(":/icons/resources/icons/rechercher.svg"))
        self.RechercherEntry.addAction(rechercher_icon, QLineEdit.LeadingPosition)

    def setup_icons(self):
        self.DashboardButton.setIcon(create_uniform_icon(":/icons/resources/icons/dashboard.svg", 20))

    def setup_sidebar_buttons(self):
        sidebar_buttons = self.SidebarFrame.findChildren(QToolButton)
        sidebar_buttons += self.FootSidebarFrame.findChildren(QToolButton)
        for w in sidebar_buttons:
            w.clicked.connect(lambda _checked=False, w=w: self.mark_button(w))

    def setup_widgets_stock(self):
        dashboard_widget = DashboardWidget()
        self.WidgetStock.layout().addWidget(dashboard_widget)
        self.WidgetStock.setCurrentWidget(dashboard_widget)

    # ------------------------ Helper Functions ----------------------- #
    def mark_button(self, button):
        # Unmark all buttons first
        sidebar_buttons = self.SidebarFrame.findChildren(QToolButton)
        sidebar_buttons += self.FootSidebarFrame.findChildren(QToolButton)
        for widget in sidebar_buttons:
            widget.setChecked(False)
            gray_icon = get_colored_icon(widget.icon(), "#434655", widget.iconSize())
            widget.setIcon(gray_icon)

        # Mark the clicked button
        button.setChecked(True)
        blue_icon = get_colored_icon(button.icon(), "#0051DF", button.iconSize())
        button.setIcon(blue_icon)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dashboard_menu_window = DashboardMenuUI()
    dashboard_menu_window.show()
    sys.exit(app.exec_())