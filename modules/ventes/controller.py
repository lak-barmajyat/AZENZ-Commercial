

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
            (id,
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
             transforme) = row
            self.view.VentesTable.append_row({
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
            })


    def setup(self):
        self.load_ventes()