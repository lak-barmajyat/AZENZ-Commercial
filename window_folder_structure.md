## Project structure

new_user/
├── view.py
├── controller.py
├── model.py
├── main.py
└── new_user.ui

### model.py

The Model is responsible only for backend/data/database logic. It knows nothing about Qt or the UI.
```
class NewUserModel:
    def add_user(self, name, email):
        # Database / backend logic goes here
		pass

    def get_users(self):
        # Database query goes here
		pass
```
### view.py

The View is responsible only for the graphical interface.

```
class NewUserView(QWidget):
    def __init__(self):
        super().__init__()

        # Load the UI created with Qt Designer
        uic.loadUi("new_user.ui", self)

		# create the controller
        self.controller = NewUserController(self)

        # UI-related configuration
        self.setup()

	def setup():
		setup_ui()
		setup_table()

    def setup_ui(self):
        self.name_input.clear()
        self.email_input.clear()

	def setup_table(self)
        self.users_table.setColumnCount(2)
        self.users_table.setHorizontalHeaderLabels(
            ["Name", "Email"]
        )

    def clear_form(self):
        self.name_input.clear()
        self.email_input.clear()

    def show_success(self, message):
        self.status_label.setText(message)

    def show_error(self, message):
        self.status_label.setText(message)
```

The View does not contain:
`button.clicked.connect(...)`
It also does not create:
`NewUserModel()`
And it does not contain SQL or database logic.
### controller.py

The Controller connects the View and Model and handles the interaction logic.
```
class Controller:
    def __init__(self, view):
        self.view = view
        self.model = NewUserModel()
		setup():

	def setup():
        self.connect_signals()
        self.fill_entries()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_user)
        self.view.clear_button.clicked.connect(self.clear_form)

    def add_user(self):
        # Get data from the View
        name = self.view.name_input.text().strip()
        email = self.view.email_input.text().strip()

        # Validation
        if not name:
            self.view.show_error("Name is required.")
            return

        if not email:
            self.view.show_error("Email is required.")
            return

        # Call the Model
        success = self.model.add_user(name, email)

        # Handle the result
        if success:
            self.view.show_success("User added successfully.")
            self.view.clear_form()

    def clear_form(self):
        self.view.clear_form()
```
The important part is:
`self.view.add_button.clicked.connect(self.add_user)`
Not:
`self.view.add_button.clicked.connect(self.model.add_user)`
The button calls a Controller method first. The Controller decides what should happen, gets the necessary information from the View, validates it, calls the Model, and then updates the View.

### main.py

The application creates the View and Controller, just to test this window only instead of run entire program.

```
import sys
from PyQt5.QtWidgets import QApplication
from new_user.view import View

app = QApplication(sys.argv)
view = View()
view.show()
sys.exit(app.exec_())

if __name__ == "__main__":
	main()
```

How the interaction works
When the user clicks Add User:

User
  │
  ▼
View
  │
  │ button.clicked
  ▼
Controller.add_user()
  │
  ├── Get name/email from View
  │
  ├── Validate data
  │
  ▼
Model.add_user()
  │
  ├── Database
  │
  ▼
Model returns result
  │
  ▼
Controller
  │
  ▼
View.show_success()

| Class | Responsibility |
| :--- | :--- |
| **View** | UI, widgets, UI configuration, displaying information |
| **Controller** | Signals, user actions, validation, coordination between View and Model |
| **Model** | Database, backend, data processing, business/data logic |
## Naming

### Python classes

Each window/page follows:

```text
{WindowName}View
{WindowName}Controller
{WindowName}Model
```

Examples:

```python
LoginView
LoginController
LoginModel
```

Use `PascalCase` for class names.

### Python methods and variables

Use `snake_case`:

```python
load_document()
prepare_new_document()
connect_signals()
```

### `.ui` widget naming

Widget object names follow:

```text
{WidgetName}{WidgetType}
```

The widget type is the Qt class name without the `Q` prefix:

```text
QPushButton -> Button
QToolButton -> ToolButton
QLabel      -> Label
QLineEdit   -> LineEdit
QTextEdit   -> TextEdit
QComboBox   -> ComboBox
QCheckBox   -> CheckBox
QRadioButton -> RadioButton
QSpinBox    -> SpinBox

Examples:
```

```text
LoginButton
CancelButton
UsernameLineEdit
PasswordLineEdit
DatabaseComboBox
```

---

## Logging

The application logger is configured once globally when the application starts:

```python
logger = setup_logger()
```

```python
import logging

class LoginController:
    def __init__(self, view):
        self.view = view
        self.model = LoginModel()
        self.logger = logging.getLogger("app.login")
```

Then:

```python
    try:
        ...
    except Exception:
        self.logger.exception("Login failed because of an unexpected error")
    self.logger.info("User %s logged in successfully", username)
```

Use child logger names that follow the module/window structure:

```text
app.login
app.table_de_bord
app.ventes.list
app.ventes.nouveau_doc
app.achats.list
app.reglements.nouveau_reglement
```

For example:

```python
self.logger = logging.getLogger("app.ventes.nouveau_doc")
```

This produces useful log entries such as:

```text
2026-08-07 18:20:10 | INFO | app.ventes.nouveau_doc | controller:83 | Creating new document
2026-08-07 18:20:15 | INFO | app.ventes.nouveau_doc | controller:121 | Document 54 saved
2026-08-07 18:20:18 | ERROR | app.ventes.nouveau_doc | controller:130 | Failed to save document
```

### Logging responsibilities

```text
Controller
    Main place for window-specific logging.
    User actions, validation failures, workflow events,
    operation results, and unexpected exceptions.
```