from services.sql.db_connection import with_cursor


class VentesModel:
    def __init__(self):
        pass

    @with_cursor(dictionary=True)
    def get_ventes_documents(self, cursor):

        query = """
            SELECT
            dd.`id`,
            ptd.`nom_type_document` AS `type_document_id`,
            dd.`code_document`,
            dd.`autre_code_document`,
            ddo.`code_document` AS `document_origine_id`,
            dt.`raison_sociale` AS `tier_id`,
            adl.`nom_adresse` AS `adresse_livraison_id`,
            pu.`nom_utilisateur` AS `utilisateur_id`,
            pv.`nom_utilisateur` AS `vendeur_id`,
            dd.`montant_ht`,
            dd.`montant_remise`,
            dd.`montant_net_ht`,
            dd.`montant_tva`,
            dd.`montant_ttc`,
            dd.`montant_net_ttc`,
            dd.`montant_paye`,
            dd.`montant_restant`,
            psd.`nom_statut` AS `statut_document_id`,
            dd.`document_valide`,
            dd.`document_cloture`,
            dd.`date_document`,
            dd.`date_livraison_prevue`,
            dd.`date_livraison_effective`,
            dd.`transforme`,
            dd.`date_transforme`,
            dd.`commentaire`
            FROM `d_documents` AS dd
            LEFT JOIN `d_documents` AS ddo ON dd.document_origine_id = ddo.id
            LEFT JOIN `d_tiers` AS dt ON dd.tier_id = dt.id
            LEFT JOIN `d_adresses_livraison` AS adl ON dd.adresse_livraison_id = adl.id
            LEFT JOIN `p_utilisateurs` AS pu ON dd.utilisateur_id = pu.id
            LEFT JOIN `p_utilisateurs` AS pv ON dd.vendeur_id = pv.id
            LEFT JOIN `p_statuts_documents` AS psd ON dd.statut_document_id = psd.id
            LEFT JOIN `p_types_documents` AS ptd ON dd.type_document_id = ptd.id
            WHERE dd.transforme != 2
        """

        cursor.execute(query)
        result = cursor.fetchall()
        return result
