from ui_utils.effects import set_drop_shadow
from ui_utils.canvas import create_uniform_icon, get_colored_icon

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QPropertyAnimation, QEasingCurve, Qt

from PyQt5.QtWidgets import (
    QAction, QFrame, QMainWindow, QWidget,
    QLineEdit, QToolButton, QHeaderView, QVBoxLayout, QLabel)

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

        self.group_states = {
            self.TiersGFrame: True,
            self.DocumentsGFrame: True,
            self.CatalogueGFrame: True,
        }

        self.group_button_frames = {
            self.TiersGButton: self.TiersGFrame,
            self.DocumentsGButton: self.DocumentsGFrame,
            self.CatalogueGButton: self.CatalogueGFrame,
            self.toggleSidebarButton: True
        }

        self.setup()

    def setup(self):
        self.setup_widgets()
        self.setup_sidebar_buttons()
        self.setup_widgets_stock()
        self.setup_signals()
        self.setup_window()

        # Functions need call
        self.mark_button(self.DashboardButton)
        self.toggle_group(self.DocumentsGFrame)
        self.toggle_group(self.TiersGFrame)
        self.toggle_group(self.CatalogueGFrame)

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
        if self.WidgetStock.count() > 0:
            return

        self.sidebar_widget_map = {}

        def create_placeholder(button):
            title = button.text().strip() or button.objectName()
            placeholder = QWidget()
            layout = QVBoxLayout(placeholder)
            layout.setContentsMargins(0, 0, 0, 0)
            label = QLabel(title)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            return placeholder

        def add_page(button, widget=None):
            if widget is None:
                widget = create_placeholder(button)
            self.WidgetStock.addWidget(widget)
            self.sidebar_widget_map[button] = widget
            button.clicked.connect(
                lambda _checked=False, b=button: self.WidgetStock.setCurrentWidget(self.sidebar_widget_map[b])
            )

        dashboard_widget = DashboardWidget()
        ventes_widget = VentesView()

        add_page(self.DashboardButton, dashboard_widget)
        add_page(self.VentesButton, ventes_widget)
        add_page(dashboard_widget.ListeVentesButton, ventes_widget)
        add_page(self.ClientsButton)
        add_page(self.FournisseursButton)
        add_page(self.ArticlesButton)
        add_page(self.FamillesButton)
        add_page(self.AchatsButton)
        add_page(self.StockageButton)
        add_page(self.PaiementsButton)
        add_page(self.SettingsButton)

        self.WidgetStock.setCurrentWidget(dashboard_widget)

    def setup_signals(self):
        self.toggleSidebarButton.clicked.connect(self.toggle_sidebar)
        self.TiersGButton.clicked.connect(
            lambda: self.toggle_group(self.TiersGFrame)
        )

        self.DocumentsGButton.clicked.connect(
            lambda: self.toggle_group(self.DocumentsGFrame)
        )

        self.CatalogueGButton.clicked.connect(
            lambda: self.toggle_group(self.CatalogueGFrame)
        )

    # ------------------------ Helper Functions ----------------------- #
    def mark_button(self, button):
        # Unmark all buttons first
        sidebar_buttons = self.SidebarFrame.findChildren(QToolButton)
        for widget in sidebar_buttons:
            if self.group_button_frames.get(widget) is not None:
                continue  # Skip group buttons, they will be handled separately
            widget.setChecked(False)
            gray_icon = get_colored_icon(widget.icon(), "#434655", widget.iconSize())
            widget.setIcon(gray_icon)

        frame = self.group_button_frames.get(button)
        if frame is not None and self.group_states.get(frame, False):
            # If it's a group button and its group is open, keep it marked
            button_state = button.isChecked()
            if button_state:
                blue_icon = get_colored_icon(button.icon(), "#0051DF", button.iconSize())
                button.setIcon(blue_icon)
            else:
                gray_icon = get_colored_icon(button.icon(), "#434655", button.iconSize())
                button.setIcon(gray_icon)

            button.setChecked(not button_state)
            return
            

        # Mark the clicked button
        button.setChecked(True)
        blue_icon = get_colored_icon(button.icon(), "#0051DF", button.iconSize())
        button.setIcon(blue_icon)

    def toggle_group(self, frame):
        is_open = self.group_states.get(frame, False)

        if is_open:
            start_height = frame.height()
            end_height = 0
        else:
            start_height = 0
            end_height = frame.layout().sizeHint().height()

        animation = QPropertyAnimation(frame, b"maximumHeight")
        animation.setDuration(220)
        animation.setStartValue(start_height)
        animation.setEndValue(end_height)
        animation.setEasingCurve(QEasingCurve.InOutCubic)
        animation.start()

        frame.animation = animation
        self.group_states[frame] = not is_open

    def toggle_sidebar(self):
        current_width = self.SidebarFrame_.width()

        closing = self.sidebar_open
        target_width = self.sidebar_collapsed_width if closing else self.sidebar_expanded_width

        self.animation = QPropertyAnimation(self.SidebarFrame_, b"maximumWidth")
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