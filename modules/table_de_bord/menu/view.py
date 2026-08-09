from ui_utils.canvas import create_uniform_icon, get_colored_icon

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QLineEdit,
    QMainWindow,
    QToolButton,
)

from modules.table_de_bord.menu.controller import DashboardMenuController


class DashboardMenuView(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("modules/table_de_bord/menu/dashboard_menu.ui", self)

        self.sidebar_open = True
        self.sidebar_expanded_width = 250
        self.sidebar_collapsed_width = 60

        self.group_states = {
            self.TiersGFrame: True,
            self.DocumentsGFrame: True,
            self.CatalogueGFrame: True,
        }

        self.group_button_frames = {
            self.TiersGButton: self.TiersGFrame,
            self.DocumentsGButton: self.DocumentsGFrame,
            self.CatalogueGButton: self.CatalogueGFrame,
            self.ToggleSidebarToolButton: True,
        }

        self._active_section_buttons = {
            "table_de_bord": self.DashboardButton,
            "ventes": self.VentesButton,
            "clients": self.ClientsButton,
            "fournisseurs": self.FournisseursButton,
            "articles": self.ArticlesButton,
            "familles": self.FamillesButton,
            "achats": self.AchatsButton,
            "stockage": self.StockageButton,
            "reglements": self.PaiementsButton,
            "parameters": self.SettingsButton,
        }

        self._sidebar_destinations = {
            self.DashboardButton: "table_de_bord.widget",
            self.VentesButton: "ventes.list",
            self.ClientsButton: "clients.list",
            self.FournisseursButton: "fournisseurs.list",
            self.ArticlesButton: "articles.list",
            self.FamillesButton: "familles.list",
            self.AchatsButton: "achats.list",
            self.StockageButton: "stockage.list",
            self.PaiementsButton: "reglements.list",
            self.SettingsButton: "parameters.list",
        }

        self.setup()
        self.controller = DashboardMenuController(self)

    def setup(self):
        self.setup_widgets()
        self.setup_sidebar_buttons()
        self.setup_sidebar_groups()
        self.setup_window()

        # Functions need call
        self.mark_button(self.DashboardButton)
        self.toggle_group(self.DocumentsGFrame)
        self.toggle_group(self.TiersGFrame)
        self.toggle_group(self.CatalogueGFrame)

    def setup_window(self):
        self.setWindowTitle("AZENZ - Dashboard")
        self.setWindowIcon(QIcon(":/images/images/program_logo.png"))
        self.showMaximized()

    def setup_widgets(self):
        # For Rechercher Field
        rechercher_icon = QAction(self)
        rechercher_icon.setIcon(create_uniform_icon(":/icons/icons/rechercher.svg"))
        self.RechercherLineEdit.addAction(rechercher_icon, QLineEdit.LeadingPosition)

    def setup_sidebar_buttons(self):
        for button, destination in self._sidebar_destinations.items():
            button.clicked.connect(
                lambda _checked=False, b=button, dest=destination: self._navigate(b, dest)
            )

    def setup_sidebar_groups(self):
        self.TiersGButton.clicked.connect(
            lambda: self.toggle_group(self.TiersGFrame)
        )

        self.DocumentsGButton.clicked.connect(
            lambda: self.toggle_group(self.DocumentsGFrame)
        )

        self.CatalogueGButton.clicked.connect(
            lambda: self.toggle_group(self.CatalogueGFrame)
        )

        self.ToggleSidebarToolButton.clicked.connect(self.toggle_sidebar)

    def _navigate(self, button, destination):
        self.mark_button(button)

        app = QApplication.instance()
        if app is None or not hasattr(app, "window_manager"):
            return

        app.window_manager.open(destination)

    def show_page(self, page_widget):
        if page_widget is None:
            return

        if self.PagesWidget.indexOf(page_widget) == -1:
            self.PagesWidget.addWidget(page_widget)
        self.PagesWidget.setCurrentWidget(page_widget)

    def set_active_section(self, section):
        sidebar_buttons = self.SidebarFrame.findChildren(QToolButton)
        for widget in sidebar_buttons:
            if self.group_button_frames.get(widget) is not None:
                continue
            widget.setChecked(False)
            gray_icon = get_colored_icon(widget.icon(), "#434655", widget.iconSize())
            widget.setIcon(gray_icon)

        button = self._active_section_buttons.get(section)
        if button is None:
            return

        button.setChecked(True)
        blue_icon = get_colored_icon(button.icon(), "#0051DF", button.iconSize())
        button.setIcon(blue_icon)

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
