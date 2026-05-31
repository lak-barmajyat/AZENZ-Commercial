-- Seed data for azenz_commercial
-- Generated from full schema analysis. This script refreshes demo data.
-- Import after creating the database structure in `azenz_commercial.sql`.

SET NAMES utf8mb4;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET FOREIGN_KEY_CHECKS = 0;
START TRANSACTION;

-- Clean existing demo data. Remove this block if you want to keep current records.
TRUNCATE TABLE `journaux_audit`;
TRUNCATE TABLE `d_document_reglements`;
TRUNCATE TABLE `d_mouvements_stock`;
TRUNCATE TABLE `d_lots_sn`;
TRUNCATE TABLE `d_stock`;
TRUNCATE TABLE `d_document_lignes`;
TRUNCATE TABLE `d_reglements`;
TRUNCATE TABLE `d_documents`;
TRUNCATE TABLE `d_projets`;
TRUNCATE TABLE `d_adresses_livraison`;
TRUNCATE TABLE `d_utilisateur_depots`;
TRUNCATE TABLE `d_articles`;
TRUNCATE TABLE `d_familles`;
TRUNCATE TABLE `d_tiers`;
TRUNCATE TABLE `p_numerotation_documents`;
TRUNCATE TABLE `p_statuts_documents`;
TRUNCATE TABLE `p_users_roles`;
TRUNCATE TABLE `p_role_permissions`;
TRUNCATE TABLE `p_permissions`;
TRUNCATE TABLE `p_roles`;
TRUNCATE TABLE `p_informations_societe`;
TRUNCATE TABLE `p_caisses`;
TRUNCATE TABLE `p_depots`;
TRUNCATE TABLE `p_modes_reglement`;
TRUNCATE TABLE `p_utilisateurs`;
TRUNCATE TABLE `p_unites`;
TRUNCATE TABLE `p_tvas`;
TRUNCATE TABLE `p_types_documents`;
TRUNCATE TABLE `p_devises`;

SET FOREIGN_KEY_CHECKS = 1;

-- Data for `p_devises` (3 rows)
INSERT INTO `p_devises` (`id`, `code_devise`, `nom_devise`, `symbole`, `devise_principale`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'MAD', 'Dirham Marocain', 'DH', 1, 1, NULL, '2026-05-31 10:30:00', 0),
  (2, 'EUR', 'Euro', '€', 0, 1, NULL, '2026-05-31 10:30:00', 0),
  (3, 'USD', 'Dollar Américain', '$', 0, 1, NULL, '2026-05-31 10:30:00', 0);

-- Data for `p_tvas` (4 rows)
INSERT INTO `p_tvas` (`id`, `code_tva`, `nom_tva`, `taux`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'TVA0', 'Exonéré TVA', 0, 1, NULL, '2026-05-31 10:30:00', 0),
  (2, 'TVA7', 'TVA réduite 7%', 7, 1, NULL, '2026-05-31 10:30:00', 0),
  (3, 'TVA10', 'TVA intermédiaire 10%', 10, 1, NULL, '2026-05-31 10:30:00', 0),
  (4, 'TVA20', 'TVA normale 20%', 20, 1, NULL, '2026-05-31 10:30:00', 0);

-- Data for `p_unites` (5 rows)
INSERT INTO `p_unites` (`id`, `code_unite`, `nom_unite`, `symbole`, `type_unite`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'PCS', 'Pièce', 'pcs', 'QUANTITE', 1, NULL, '2026-05-31 10:30:00', 0),
  (2, 'KG', 'Kilogramme', 'kg', 'POIDS', 1, NULL, '2026-05-31 10:30:00', 0),
  (3, 'L', 'Litre', 'L', 'VOLUME', 1, NULL, '2026-05-31 10:30:00', 0),
  (4, 'H', 'Heure', 'h', 'TEMPS', 1, NULL, '2026-05-31 10:30:00', 0),
  (5, 'M', 'Mètre', 'm', 'LONGUEUR', 1, NULL, '2026-05-31 10:30:00', 0);

-- Data for `p_types_documents` (8 rows)
INSERT INTO `p_types_documents` (`id`, `code_type_document`, `nom_type_document`, `domaine`, `sens_stock`, `impacte_stock`, `impacte_reglement`, `actif`) VALUES
  (1, 'DEV', 'Devis client', 'VENTE', 'AUCUN', 0, 0, 1),
  (2, 'BCV', 'Bon de commande client', 'VENTE', 'AUCUN', 0, 0, 1),
  (3, 'BLV', 'Bon de livraison vente', 'VENTE', 'SORTIE', 1, 0, 1),
  (4, 'FACV', 'Facture vente', 'VENTE', 'AUCUN', 0, 1, 1),
  (5, 'BCA', 'Bon de commande achat', 'ACHAT', 'AUCUN', 0, 0, 1),
  (6, 'BRA', 'Bon de réception achat', 'ACHAT', 'ENTREE', 1, 0, 1),
  (7, 'FACA', 'Facture achat', 'ACHAT', 'AUCUN', 0, 1, 1),
  (8, 'INV', 'Inventaire stock', 'STOCK', 'AUCUN', 1, 0, 1);

-- Data for `p_utilisateurs` (4 rows)
INSERT INTO `p_utilisateurs` (`id`, `nom_utilisateur`, `description`, `code_utilisateur`, `email`, `telephone`, `mot_de_passe_hash`, `est_administrateur`, `date_mot_de_passe`, `statut_mot_de_passe`, `actif`, `tentatives_connexion`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'admin', 'Administrateur système', 'ADMIN', 'admin@azenz.local', '0600000001', '$2a$12$UKOe61U7etZNxJb76yjLeeodZsdorf.QW738JIJ3hTqtcLyfKmTC2', 1, '2026-05-31 09:00:00', 'ACTIF', 1, 0, NULL, '2026-05-31 10:30:00', 0),
  (2, 'sara', 'Responsable ventes', 'USR-SARA', 'sara@azenz.local', '0600000002', '$2a$12$UKOe61U7etZNxJb76yjLeeodZsdorf.QW738JIJ3hTqtcLyfKmTC2', 0, '2026-05-31 09:00:00', 'ACTIF', 1, 0, 1, '2026-05-31 10:30:00', 0),
  (3, 'youssef', 'Magasinier', 'USR-YOUSSEF', 'youssef@azenz.local', '0600000003', '$2a$12$UKOe61U7etZNxJb76yjLeeodZsdorf.QW738JIJ3hTqtcLyfKmTC2', 0, '2026-05-31 09:00:00', 'ACTIF', 1, 0, 1, '2026-05-31 10:30:00', 0),
  (4, 'amina', 'Comptable', 'USR-AMINA', 'amina@azenz.local', '0600000004', '$2a$12$UKOe61U7etZNxJb76yjLeeodZsdorf.QW738JIJ3hTqtcLyfKmTC2', 0, '2026-05-31 09:00:00', 'ACTIF', 1, 0, 1, '2026-05-31 10:30:00', 0),
  (5, 'karim', 'Responsable achat', 'USR-KARIM', 'karim@azenz.local', '0600000005', '$2a$12$UKOe61U7etZNxJb76yjLeeodZsdorf.QW738JIJ3hTqtcLyfKmTC2', 0, '2026-05-31 09:00:00', 'ACTIF', 1, 0, 1, '2026-05-31 10:30:00', 0);


-- Data for `p_depots` (3 rows)
INSERT INTO `p_depots` (`id`, `code_depot`, `nom_depot`, `description`, `adresse`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'DEP-PR', 'Dépôt principal', 'Stock principal', 'Zone industrielle Marrakech', 1, 1, '2026-05-31 10:30:00', 0),
  (2, 'DEP-MG', 'Magasin vente', 'Magasin showroom', 'Centre ville Marrakech', 1, 1, '2026-05-31 10:30:00', 0),
  (3, 'DEP-RET', 'Dépôt retours', 'Produits retournés', 'Zone SAV', 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `p_modes_reglement` (4 rows)
INSERT INTO `p_modes_reglement` (`id`, `code_mode_reglement`, `nom_mode_reglement`, `type_mode`, `description`, `requiert_banque`, `requiert_numero_piece`, `requiert_date_echeance`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'ESP', 'Espèces', 'ESPECE', 'Paiement cash', 0, 0, 0, 1, 1, '2026-05-31 10:30:00', 0),
  (2, 'CHQ', 'Chèque', 'CHEQUE', 'Paiement par chèque', 1, 1, 1, 1, 1, '2026-05-31 10:30:00', 0),
  (3, 'VIR', 'Virement bancaire', 'VIREMENT', 'Paiement par virement', 1, 1, 0, 1, 1, '2026-05-31 10:30:00', 0),
  (4, 'CB', 'Carte bancaire', 'CARTE', 'Paiement par TPE', 0, 1, 0, 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `p_caisses` (3 rows)
INSERT INTO `p_caisses` (`id`, `code_caisse`, `nom_caisse`, `type_caisse`, `banque_nom`, `numero_compte`, `iban`, `rib`, `description`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'CASH-PR', 'Caisse principale', 'CAISSE', NULL, NULL, NULL, NULL, 'Caisse du magasin', 1, 1, '2026-05-31 10:30:00', 0),
  (2, 'BANK-CI', 'Compte CIH', 'BANQUE', 'CIH Bank', '1234567890', 'MA640123456789012345678901', '123456789012345678901234', 'Compte bancaire principal', 1, 1, '2026-05-31 10:30:00', 0),
  (3, 'TPE-01', 'Terminal paiement', 'TERMINAL_PAIEMENT', NULL, NULL, NULL, NULL, 'TPE magasin', 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `p_roles` (5 rows)
INSERT INTO `p_roles` (`id`, `name`, `display_name`, `description`, `active`, `date_creation`) VALUES
  (1, 'admin', 'Administrateur', 'Accès complet', 1, '2026-05-31 10:30:00'),
  (2, 'manager', 'Manager', 'Gestion commerciale', 1, '2026-05-31 10:30:00'),
  (3, 'vendeur', 'Vendeur', 'Vente et consultation stock', 1, '2026-05-31 10:30:00'),
  (4, 'magasinier', 'Magasinier', 'Stock et mouvements', 1, '2026-05-31 10:30:00'),
  (5, 'comptable', 'Comptable', 'Règlements et reporting', 1, '2026-05-31 10:30:00');

-- Data for `p_permissions` (40 rows)
INSERT INTO `p_permissions` (`id`, `code`, `module`, `action`, `description`) VALUES
  (1, 'clients.view', 'clients', 'view', 'view clients'),
  (2, 'clients.create', 'clients', 'create', 'create clients'),
  (3, 'clients.edit', 'clients', 'edit', 'edit clients'),
  (4, 'clients.delete', 'clients', 'delete', 'delete clients'),
  (5, 'fournisseurs.view', 'fournisseurs', 'view', 'view fournisseurs'),
  (6, 'fournisseurs.create', 'fournisseurs', 'create', 'create fournisseurs'),
  (7, 'fournisseurs.edit', 'fournisseurs', 'edit', 'edit fournisseurs'),
  (8, 'fournisseurs.delete', 'fournisseurs', 'delete', 'delete fournisseurs'),
  (9, 'articles.view', 'articles', 'view', 'view articles'),
  (10, 'articles.create', 'articles', 'create', 'create articles'),
  (11, 'articles.edit', 'articles', 'edit', 'edit articles'),
  (12, 'articles.delete', 'articles', 'delete', 'delete articles'),
  (13, 'ventes.view', 'ventes', 'view', 'view ventes'),
  (14, 'ventes.create', 'ventes', 'create', 'create ventes'),
  (15, 'ventes.edit', 'ventes', 'edit', 'edit ventes'),
  (16, 'ventes.delete', 'ventes', 'delete', 'delete ventes'),
  (17, 'achats.view', 'achats', 'view', 'view achats'),
  (18, 'achats.create', 'achats', 'create', 'create achats'),
  (19, 'achats.edit', 'achats', 'edit', 'edit achats'),
  (20, 'achats.delete', 'achats', 'delete', 'delete achats'),
  (21, 'stock.view', 'stock', 'view', 'view stock'),
  (22, 'stock.create', 'stock', 'create', 'create stock'),
  (23, 'stock.edit', 'stock', 'edit', 'edit stock'),
  (24, 'stock.delete', 'stock', 'delete', 'delete stock'),
  (25, 'reglements.view', 'reglements', 'view', 'view reglements'),
  (26, 'reglements.create', 'reglements', 'create', 'create reglements'),
  (27, 'reglements.edit', 'reglements', 'edit', 'edit reglements'),
  (28, 'reglements.delete', 'reglements', 'delete', 'delete reglements'),
  (29, 'utilisateurs.view', 'utilisateurs', 'view', 'view utilisateurs'),
  (30, 'utilisateurs.create', 'utilisateurs', 'create', 'create utilisateurs'),
  (31, 'utilisateurs.edit', 'utilisateurs', 'edit', 'edit utilisateurs'),
  (32, 'utilisateurs.delete', 'utilisateurs', 'delete', 'delete utilisateurs'),
  (33, 'parametres.view', 'parametres', 'view', 'view parametres'),
  (34, 'parametres.create', 'parametres', 'create', 'create parametres'),
  (35, 'parametres.edit', 'parametres', 'edit', 'edit parametres'),
  (36, 'parametres.delete', 'parametres', 'delete', 'delete parametres'),
  (37, 'rapports.view', 'rapports', 'view', 'view rapports'),
  (38, 'rapports.create', 'rapports', 'create', 'create rapports'),
  (39, 'rapports.edit', 'rapports', 'edit', 'edit rapports'),
  (40, 'rapports.delete', 'rapports', 'delete', 'delete rapports');

-- Data for `p_role_permissions` (96 rows)
INSERT INTO `p_role_permissions` (`role_id`, `permission_id`) VALUES
  (1, 1),
  (1, 2),
  (1, 3),
  (1, 4),
  (1, 5),
  (1, 6),
  (1, 7),
  (1, 8),
  (1, 9),
  (1, 10),
  (1, 11),
  (1, 12),
  (1, 13),
  (1, 14),
  (1, 15),
  (1, 16),
  (1, 17),
  (1, 18),
  (1, 19),
  (1, 20),
  (1, 21),
  (1, 22),
  (1, 23),
  (1, 24),
  (1, 25),
  (1, 26),
  (1, 27),
  (1, 28),
  (1, 29),
  (1, 30),
  (1, 31),
  (1, 32),
  (1, 33),
  (1, 34),
  (1, 35),
  (1, 36),
  (1, 37),
  (1, 38),
  (1, 39),
  (1, 40),
  (2, 1),
  (2, 2),
  (2, 3),
  (2, 5),
  (2, 6),
  (2, 7),
  (2, 9),
  (2, 10),
  (2, 11),
  (2, 13),
  (2, 14),
  (2, 15),
  (2, 17),
  (2, 18),
  (2, 19),
  (2, 21),
  (2, 22),
  (2, 23),
  (2, 25),
  (2, 26),
  (2, 27),
  (2, 33),
  (2, 37),
  (3, 1),
  (3, 2),
  (3, 3),
  (3, 9),
  (3, 13),
  (3, 14),
  (3, 15),
  (3, 21),
  (3, 25),
  (3, 26),
  (3, 37),
  (4, 9),
  (4, 17),
  (4, 18),
  (4, 19),
  (4, 20),
  (4, 21),
  (4, 22),
  (4, 23),
  (4, 24),
  (4, 37),
  (5, 1),
  (5, 5),
  (5, 13),
  (5, 17),
  (5, 25),
  (5, 26),
  (5, 27),
  (5, 28),
  (5, 37),
  (5, 38),
  (5, 39),
  (5, 40);

-- Data for `p_users_roles` (5 rows)
INSERT INTO `p_users_roles` (`user_id`, `role_id`) VALUES
  (1, 1),
  (2, 2),
  (2, 3),
  (3, 4),
  (4, 5);

-- Data for `p_statuts_documents` (32 rows)
INSERT INTO `p_statuts_documents` (`id`, `code_statut`, `nom_statut`, `type_document_id`, `ordre_affichage`, `couleur`, `document_verrouille`, `impacte_stock`, `impacte_reglement`, `actif`, `cree_par`, `date_creation`) VALUES
  (1, 'BROUILLON', 'Brouillon', 1, 1, '#9CA3AF', 0, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (2, 'VALIDE', 'Validé', 1, 2, '#2563EB', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (3, 'CLOTURE', 'Clôturé', 1, 3, '#16A34A', 1, 1, 1, 1, 1, '2026-05-31 10:30:00'),
  (4, 'ANNULE', 'Annulé', 1, 4, '#DC2626', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (5, 'BROUILLON', 'Brouillon', 2, 1, '#9CA3AF', 0, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (6, 'VALIDE', 'Validé', 2, 2, '#2563EB', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (7, 'CLOTURE', 'Clôturé', 2, 3, '#16A34A', 1, 1, 1, 1, 1, '2026-05-31 10:30:00'),
  (8, 'ANNULE', 'Annulé', 2, 4, '#DC2626', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (9, 'BROUILLON', 'Brouillon', 3, 1, '#9CA3AF', 0, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (10, 'VALIDE', 'Validé', 3, 2, '#2563EB', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (11, 'CLOTURE', 'Clôturé', 3, 3, '#16A34A', 1, 1, 1, 1, 1, '2026-05-31 10:30:00'),
  (12, 'ANNULE', 'Annulé', 3, 4, '#DC2626', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (13, 'BROUILLON', 'Brouillon', 4, 1, '#9CA3AF', 0, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (14, 'VALIDE', 'Validé', 4, 2, '#2563EB', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (15, 'CLOTURE', 'Clôturé', 4, 3, '#16A34A', 1, 1, 1, 1, 1, '2026-05-31 10:30:00'),
  (16, 'ANNULE', 'Annulé', 4, 4, '#DC2626', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (17, 'BROUILLON', 'Brouillon', 5, 1, '#9CA3AF', 0, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (18, 'VALIDE', 'Validé', 5, 2, '#2563EB', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (19, 'CLOTURE', 'Clôturé', 5, 3, '#16A34A', 1, 1, 1, 1, 1, '2026-05-31 10:30:00'),
  (20, 'ANNULE', 'Annulé', 5, 4, '#DC2626', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (21, 'BROUILLON', 'Brouillon', 6, 1, '#9CA3AF', 0, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (22, 'VALIDE', 'Validé', 6, 2, '#2563EB', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (23, 'CLOTURE', 'Clôturé', 6, 3, '#16A34A', 1, 1, 1, 1, 1, '2026-05-31 10:30:00'),
  (24, 'ANNULE', 'Annulé', 6, 4, '#DC2626', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (25, 'BROUILLON', 'Brouillon', 7, 1, '#9CA3AF', 0, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (26, 'VALIDE', 'Validé', 7, 2, '#2563EB', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (27, 'CLOTURE', 'Clôturé', 7, 3, '#16A34A', 1, 1, 1, 1, 1, '2026-05-31 10:30:00'),
  (28, 'ANNULE', 'Annulé', 7, 4, '#DC2626', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (29, 'BROUILLON', 'Brouillon', 8, 1, '#9CA3AF', 0, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (30, 'VALIDE', 'Validé', 8, 2, '#2563EB', 1, 0, 0, 1, 1, '2026-05-31 10:30:00'),
  (31, 'CLOTURE', 'Clôturé', 8, 3, '#16A34A', 1, 1, 1, 1, 1, '2026-05-31 10:30:00'),
  (32, 'ANNULE', 'Annulé', 8, 4, '#DC2626', 1, 0, 0, 1, 1, '2026-05-31 10:30:00');

-- Data for `p_numerotation_documents` (8 rows)
INSERT INTO `p_numerotation_documents` (`id`, `type_document_id`, `prefixe`, `annee`, `dernier_numero`, `longueur_numero`, `actif`) VALUES
  (1, 1, 'DEV-', 2026, 26, 5, 1),
  (2, 2, 'BCV-', 2026, 27, 5, 1),
  (3, 3, 'BLV-', 2026, 28, 5, 1),
  (4, 4, 'FACV-', 2026, 29, 5, 1),
  (5, 5, 'BCA-', 2026, 30, 5, 1),
  (6, 6, 'BRA-', 2026, 31, 5, 1),
  (7, 7, 'FACA-', 2026, 32, 5, 1),
  (8, 8, 'INV-', 2026, 33, 5, 1);

-- Data for `p_informations_societe` (2 rows)
INSERT INTO `p_informations_societe` (`id`, `raison_sociale`, `nom_commercial`, `activite`, `identifiant_fiscal`, `ice`, `rc`, `patente`, `cnss`, `adresse`, `code_postal`, `ville`, `region`, `pays`, `telephone`, `email`, `site_web`, `logo_url`, `devise_id`, `tva_id`) VALUES
  (1, 'Azenz Commercial SARL', 'Azenz', 'Commerce et distribution', 'IF-AZENZ-2026', '002345678000071', 'RC-45210', 'PAT-88991', 'CNSS-120033', 'Route de Casablanca, Marrakech', '40000', 'Marrakech', 'Marrakech-Safi', 'Maroc', '0524000000', 'contact@azenz.local', 'https://azenz.local', '/assets/logo/azenz.png', 1, 4),
  (2, 'Azenz Showroom', 'Azenz Store', 'Vente détail', 'IF-STORE-2026', '002345678000089', 'RC-45211', 'PAT-88992', 'CNSS-120034', 'Guéliz, Marrakech', '40000', 'Marrakech', 'Marrakech-Safi', 'Maroc', '0524000011', 'store@azenz.local', 'https://store.azenz.local', '/assets/logo/azenz-store.png', 1, 4);

-- Data for `d_familles` (4 rows)
INSERT INTO `d_familles` (`id`, `code_famille`, `nom_famille`, `description`, `type_famille`, `suivi_stock`, `mode_valorisation_stock`, `tva_id`, `gestion_lot`, `gestion_numero_serie`, `unite_id`, `depot_id`, `exclure_statistiques`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'ELEC', 'Électronique', 'Famille Électronique', 'PRODUIT', 1, 'CMUP', 4, 0, 0, 1, 1, 0, 1, 1, '2026-05-31 10:30:00', 0),
  (2, 'BUREAU', 'Fournitures bureau', 'Famille Fournitures bureau', 'PRODUIT', 1, 'CMUP', 4, 0, 0, 1, 1, 0, 1, 1, '2026-05-31 10:30:00', 0),
  (3, 'SERV', 'Services', 'Famille Services', 'SERVICE', 0, 'CMUP', 4, 0, 0, 4, NULL, 0, 1, 1, '2026-05-31 10:30:00', 0),
  (4, 'MP', 'Matières premières', 'Famille Matières premières', 'MATIERE_PREMIERE', 1, 'CMUP', 4, 0, 0, 2, 1, 0, 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `d_articles` (5 rows)
INSERT INTO `d_articles` (`id`, `code_article`, `designation`, `description`, `famille_id`, `type_article`, `unite_id`, `unite_secondaire_id`, `prix_achat_ht`, `prix_achat_ttc`, `prix_vente_ht`, `prix_vente_ttc`, `prix_net`, `tva_id`, `suivi_stock`, `mode_valorisation_stock`, `prix_revient_unitaire`, `quantite_min_stock`, `quantite_max_stock`, `gestion_lot`, `gestion_numero_serie`, `article_compose`, `interdire_achat`, `interdire_vente`, `interdire_commande`, `exclure_statistiques`, `image_url`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'ART-LAP-001', 'Laptop Pro 14', 'Ordinateur portable professionnel', 1, 'PRODUIT', 1, 4, 7200, 8640, 9500, 11400, 11400, 4, 1, 'SN', 7200, 2, 20, 0, 1, 0, 0, 0, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0),
  (2, 'ART-PRN-001', 'Imprimante Laser', 'Imprimante bureau monochrome', 1, 'PRODUIT', 1, NULL, 1300, 1560, 1850, 2220, 2220, 4, 1, 'CMUP', 1300, 3, 15, 0, 0, 0, 0, 0, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0),
  (3, 'ART-PAP-A4', 'Papier A4 80g', 'Ramette papier A4', 2, 'PRODUIT', 1, NULL, 32, 38.4, 45, 54, 54, 4, 1, 'FIFO', 32, 50, 500, 1, 0, 0, 0, 0, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0),
  (4, 'SERV-INST', 'Installation logiciel', 'Service installation et paramétrage', 3, 'SERVICE', 4, NULL, 0, 0, 300, 360, 360, 4, 0, 'AUCUN', 0, 0, NULL, 0, 0, 0, 1, 0, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0),
  (5, 'MP-CABL-001', 'Câble réseau CAT6', 'Bobine câble réseau', 4, 'MATIERE_PREMIERE', 5, NULL, 4, 4.8, 7, 8.4, 8.4, 4, 1, 'CMUP', 4, 100, 1000, 0, 0, 0, 0, 1, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `d_tiers` (5 rows)
INSERT INTO `d_tiers` (`id`, `code_tiers`, `raison_sociale`, `nom_commercial`, `type_tiers`, `contact_principal`, `telephone`, `telephone_secondaire`, `email`, `site_web`, `adresse`, `code_postal`, `ville`, `region`, `pays`, `identifiant_fiscal`, `ice`, `rc`, `patente`, `cnss`, `tva_id`, `activite`, `plafond_credit`, `delai_paiement_jours`, `devise_id`, `mode_paiement_id`, `code_edi`, `type_edi`, `facture_electronique`, `emission_fe`, `application_fe`, `notes`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'CLT-001', 'Atlas Distribution', 'Atlas Pro', 'CLIENT', 'Nadia El Amrani', '0611111111', NULL, 'client1@azenz.local', NULL, 'Adresse Atlas Distribution', '40000', 'Marrakech', NULL, 'Maroc', 'IF-CLT-001', 'ICE-CLT-001', NULL, NULL, NULL, 1, 'Commerce', 60000, 30, 1, 1, NULL, NULL, 0, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0),
  (2, 'CLT-002', 'Riad Services', 'Riad Services', 'CLIENT', 'Omar Benali', '0622222222', NULL, 'client2@azenz.local', NULL, 'Adresse Riad Services', '40000', 'Agadir', NULL, 'Maroc', 'IF-CLT-002', 'ICE-CLT-002', NULL, NULL, NULL, 4, 'Commerce', 35000, 15, 1, 3, NULL, NULL, 0, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0),
  (3, 'FRN-001', 'Tech Import Maroc', 'TIM', 'FOURNISSEUR', 'Hicham Fassi', '0633333333', NULL, 'fournisseur1@azenz.local', NULL, 'Adresse Tech Import Maroc', '40000', 'Casablanca', NULL, 'Maroc', 'IF-FRN-001', 'ICE-FRN-001', NULL, NULL, NULL, 4, 'Commerce', 0, 45, 1, 3, NULL, NULL, 0, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0),
  (4, 'FRN-002', 'Papier Nord', 'Papier Nord', 'FOURNISSEUR', 'Salma Idrissi', '0644444444', NULL, 'fournisseur2@azenz.local', NULL, 'Adresse Papier Nord', '40000', 'Tanger', NULL, 'Maroc', 'IF-FRN-002', 'ICE-FRN-002', NULL, NULL, NULL, 4, 'Commerce', 0, 30, 1, 2, NULL, NULL, 0, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0),
  (5, 'PRS-001', 'Boutique Al Amal', 'Al Amal', 'PROSPECT', 'Karima Saidi', '0655555555', NULL, 'prospect@azenz.local', NULL, 'Adresse Boutique Al Amal', '40000', 'Rabat', NULL, 'Maroc', 'IF-PRS-001', 'ICE-PRS-001', NULL, NULL, NULL, 4, 'Commerce', 10000, 7, 1, 1, NULL, NULL, 0, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `d_adresses_livraison` (4 rows)
INSERT INTO `d_adresses_livraison` (`id`, `tier_id`, `nom_adresse`, `adresse`, `utilisateur_id`, `telephone`, `email`, `code_postal`, `ville`, `region`, `pays`, `instructions_livraison`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 1, 'Siège Atlas', 'Quartier industriel, Marrakech', NULL, '0600000100', NULL, '40000', 'Marrakech', 'Marrakech-Safi', 'Maroc', 'Appeler avant livraison', 1, 1, '2026-05-31 10:30:00', 0),
  (2, 1, 'Dépôt Atlas', 'Route Safi, Marrakech', NULL, '0600000100', NULL, '40000', 'Marrakech', 'Marrakech-Safi', 'Maroc', 'Appeler avant livraison', 1, 1, '2026-05-31 10:30:00', 0),
  (3, 2, 'Riad Services Agadir', 'Avenue Hassan II', NULL, '0600000100', NULL, '40000', 'Agadir', 'Souss-Massa', 'Maroc', 'Appeler avant livraison', 1, 1, '2026-05-31 10:30:00', 0),
  (4, 5, 'Boutique Rabat', 'Agdal', NULL, '0600000100', NULL, '40000', 'Rabat', 'Rabat-Salé-Kénitra', 'Maroc', 'Appeler avant livraison', 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `d_projets` (3 rows)
INSERT INTO `d_projets` (`id`, `code_projet`, `nom_projet`, `description`, `tier_id`, `utilisateur_id`, `date_debut`, `date_fin_prevue`, `priorite`, `budget_prevu`, `budget_reel`, `montant_facture`, `notes`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'PRJ-001', 'Équipement Atlas', 'Projet Équipement Atlas', 1, 2, '2026-05-01', '2026-07-31', 'HAUTE', 85000, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0),
  (2, 'PRJ-002', 'Showroom Riad Services', 'Projet Showroom Riad Services', 2, 2, '2026-05-01', '2026-07-31', 'NORMALE', 42000, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0),
  (3, 'PRJ-003', 'Refonte réseau interne', 'Projet Refonte réseau interne', 1, 3, '2026-05-01', '2026-07-31', 'URGENTE', 15000, 0, 0, NULL, 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `d_utilisateur_depots` (6 rows)
INSERT INTO `d_utilisateur_depots` (`id`, `utilisateur_id`, `depot_id`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 1, 1, 1, 1, '2026-05-31 10:30:00', 0),
  (2, 2, 1, 1, 1, '2026-05-31 10:30:00', 0),
  (3, 2, 2, 1, 1, '2026-05-31 10:30:00', 0),
  (4, 3, 1, 1, 1, '2026-05-31 10:30:00', 0),
  (5, 3, 3, 1, 1, '2026-05-31 10:30:00', 0),
  (6, 4, 1, 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `d_documents` (8 rows)
INSERT INTO `d_documents` (`id`, `type_document_id`, `reference_document`, `document_origine_id`, `tier_id`, `adresse_livraison_id`, `utilisateur_id`, `vendeur_id`, `montant_ht`, `montant_remise`, `montant_net_ht`, `montant_tva`, `montant_ttc`, `montant_net_ttc`, `montant_paye`, `montant_restant`, `statut_document_id`, `document_valide`, `document_cloture`, `date_document`, `date_livraison_prevue`, `commentaire`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 1, 'DEV-00001', NULL, 1, 1, 2, 2, 19350, 0, 19350, 3870, 23220, 23220, 0, 23220, 2, 1, 0, '2026-05-10 10:00:00', '2026-05-18 09:00:00', 'Devis matériel Atlas', 1, '2026-05-31 10:30:00', 0),
  (2, 2, 'BCV-00001', 1, 1, 1, 2, 2, 19350, 0, 19350, 3870, 23220, 23220, 5000, 18220, 6, 1, 0, '2026-05-11 11:00:00', '2026-05-18 09:00:00', 'Commande client issue du devis', 1, '2026-05-31 10:30:00', 0),
  (3, 3, 'BLV-00001', 2, 1, 1, 3, 2, 9850, 0, 9850, 1970, 11820, 11820, 0, 11820, 11, 1, 1, '2026-05-13 09:00:00', '2026-05-18 09:00:00', 'Livraison partielle', 1, '2026-05-31 10:30:00', 0),
  (4, 4, 'FACV-00001', 3, 1, 1, 4, 2, 9850, 0, 9850, 1970, 11820, 11820, 11820, 0, 15, 1, 1, '2026-05-14 15:00:00', '2026-05-18 09:00:00', 'Facture livraison partielle', 1, '2026-05-31 10:30:00', 0),
  (5, 5, 'BCA-00001', NULL, 3, NULL, 3, 3, 14400, 0, 14400, 2880, 17280, 17280, 0, 17280, 18, 1, 0, '2026-05-09 14:00:00', '2026-05-18 09:00:00', 'Commande achat laptops', 1, '2026-05-31 10:30:00', 0),
  (6, 6, 'BRA-00001', 5, 3, NULL, 3, 3, 14400, 0, 14400, 2880, 17280, 17280, 0, 17280, 23, 1, 1, '2026-05-12 10:30:00', '2026-05-18 09:00:00', 'Réception achat laptops', 1, '2026-05-31 10:30:00', 0),
  (7, 7, 'FACA-00001', 6, 3, NULL, 4, 3, 14400, 0, 14400, 2880, 17280, 17280, 8000, 9280, 27, 1, 0, '2026-05-15 16:10:00', '2026-05-18 09:00:00', 'Facture fournisseur', 1, '2026-05-31 10:30:00', 0),
  (8, 8, 'INV-00001', NULL, NULL, NULL, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 31, 1, 1, '2026-05-20 08:30:00', '2026-05-18 09:00:00', 'Inventaire mensuel', 1, '2026-05-31 10:30:00', 0);

-- Data for `d_document_lignes` (14 rows)
INSERT INTO `d_document_lignes` (`id`, `document_id`, `numero_ligne`, `article_id`, `reference_article`, `designation`, `type_ligne`, `quantite`, `unite_id`, `prix_unitaire_ht`, `prix_unitaire_ttc`, `prix_revient_unitaire`, `tva_id`, `tva_percentage`, `remise_percentage`, `valeur_unitaire_remise`, `depot_id`, `impact_stock`, `valorise_stock`, `projet_id`, `date_livraison_prevue`, `notes`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 1, 1, 1, 'ART-LAP-001', 'Laptop Pro 14', 0, 2, 1, 9500, 11400, 7200, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (2, 1, 2, 3, 'ART-PAP-A4', 'Papier A4 80g', 0, 30, 1, 45, 54, 32, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (3, 1, 3, 4, 'SERV-INST', 'Installation logiciel', 0, 1, 4, 300, 360, 0, 4, 20, 0, 0, 1, 0, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (4, 2, 1, 1, 'ART-LAP-001', 'Laptop Pro 14', 0, 2, 1, 9500, 11400, 7200, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (5, 2, 2, 3, 'ART-PAP-A4', 'Papier A4 80g', 0, 30, 1, 45, 54, 32, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (6, 2, 3, 4, 'SERV-INST', 'Installation logiciel', 0, 1, 4, 300, 360, 0, 4, 20, 0, 0, 1, 0, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (7, 3, 1, 1, 'ART-LAP-001', 'Laptop Pro 14', 0, 1, 1, 9500, 11400, 7200, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (8, 3, 2, 3, 'ART-PAP-A4', 'Papier A4 80g', 0, 10, 1, 35, 42, 32, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (9, 4, 1, 1, 'ART-LAP-001', 'Laptop Pro 14', 0, 1, 1, 9500, 11400, 7200, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (10, 4, 2, 3, 'ART-PAP-A4', 'Papier A4 80g', 0, 10, 1, 35, 42, 32, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (11, 5, 1, 1, 'ART-LAP-001', 'Laptop Pro 14', 0, 2, 1, 7200, 8640, 7200, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (12, 6, 1, 1, 'ART-LAP-001', 'Laptop Pro 14', 0, 2, 1, 7200, 8640, 7200, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (13, 7, 1, 1, 'ART-LAP-001', 'Laptop Pro 14', 0, 2, 1, 7200, 8640, 7200, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0),
  (14, 8, 1, 3, 'ART-PAP-A4', 'Ajustement stock papier', 0, 5, 1, 32, 38.4, 32, 4, 20, 0, 0, 1, 1, 1, 1, '2026-05-18 09:00:00', NULL, 1, '2026-05-31 10:30:00', 0);

-- Data for `d_stock` (6 rows)
INSERT INTO `d_stock` (`id`, `article_id`, `depot_id`, `quantite_stock`, `quantite_reservee`, `cout_moyen`, `date_dernier_mouvement`) VALUES
  (1, 1, 1, 8, 0, 7200, '2026-05-20 08:30:00'),
  (2, 2, 1, 5, 1, 1300, '2026-05-20 08:30:00'),
  (3, 3, 1, 180, 10, 32, '2026-05-20 08:30:00'),
  (4, 5, 1, 320, 0, 4, '2026-05-20 08:30:00'),
  (5, 1, 2, 1, 0, 7200, '2026-05-20 08:30:00'),
  (6, 3, 2, 40, 0, 32, '2026-05-20 08:30:00');

-- Data for `d_lots_sn` (3 rows)
INSERT INTO `d_lots_sn` (`id`, `article_id`, `numero_lot_sn`, `date_fabrication`, `date_peremption`, `quantite_initiale`, `quantite_actuelle`, `prix_achat_unitaire`, `depot_id`, `fournisseur_id`, `document_entree_id`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 1, 'SN-LAP-2026-0001', '2026-04-01', '2029-04-01', 1, 1, 7200, 1, 3, 6, 1, 1, '2026-05-31 10:30:00', 0),
  (2, 1, 'SN-LAP-2026-0002', '2026-04-01', '2029-04-01', 1, 1, 7200, 1, 3, 6, 1, 1, '2026-05-31 10:30:00', 0),
  (3, 3, 'LOT-PAP-2026-05', '2026-05-01', '2028-05-01', 100, 85, 32, 1, 4, NULL, 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `d_mouvements_stock` (5 rows)
INSERT INTO `d_mouvements_stock` (`id`, `article_id`, `depot_id`, `document_id`, `document_ligne_id`, `type_mouvement`, `sens_mouvement`, `quantite`, `prix_revient_unitaire`, `date_mouvement`, `description`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 1, 1, 6, 12, 'ENTREE', 'IN', 2, 7200, '2026-05-20 08:30:00', 'Réception achat', 1, '2026-05-31 10:30:00', 0),
  (2, 1, 1, 3, 7, 'SORTIE', 'OUT', 1, 7200, '2026-05-20 08:30:00', 'Livraison client', 1, '2026-05-31 10:30:00', 0),
  (3, 3, 1, 3, 8, 'SORTIE', 'OUT', 10, 32, '2026-05-20 08:30:00', 'Livraison papier', 1, '2026-05-31 10:30:00', 0),
  (4, 3, 1, 8, 14, 'INVENTAIRE', 'IN', 5, 32, '2026-05-20 08:30:00', 'Ajustement inventaire', 1, '2026-05-31 10:30:00', 0),
  (5, 5, 1, NULL, NULL, 'AJUSTEMENT', 'IN', 320, 4, '2026-05-20 08:30:00', 'Stock initial câble', 1, '2026-05-31 10:30:00', 0);

-- Data for `d_reglements` (3 rows)
INSERT INTO `d_reglements` (`id`, `code_reglement`, `utilisateur_id`, `tier_id`, `date_reglement`, `description`, `sens_reglement`, `mode_reglement_id`, `devise_id`, `taux_change`, `montant_total`, `montant_devise`, `montant_affecte`, `montant_restant`, `montant_commission`, `montant_net`, `caisse_id`, `numero_piece`, `date_echeance`, `statut_reglement`, `est_impute`, `cloture`, `valide`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'REG-00001', 4, 1, '2026-05-11 12:00:00', 'Règlement REG-00001', 'ENTREE', 1, 1, 1, 5000, 5000, 5000, 0, 0, 5000, 1, NULL, NULL, 'IMPUTE_PARTIEL', 1, 0, 1, 1, '2026-05-31 10:30:00', 0),
  (2, 'REG-00002', 4, 1, '2026-05-14 17:00:00', 'Règlement REG-00002', 'ENTREE', 3, 1, 1, 11820, 11820, 11820, 0, 15, 11805, 2, 'VIR-2026-001', NULL, 'IMPUTE_TOTAL', 1, 0, 1, 1, '2026-05-31 10:30:00', 0),
  (3, 'REG-00003', 4, 3, '2026-05-16 10:00:00', 'Règlement REG-00003', 'SORTIE', 3, 1, 1, 8000, 8000, 8000, 0, 0, 8000, 2, 'VIR-FOUR-001', NULL, 'IMPUTE_PARTIEL', 1, 0, 1, 1, '2026-05-31 10:30:00', 0);

-- Data for `d_document_reglements` (3 rows)
INSERT INTO `d_document_reglements` (`id`, `document_id`, `reglement_id`, `date_liaison`, `montant_affecte`, `montant_affecte_devise`, `regle`, `type_affectation`, `description`, `utilisateur_id`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 2, 1, '2026-05-31 10:30:00', 5000, 5000, 0, 'ACOMPTE', 'Acompte commande', 4, 1, '2026-05-31 10:30:00', 0),
  (2, 4, 2, '2026-05-31 10:30:00', 11820, 11820, 1, 'REGLEMENT', 'Règlement facture client', 4, 1, '2026-05-31 10:30:00', 0),
  (3, 7, 3, '2026-05-31 10:30:00', 8000, 8000, 0, 'REGLEMENT', 'Paiement partiel fournisseur', 4, 1, '2026-05-31 10:30:00', 0);

-- Data for `journaux_audit` (4 rows)
INSERT INTO `journaux_audit` (`id`, `utilisateur_id`, `action`, `table_cible`, `enregistrement_id`, `ancienne_valeur`, `nouvelle_valeur`, `description`, `adresse_ip`, `hostname`, `date_action`) VALUES
  (1, 1, 'LOGIN', 'p_utilisateurs', 1, NULL, '{"login":"admin"}', 'Connexion administrateur', '127.0.0.1', 'localhost', '2026-05-31 10:30:00'),
  (2, 2, 'CREATE', 'd_documents', 1, NULL, '{"reference":"DEV-00001"}', 'Création devis', '192.168.1.20', 'poste-vente', '2026-05-31 10:30:00'),
  (3, 3, 'VALIDATE', 'd_documents', 3, '{"status":"BROUILLON"}', '{"status":"CLOTURE"}', 'Validation BL', '192.168.1.21', 'poste-stock', '2026-05-31 10:30:00'),
  (4, 4, 'CREATE', 'd_reglements', 2, NULL, '{"montant":11820}', 'Création règlement', '192.168.1.22', 'poste-compta', '2026-05-31 10:30:00');

-- Reset AUTO_INCREMENT values
ALTER TABLE `d_adresses_livraison` AUTO_INCREMENT = 5;
ALTER TABLE `d_articles` AUTO_INCREMENT = 6;
ALTER TABLE `d_documents` AUTO_INCREMENT = 9;
ALTER TABLE `d_document_lignes` AUTO_INCREMENT = 15;
ALTER TABLE `d_document_reglements` AUTO_INCREMENT = 4;
ALTER TABLE `d_familles` AUTO_INCREMENT = 5;
ALTER TABLE `d_lots_sn` AUTO_INCREMENT = 4;
ALTER TABLE `d_mouvements_stock` AUTO_INCREMENT = 6;
ALTER TABLE `d_projets` AUTO_INCREMENT = 4;
ALTER TABLE `d_reglements` AUTO_INCREMENT = 4;
ALTER TABLE `d_stock` AUTO_INCREMENT = 7;
ALTER TABLE `d_tiers` AUTO_INCREMENT = 6;
ALTER TABLE `d_utilisateur_depots` AUTO_INCREMENT = 7;
ALTER TABLE `journaux_audit` AUTO_INCREMENT = 5;
ALTER TABLE `p_caisses` AUTO_INCREMENT = 4;
ALTER TABLE `p_depots` AUTO_INCREMENT = 4;
ALTER TABLE `p_devises` AUTO_INCREMENT = 4;
ALTER TABLE `p_informations_societe` AUTO_INCREMENT = 3;
ALTER TABLE `p_modes_reglement` AUTO_INCREMENT = 5;
ALTER TABLE `p_numerotation_documents` AUTO_INCREMENT = 9;
ALTER TABLE `p_permissions` AUTO_INCREMENT = 41;
ALTER TABLE `p_roles` AUTO_INCREMENT = 6;
ALTER TABLE `p_statuts_documents` AUTO_INCREMENT = 33;
ALTER TABLE `p_tvas` AUTO_INCREMENT = 5;
ALTER TABLE `p_types_documents` AUTO_INCREMENT = 9;
ALTER TABLE `p_unites` AUTO_INCREMENT = 6;
ALTER TABLE `p_utilisateurs` AUTO_INCREMENT = 5;

COMMIT;
