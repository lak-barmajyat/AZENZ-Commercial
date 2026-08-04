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

    @with_cursor(dictionary=True)
    def search_articles(self, search_text: str, cursor=None):
        """Return active articles matching a code or designation."""
        query = """
            SELECT
                a.id,
                a.code_article,
                a.designation,
                a.description,
                a.type_article,
                a.unite_id,
                u.nom_unite,
                a.prix_vente_ht,
                a.prix_vente_ttc,
                a.prix_net,
                a.prix_revient_unitaire,
                a.tva_id,
                t.code_tva,
                t.taux
            FROM d_articles AS a
            LEFT JOIN p_unites AS u ON u.id = a.unite_id
            LEFT JOIN p_tvas AS t ON t.id = a.tva_id
            WHERE a.actif = 1
              AND a.supprime = 0
              AND (a.code_article LIKE %s OR a.designation LIKE %s)
            ORDER BY
                CASE WHEN a.code_article = %s THEN 0 ELSE 1 END,
                a.code_article
            LIMIT 20
        """
        pattern = f"%{search_text.strip()}%"
        cursor.execute(query, (pattern, pattern, search_text.strip()))
        return cursor.fetchall()

    @with_cursor(dictionary=True)
    def get_article_by_code(self, article_code: str, cursor=None):
        """Return one active article using an exact, case-insensitive code."""
        query = """
            SELECT
                a.id,
                a.code_article,
                a.designation,
                a.description,
                a.type_article,
                a.unite_id,
                u.nom_unite,
                a.prix_vente_ht,
                a.prix_vente_ttc,
                a.prix_net,
                a.prix_revient_unitaire,
                a.tva_id,
                t.code_tva,
                t.taux
            FROM d_articles AS a
            LEFT JOIN p_unites AS u ON u.id = a.unite_id
            LEFT JOIN p_tvas AS t ON t.id = a.tva_id
            WHERE LOWER(a.code_article) = LOWER(%s)
              AND a.actif = 1
              AND a.supprime = 0
            LIMIT 1
        """
        cursor.execute(query, (article_code.strip(),))
        return cursor.fetchone()
    
    @with_cursor(dictionary=True)
    def get_document_lines(self, document_id: int, cursor=None):
        query = """
            SELECT
                dl.id,
                dl.type_ligne,
                dl.article_id,
                dl.reference_article,
                dl.designation,
                dl.notes,
                dl.quantite,
                u.nom_unite,
                dl.unite_id,
                dl.prix_unitaire_ht,
                dl.unitaire_remise,
                dl.remise_percentage,
                dl.unitaire_marge,
                dl.code_tva,
                dl.tva_percentage,
                dl.tva_id,
                dl.unitaire_tva,
                dl.prix_unitaire_ttc,
                dl.prix_unitaire_net_ht,
                dl.montant_tva,
                dl.montant_ht,
                dl.montant_ttc,
                dl.montant_net_ht,
                dl.montant_remise,
                dl.montant_marge,
                p.nom_projet,
                dl.projet_id,
                d.nom_depot,
                dl.depot_id
            FROM d_document_lignes AS dl
            LEFT JOIN p_unites AS u
                ON u.id = dl.unite_id
            LEFT JOIN d_projets AS p
                ON p.id = dl.projet_id
            LEFT JOIN p_depots AS d
                ON d.id = dl.depot_id
            WHERE dl.document_id = %s
            AND dl.supprime = 0
            ORDER BY dl.numero_ligne ASC
        """

        cursor.execute(query, (document_id,))
        return cursor.fetchall()

    @with_cursor()
    def get_currency_symbol(self, cursor=None):
        # I have to get the devise id from p_informations_societe, and get the symbole from p_devises
        query = """SELECT pd.symbole FROM p_informations_societe pis
                LEFT JOIN p_devises pd ON pis.devise_id = pd.id"""
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return result[0]
        return ""

    @with_cursor()
    def get_units(self, cursor=None):
        query = """SELECT symbole FROM p_unites"""
        cursor.execute(query)
        result = cursor.fetchall()
        units = [symbole for symbole in result]
        return units
