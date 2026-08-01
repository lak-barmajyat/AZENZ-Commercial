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

class NouveauDocumentModel:
    def __init__(self):
        pass

    @with_cursor()
    def get_types_documents(self, cursor=None):
        query = """SELECT id, nom_type_document FROM p_types_documents WHERE domaine = 'VENTE'"""
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    @with_cursor()
    def get_etats_documents(self, type_document_id, cursor=None):
        query = """SELECT id, nom_statut FROM p_statuts_documents WHERE type_document_id = %s"""
        cursor.execute(query, (type_document_id,))
        result = cursor.fetchall()
        return result
    
    @with_cursor()
    def get_affaires(self, cursor=None):
        query = """SELECT id, nom_projet FROM d_projets"""
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    @with_cursor()
    def get_new_client_code(self, client, cursor=None):
        query = """
            SELECT code_tiers
            FROM d_tiers
            WHERE nom_commercial LIKE %s
            LIMIT 1
        """
        cursor.execute(query, (f"%{client}%",))
        result = cursor.fetchone()
        if result:
            code_tier = result[0]
            return str(code_tier)
        return ""
    
    @with_cursor()
    def get_clients(self, cursor=None):
        query = """SELECT id, nom_commercial FROM d_tiers"""
        cursor.execute(query)
        items = [nom_commercial for id, nom_commercial in cursor.fetchall()]
        return items

    @with_cursor()
    def get_client_by_code(self, code_tier, cursor=None):
        query = """SELECT nom_commercial FROM d_tiers WHERE code_tiers LIKE %s LIMIT 1"""
        cursor.execute(query, (f"%{code_tier}%",))
        result = cursor.fetchone()
        if result:
            return result[0]
        return ""
    
    @with_cursor()
    def get_document_lines(self, cursor=None):
        query = """SELECT id,
                nom_ligne FROM d_lignes_documents"""
        cursor.execute(query)
        result = cursor.fetchall()
        return result
