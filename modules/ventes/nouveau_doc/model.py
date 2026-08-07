from services.sql.db_connection import with_cursor

import string, re

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
                a.id AS article_id,
                a.code_article AS code_article,
                a.designation,
                a.description AS notes,
                a.unite_id,
                u.nom_unite,
                a.prix_vente_ht AS prix_unitaire_ht,
                a.prix_vente_ttc AS prix_unitaire_ttc,
                a.prix_net AS prix_unitaire_net_ht,
                a.prix_revient_unitaire,
                a.tva_id,
                t.code_tva,
                t.taux AS tva_percentage,
                (a.prix_vente_ht * COALESCE(t.taux, 0) / 100) AS unitaire_tva,
                (a.prix_vente_ht - COALESCE(a.prix_revient_unitaire, 0)) AS unitaire_marge
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
                a.id AS article_id,
                a.code_article AS code_article,
                a.designation,
                a.description AS notes,
                a.unite_id,
                u.nom_unite,
                a.prix_vente_ht AS prix_unitaire_ht,
                a.prix_vente_ttc AS prix_unitaire_ttc,
                a.prix_net AS prix_unitaire_net_ht,
                a.prix_revient_unitaire,
                a.tva_id,
                t.code_tva,
                t.taux AS tva_percentage,
                (a.prix_vente_ht * COALESCE(t.taux, 0) / 100) AS unitaire_tva,
                (a.prix_vente_ht - COALESCE(a.prix_revient_unitaire, 0)) AS unitaire_marge
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
                dl.code_article,
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
                dl.prix_unitaire_net_ttc,
                dl.prix_revient_unitaire,
                dl.montant_tva,
                dl.montant_ht,
                dl.montant_ttc,
                dl.montant_net_ht,
                dl.montant_net_ttc,
                dl.montant_remise,
                dl.montant_marge,
                p.nom_projet,
                dl.projet_id,
                d.nom_depot,
                dl.depot_id
            FROM d_document_lignes AS dl
            LEFT JOIN p_unites AS u ON u.id = dl.unite_id
            LEFT JOIN d_projets AS p ON p.id = dl.projet_id
            LEFT JOIN p_depots AS d ON d.id = dl.depot_id
            WHERE dl.document_id = %s AND dl.supprime = 0
            ORDER BY dl.numero_ligne ASC
        """

        if document_id is None:
            return []
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
        units = [symbole[0] for symbole in cursor.fetchall()]
        return units

    @with_cursor(dictionary=True)
    def search_units(self, search_text: str, cursor=None):
        query = """
            SELECT id AS unite_id, nom_unite
            FROM p_unites
            WHERE nom_unite LIKE %s OR symbole LIKE %s
            ORDER BY nom_unite
            LIMIT 20
        """
        pattern = f"%{search_text.strip()}%"
        cursor.execute(query, (pattern, pattern))
        return cursor.fetchall()

    @with_cursor(dictionary=True)
    def search_projects(self, search_text: str, cursor=None):
        query = """
            SELECT id AS projet_id, nom_projet
            FROM d_projets
            WHERE nom_projet LIKE %s
            ORDER BY nom_projet
            LIMIT 20
        """
        cursor.execute(query, (f"%{search_text.strip()}%",))
        return cursor.fetchall()

    @with_cursor(dictionary=True)
    def search_depots(self, search_text: str, cursor=None):
        query = """
            SELECT id AS depot_id, nom_depot
            FROM p_depots
            WHERE nom_depot LIKE %s
            ORDER BY nom_depot
            LIMIT 20
        """
        cursor.execute(query, (f"%{search_text.strip()}%",))
        return cursor.fetchall()


    @with_cursor(dictionary=True)
    def get_document(self, document_id, cursor=None):
        query = """
            SELECT
                dd.`id`,
                dd.`type_document_id`,
                ptd.`nom_type_document` AS `type_document_name`,
                dd.`code_document`,
                dd.`autre_code_document`,
                dd.`document_origine_id`,
                ddo.`code_document` AS `document_origine_name`,
                dd.`tier_id`,
                dt.`code_tiers` AS `tier_code`,
                dt.`raison_sociale` AS `tier_name`,
                dd.`adresse_livraison_id`,
                adl.`nom_adresse` AS `adresse_livraison_name`,
                dd.`utilisateur_id`,
                pu.`nom_utilisateur` AS `utilisateur_name`,
                dd.`vendeur_id`,
                pv.`nom_utilisateur` AS `vendeur_name`,
                dd.`montant_ht`,
                dd.`montant_remise`,
                dd.`montant_net_ht`,
                dd.`montant_tva`,
                dd.`montant_ttc`,
                dd.`montant_net_ttc`,
                dd.`montant_paye`,
                dd.`montant_restant`,
                dd.`statut_document_id`,
                psd.`nom_statut` AS `statut_document_name`,
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
            WHERE dd.id = %s
            LIMIT 1
        """

        cursor.execute(query, (document_id,))
        return cursor.fetchone()

    @with_cursor()
    def generate_doc_code(self, id_type: int, cursor) -> str:
        query = """
            SELECT dernier_numero, longueur_numero
            FROM p_numerotation_documents
            WHERE type_document_id = %s
        """
        cursor.execute(query, (id_type,))
        row = cursor.fetchone()

        if row is None:
            raise ValueError(f"No numbering configuration found for document type {id_type}")

        dernier_numero, longueur_numero = row

        if not dernier_numero:
            return f"{1:0{longueur_numero}d}"

        # Separate the prefix from the numeric suffix.
        match = re.match(r"^(.*?)(\d+)$", dernier_numero)

        if match:
            prefix, numeric_part = match.groups()
            next_number = int(numeric_part) + 1
        else:
            # The previous value contains no ending number.
            prefix = dernier_numero
            next_number = 1

        return f"{prefix}{next_number:0{longueur_numero}d}"