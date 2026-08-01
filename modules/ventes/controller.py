from services.sql.db_connection import with_cursor
from services.ndoc_generator import generate_document_number
from datetime import datetime

from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtWidgets import QCompleter


class VentesController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.setup()

    def load_ventes(self):
        print("Loading ventes documents...")
        result = self.model.get_ventes_documents()
        print(f"Loaded {result} ventes documents.")
        for row in result:
            (
                id,
                nom_type_document,
                reference_document,
                nom_commercial,
                utilisateur_id,
                vendeur_id,
                montant_net_ht,
                montant_net_ttc,
                montant_restant,
                nom_statut,
                document_valide,
                statut_icon,
                document_cloture,
                date_document,
                transforme,
            ) = row
            self.view.VentesTable.append_row(
                {
                    "id": id,
                    "utilisateur_id": utilisateur_id,
                    "vendeur_id": vendeur_id,
                    "type": nom_type_document,
                    "numero_document": reference_document,
                    "icon": statut_icon,
                    "date": date_document,
                    "client": nom_commercial,
                    "total_ht": montant_net_ht,
                    "total_ttc": montant_net_ttc,
                    "solde": montant_restant,
                    "statut": nom_statut,
                }
            )

    def setup(self):
        self.load_ventes()


class NouveauDocumentController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.setup()

    def setup(self):
        self.fill_entries()
        self.connect_signals()

    def fill_entries(self):
        # fill type document combobox
        items = self.model.get_types_documents()
        for id, nom_type_document in items:
            self.view.TypeDocComboBox.addItem(nom_type_document, id)

        # fill numero document
        selected_id = self.view.TypeDocComboBox.currentData()
        self.view.NumeroDocEntry.setText(generate_document_number(selected_id))

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
        self.view.ClientcomboBox.lineEdit().textChanged.connect(self.on_client_selection_change)
        # update client name when I hit enter or tab in the code client entry
        self.view.CodeClientEntry.editingFinished.connect(self.on_code_client_change)


    def on_type_selection_change(self):
        # update Numero document based on selected type document
        selected_id = self.view.TypeDocComboBox.currentData()
        self.view.NumeroDocEntry.setText(generate_document_number(selected_id))

        # update Etat document combobox based on selected type document
        self.view.EtatDocComboBox.clear()
        items = self.model.get_etats_documents(selected_id)
        for id, nom_statut in items:
            self.view.EtatDocComboBox.addItem(nom_statut, id)

    def on_client_selection_change(self):
        client = self.view.ClientcomboBox.currentText()
        code_tier = self.model.get_new_client_code(client)
        self.view.CodeClientEntry.setText(code_tier)
    
    def on_code_client_change(self):
        code_tier = self.view.CodeClientEntry.text()
        client_name = self.model.get_client_by_code(code_tier)
        self.view.ClientcomboBox.setCurrentText(client_name)

    def fill_client_searchable_combo(self):
        self.view.ClientcomboBox.setEditable(True)
        self.view.ClientcomboBox.setInsertPolicy(self.view.ClientcomboBox.NoInsert)
        self.view.ClientcomboBox.setCurrentIndex(-1)
        self.view.ClientcomboBox.lineEdit().setPlaceholderText("Type to search...")

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
        lines = self.model.get_document_lines()
        self.view.DocumentLinesWidget.set_lines(lines)
