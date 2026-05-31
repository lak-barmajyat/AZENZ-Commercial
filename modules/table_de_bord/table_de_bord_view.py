from ui_utils.effects import set_drop_shadow
from ui_utils.canvas import create_uniform_icon, get_colored_icon

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QPropertyAnimation, QEasingCurve

from PyQt5.QtWidgets import (
    QAction, QFrame, QMainWindow, QWidget,
    QLineEdit, QToolButton, QHeaderView)

from modules.ventes.ventes_view import VentesView


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("modules/table_de_bord/dashboard_widget.ui", self)
        self.setup()

    def setup(self):
        self.setup_effects()

    def setup_icons(self):
        # Change icon size in toolbuttons
        card_frames = [self.CardArticles, self.CardClients, self.CardDocuments, self.CardPaiements]
        for frame in card_frames:
            buttons = frame.findChild(QToolButton)
            if buttons:
                for button in buttons:
                    button.setIconSize(QSize(40, 40))


    def setup_effects(self):
        card_frames = [self.CardArticles, self.CardClients, self.CardDocuments, self.CardPaiements]
        for frame in card_frames:
            set_drop_shadow(frame, 15, 0, 1, 35)

class DashboardMenuView(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("modules/table_de_bord/dashboard_menu.ui", self)

        self.sidebar_open = True
        self.sidebar_expanded_width = 250
        self.sidebar_collapsed_width = 65

        self.toggleSidebarButton.clicked.connect(self.toggle_sidebar)

        self.setup()

    def setup(self):
        self.setup_widgets()
        self.setup_sidebar_buttons()
        self.mark_button(self.DashboardButton)
        self.setup_widgets_stock()
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("AZENZ - Dashboard")
        self.setWindowIcon(QIcon(":/icons/resources/icons/app_icon.svg"))
        self.showMaximized()

    def setup_widgets(self):
        # For Rechercher Field
        rechercher_icon = QAction(self)
        rechercher_icon.setIcon(create_uniform_icon(":/icons/icons/rechercher.svg"))
        self.RechercherEntry.addAction(rechercher_icon, QLineEdit.LeadingPosition)

    def setup_sidebar_buttons(self):
        sidebar_buttons = self.SidebarFrame.findChildren(QToolButton)
        for w in sidebar_buttons:
            w.clicked.connect(lambda _checked=False, w=w: self.mark_button(w))

    def setup_widgets_stock(self):
        dashboard_widget = DashboardWidget()
        ventes_widget = VentesView()
        self.WidgetStock.layout().addWidget(ventes_widget)
        self.WidgetStock.layout().addWidget(dashboard_widget)
        self.WidgetStock.setCurrentWidget(ventes_widget)

    # ------------------------ Helper Functions ----------------------- #
    def mark_button(self, button):
        # Unmark all buttons first
        sidebar_buttons = self.SidebarFrame.findChildren(QToolButton)
        for widget in sidebar_buttons:
            widget.setChecked(False)
            gray_icon = get_colored_icon(widget.icon(), "#434655", widget.iconSize())
            widget.setIcon(gray_icon)

        # Mark the clicked button
        button.setChecked(True)
        blue_icon = get_colored_icon(button.icon(), "#0051DF", button.iconSize())
        button.setIcon(blue_icon)

    def toggle_sidebar(self):
        current_width = self.SidebarFrame.width()

        if self.sidebar_open:
            target_width = self.sidebar_collapsed_width
        else:
            target_width = self.sidebar_expanded_width

        self.animation = QPropertyAnimation(self.SidebarFrame, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(current_width)
        self.animation.setEndValue(target_width)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start()

        self.sidebar_open = not self.sidebar_open


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dashboard_menu_window = DashboardMenuView()
    dashboard_menu_window.show()
    sys.exit(app.exec_())