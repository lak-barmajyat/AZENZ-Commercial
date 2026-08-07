import sys

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QCompleter,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class SearchableComboBox(QComboBox):
    def __init__(self, items, parent=None):
        super().__init__(parent)

        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setCurrentIndex(-1)

        self.lineEdit().setPlaceholderText("Type to search...")

        # Model containing all available items
        model = QStringListModel(items, self)

        # The normal combo box list
        self.setModel(model)

        # Filtered suggestions shown while typing
        completer = QCompleter(model, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)

        # Prevent the suggestion list from stealing keyboard focus
        completer.popup().setFocusPolicy(Qt.NoFocus)

        self.setCompleter(completer)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Searchable ComboBox")
        self.resize(350, 130)

        items = [
            "Apple",
            "Apricot",
            "Banana",
            "Blueberry",
            "Cherry",
            "Grape",
            "Mango",
            "Orange",
            "Peach",
            "Pineapple",
            "Strawberry",
            "Watermelon",
        ]

        self.combo = SearchableComboBox(items)

        self.result_label = QLabel("Selected: nothing")

        self.combo.currentTextChanged.connect(
            lambda text: self.result_label.setText(
                f"Selected: {text}" if text else "Selected: nothing"
            )
        )

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Search for a fruit:"))
        layout.addWidget(self.combo)
        layout.addWidget(self.result_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())