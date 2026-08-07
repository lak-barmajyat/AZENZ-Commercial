from PyQt5.QtCore import QStringListModel, Qt, QDate
from PyQt5.QtWidgets import QCompleter
from datetime import datetime


class NouveauDocumentController:
    def __init__(self, view, model, document_id=None):
        self.view = view
        self.model = model
        self.document_id = document_id

        self.setup()

    def setup(self):
        self.fill_entries()
        self.connect_signals()
        self.setup_document_lines_widget()
        if self.document_id:
            self.load_document(self.document_id)

    def update_widgets(self):
        pass

    def prepare_new_document(self):
        self.document_id = None
        self.view.TypeDocComboBox.setCurrentIndex(0)
        self.on_type_selection_change()
        self.view.ReferenceEntry.clear()
        self.view.EtatDocComboBox.setCurrentIndex(0)
        self.view.AffairecomboBox.setCurrentIndex(-1)
        self.view.DateDocDateEdit.setDate(datetime.now().date())
        self.view.ClientcomboBox.setCurrentText("")
        self.view.CodeClientEntry.clear()
        self.view.DocumentLinesWidget.set_lines([])

    def fill_entries(self):
        # fill type document combobox
        items = self.model.get_types_documents()
        for id, nom_type_document in items:
            self.view.TypeDocComboBox.addItem(nom_type_document, id)

        # fill numero document
        selected_id = self.view.TypeDocComboBox.currentData()
        self.view.NumeroDocEntry.setText(self.model.generate_doc_code(selected_id))

        # fill Etat document combobox
        items = self.model.get_etats_documents(selected_id)
        for id, nom_statut in items:
            self.view.EtatDocComboBox.addItem(nom_statut, id)
        
        # fill Affaires combobox
        items = self.model.get_affaires()
        for id, nom_affaire in items:
            self.view.AffairecomboBox.addItem(nom_affaire, id)

        # fill date entry with current date
        self.view.DateDocDateEdit.setDate(datetime.now().date())

        # fill client searchable combo box
        self.fill_client_searchable_combo()

        # fill code client entry based on selected client
        self.on_client_selection_change()

    def connect_signals(self):
        self.view.TypeDocComboBox.currentIndexChanged.connect(self.on_type_selection_change)
        self.view.ClientcomboBox.currentIndexChanged.connect(self.on_client_selection_change)
        self.view.ClientcomboBox.lineEdit().editingFinished.connect(self.on_client_selection_change)
        # update client name when I hit enter or tab in the code client entry
        self.view.CodeClientEntry.editingFinished.connect(self.on_code_client_change)


    def on_type_selection_change(self):
        # update Numero document based on selected type document
        selected_id = self.view.TypeDocComboBox.currentData()
        self.view.NumeroDocEntry.setText(self.model.generate_doc_code(selected_id))

        # update Etat document combobox based on selected type document
        self.view.EtatDocComboBox.clear()
        items = self.model.get_etats_documents(selected_id)
        for id, nom_statut in items:
            self.view.EtatDocComboBox.addItem(nom_statut, id)

    def on_client_selection_change(self):
        client = self.view.ClientcomboBox.currentText()
        code_tier = self.model.get_new_client_code(client)
        self.view.CodeClientEntry.setText(code_tier)
        self.on_code_client_change()
    
    def on_code_client_change(self):
        code_tier = self.view.CodeClientEntry.text()
        client_name = self.model.get_client_by_code(code_tier)
        self.view.ClientcomboBox.setCurrentText(client_name)
        client = self.view.ClientcomboBox.currentText()
        code_tier = self.model.get_new_client_code(client)
        self.view.CodeClientEntry.setText(code_tier)

    def fill_client_searchable_combo(self):
        items = self.model.get_clients()

        model = QStringListModel(items, self.view.ClientcomboBox)
        self.view.ClientcomboBox.setModel(model)

        completer = QCompleter(model, self.view.ClientcomboBox)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)

        # Keep keyboard focus inside the input field
        completer.popup().setFocusPolicy(Qt.NoFocus)

        self.view.ClientcomboBox.setCompleter(completer)
    
    def setup_document_lines_widget(self):
        widget = self.view.DocumentLinesWidget

        # General behavior
        widget.set_editable(True)
        widget.set_read_only(False)
        widget.set_tax_enabled(True)
        widget.set_discount_enabled(True)

        # Defaults used when creating new lines
        widget.set_default_vat_percent(0.0)
        widget.set_default_unit("Unit")
        widget.set_vat_rates([0.0, 5.5, 10.0, 20.0])

        # Display formatting
        widget.set_number_format(decimals=2, thousands_sep=" ")

        # Toolbar configuration. Available action keys are:
        # "add_text", "barcode_scan", and "check_stock".
        widget.set_toolbar_visible(True)
        for action_key in ("add_text", "barcode_scan", "check_stock"):
            widget.set_toolbar_action_visible(action_key, True)
            widget.set_toolbar_action_enabled(action_key, True)

        # Article search / placeholder row
        widget.set_placeholder_text("Search or type article...")
        widget.set_search_min_chars(1)
        widget.set_search_debounce_ms(250)

        # Add per-line validation callbacks here when needed.
        widget.set_validation_rules([])

        currency = self.model.get_currency_symbol()
        widget.set_currency_symbol(currency)

        units = self.model.get_units()
        widget.set_units(units)

        lines = self.model.get_document_lines(self.document_id)
        widget.set_lines(lines)

        # Connect document-level signals to your controller. Searchable column
        # providers are configured by the view through widget.set_list().
        widget.totalsChanged.connect(self.on_totals_changed)

    def load_document(self, document_id):
        document = self.model.get_document(document_id)
        if not document:
            return

        self.view.TypeDocComboBox.setCurrentIndex(
            self.view.TypeDocComboBox.findData(document.get("type_document_id"))
        )
        self.view.NumeroDocEntry.setText(document.get("code_document") or "")
        if document.get("autre_code_document") is not None:
            self.view.ReferenceEntry.setText(document.get("autre_code_document") or "")
        self.view.EtatDocComboBox.setCurrentIndex(
            self.view.EtatDocComboBox.findData(document.get("statut_document_id"))
        )
        self.view.AffairecomboBox.setCurrentIndex(-1)
        date_value = document.get("date_document")
        if hasattr(date_value, "date"):
            date_value = date_value.date()
        if date_value:
            self.view.DateDocDateEdit.setDate(QDate(date_value.year, date_value.month, date_value.day))
        else:
            self.view.DateDocDateEdit.setDate(QDate.currentDate())
        self.view.ClientcomboBox.setCurrentText(document.get("tier_name") or "")
        self.view.CodeClientEntry.setText(document.get("tier_code") or "")

        self.view.DocumentLinesWidget.set_lines(self.model.get_document_lines(document_id))

    def on_totals_changed(self):
        # Implement your totals changed logic here
        pass
