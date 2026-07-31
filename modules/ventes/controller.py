from services.sql.db_connection import with_cursor


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
        items = self.model.fill_type_combo()
        for id, nom_type_document in items:
            self.view.TypeDocComboBox.addItem(nom_type_document, id)

        # fill numero document
        # self.view.NumeroDocEntry.setText(get_next_docu)

    def connect_signals(self):
        self.view.TypeDocComboBox.currentIndexChanged.connect(self.on_selection_change)

    def on_selection_change(self):
        # Retrieve the data
        current_text = self.view.TypeDocComboBox.currentText()
        custom_id = self.view.TypeDocComboBox.currentData()
        positional_index = self.view.TypeDocComboBox.currentIndex()

        # Display the results
        print(
            f"Selected: {current_text}\n"
            f"PyQt Positional Index: {positional_index}\n"
            f"Your Custom Data Index: {custom_id}"
        )

