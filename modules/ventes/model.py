from services.sql.db_connection import with_cursor


class VentesModel:
    def __init__(self):
        pass

    @with_cursor()
    def get_ventes_documents(self, cursor):

        query = """
            SELECT dd.`id`,
            ptd.nom_type_document,
            dd.`reference_document`,
            dt.nom_commercial,
            dd.`utilisateur_id`,
            dd.`vendeur_id`,
            dd.`montant_net_ht`,
            dd.`montant_net_ttc`,
            dd.`montant_restant`,
            psd.nom_statut,
            dd.`document_valide`,
            CASE
                WHEN dd.document_cloture = 1 THEN '🔒'
                WHEN dd.document_valide = 1 THEN '✅'
                ELSE ' ' END AS statut_icone,
            dd.`document_cloture`,
            dd.`date_document`,
            dd.`transforme`
            FROM `d_documents` AS dd
            LEFT JOIN `d_tiers` AS dt ON dd.tier_id = dt.id
            LEFT JOIN `p_statuts_documents` AS psd ON dd.statut_document_id = psd.id
            LEFT JOIN `p_types_documents` AS ptd ON dd.type_document_id = ptd.id WHERE dd.transforme != 2
        """

        cursor.execute(query)
        result = cursor.fetchall()
        return result

