-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 31, 2026 at 11:28 AM
-- Server version: 8.0.17
-- PHP Version: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Reusable commercial schema. The installer selects the target database.
-- --------------------------------------------------------

--
-- Table structure for table `d_adresses_livraison`
--

CREATE TABLE `d_adresses_livraison` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `tier_id` bigint(20) UNSIGNED NOT NULL,
  `nom_adresse` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `adresse` varchar(500) COLLATE utf8mb4_general_ci NOT NULL,
  `utilisateur_id` varchar(150) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telephone` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `code_postal` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ville` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `region` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `pays` varchar(100) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'Maroc',
  `instructions_livraison` text COLLATE utf8mb4_general_ci,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_articles`
--

CREATE TABLE `d_articles` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_article` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `designation` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci,
  `famille_id` bigint(20) UNSIGNED DEFAULT NULL,
  `type_article` enum('PRODUIT','SERVICE','NUMERIQUE','MATIERE_PREMIERE') COLLATE utf8mb4_general_ci NOT NULL,
  `unite_id` bigint(20) UNSIGNED DEFAULT NULL,
  `unite_secondaire_id` bigint(20) UNSIGNED DEFAULT NULL,
  `prix_achat_ht` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `prix_achat_ttc` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `prix_vente_ht` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `prix_vente_ttc` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `prix_net` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `tva_id` bigint(20) UNSIGNED DEFAULT NULL,
  `suivi_stock` tinyint(1) NOT NULL DEFAULT '1',
  `mode_valorisation_stock` enum('CMUP','FIFO','LIFO','LOT','SN','FEFO','AUCUN') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'CMUP',
  `prix_revient_unitaire` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `quantite_min_stock` decimal(18,4) NOT NULL DEFAULT '0.0000',
  `quantite_max_stock` decimal(18,4) DEFAULT NULL,
  `gestion_lot` tinyint(1) NOT NULL DEFAULT '0',
  `gestion_numero_serie` tinyint(1) NOT NULL DEFAULT '0',
  `article_compose` tinyint(1) NOT NULL DEFAULT '0',
  `interdire_achat` tinyint(1) NOT NULL DEFAULT '0',
  `interdire_vente` tinyint(1) NOT NULL DEFAULT '0',
  `interdire_commande` tinyint(1) NOT NULL DEFAULT '0',
  `exclure_statistiques` tinyint(1) NOT NULL DEFAULT '0',
  `image_url` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_documents`
--

CREATE TABLE `d_documents` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `type_document_id` bigint(20) UNSIGNED NOT NULL,
  `reference_document` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `document_origine_id` bigint(20) UNSIGNED DEFAULT NULL,
  `tier_id` bigint(20) UNSIGNED DEFAULT NULL,
  `adresse_livraison_id` bigint(20) UNSIGNED DEFAULT NULL,
  `utilisateur_id` bigint(20) UNSIGNED DEFAULT NULL,
  `vendeur_id` bigint(20) UNSIGNED DEFAULT NULL,
  `montant_ht` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_remise` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_net_ht` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_tva` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_ttc` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_net_ttc` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_paye` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_restant` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `statut_document_id` bigint(20) UNSIGNED NOT NULL,
  `document_valide` tinyint(1) NOT NULL DEFAULT '0',
  `document_cloture` tinyint(1) NOT NULL DEFAULT '0',
  `date_document` datetime NOT NULL,
  `date_livraison_prevue` datetime DEFAULT NULL,
  `date_livraison_effective` datetime DEFAULT NULL,
  `transforme` int(11) NOT NULL DEFAULT '0',
  `date_transforme` datetime DEFAULT NULL,
  `commentaire` text COLLATE utf8mb4_general_ci,
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_document_lignes`
--

CREATE TABLE `d_document_lignes` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `document_id` bigint(20) UNSIGNED NOT NULL,
  `numero_ligne` int(10) UNSIGNED NOT NULL,
  `article_id` bigint(20) UNSIGNED DEFAULT NULL,
  `reference_article` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `designation` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `type_ligne` tinyint(3) UNSIGNED NOT NULL DEFAULT '0',
  `quantite` decimal(18,4) NOT NULL DEFAULT '0.0000',
  `unite_id` bigint(20) UNSIGNED DEFAULT NULL,
  `tva_id` bigint(20) UNSIGNED DEFAULT NULL,
  `code_tva` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `tva_percentage` decimal(5,2) NOT NULL DEFAULT '0.00',
  `remise_percentage` decimal(5,2) NOT NULL DEFAULT '0.00',
  `prix_unitaire_ht` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `prix_unitaire_ttc` decimal(18,6) GENERATED ALWAYS AS ((`prix_unitaire_ht` * (1 + (`tva_percentage` / 100)))) STORED,
  `prix_unitaire_net_ht` decimal(18,6) GENERATED ALWAYS AS ((`prix_unitaire_ht` - ((`prix_unitaire_ht` * `remise_percentage` / 100)))) STORED,
  `prix_unitaire_net_ttc` decimal(18,6) GENERATED ALWAYS AS ((`prix_unitaire_ttc` - ((`prix_unitaire_ttc` * `remise_percentage` / 100)))) STORED,
  `prix_revient_unitaire` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `derniere_prix_achat` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `unitaire_remise` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `unitaire_marge` decimal(18,6) GENERATED ALWAYS AS ((`prix_unitaire_net_ht` - `prix_revient_unitaire`)) STORED,
  `unitaire_tva` decimal(5,2) GENERATED ALWAYS AS (`prix_unitaire_ht` * `tva_percentage` / 100) STORED,
  `montant_ht` decimal(18,6) GENERATED ALWAYS AS ((`quantite` * `prix_unitaire_ht`)) STORED,
  `montant_ttc` decimal(18,6) GENERATED ALWAYS AS ((`quantite` * `prix_unitaire_ttc`)) STORED,
  `montant_net_ht` decimal(18,6) GENERATED ALWAYS AS ((`quantite` * `prix_unitaire_net_ht`)) STORED,
  `montant_net_ttc` decimal(18,6) GENERATED ALWAYS AS ((`quantite` * `prix_unitaire_net_ttc`)) STORED,
  `montant_remise` decimal(18,6) GENERATED ALWAYS AS ((`quantite` * `unitaire_remise`)) STORED,
  `montant_marge` decimal(18,6) GENERATED ALWAYS AS ((`quantite` * `unitaire_marge`)) STORED,
  `montant_tva` decimal(18,6) GENERATED ALWAYS AS ((`quantite` * `unitaire_tva`)) STORED,
  `depot_id` bigint(20) UNSIGNED DEFAULT NULL,
  `impact_stock` tinyint(1) NOT NULL DEFAULT '1',
  `valorise_stock` tinyint(1) NOT NULL DEFAULT '1',
  `ligne_source_id` bigint(20) UNSIGNED DEFAULT NULL,
  `document_source_id` bigint(20) UNSIGNED DEFAULT NULL,
  `projet_id` bigint(20) UNSIGNED DEFAULT NULL,
  `date_livraison_prevue` datetime DEFAULT NULL,
  `date_livraison_effective` datetime DEFAULT NULL,
  `transforme` int(11) NOT NULL DEFAULT '0',
  `date_transforme` datetime DEFAULT NULL,
  `numero_lot_sn` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `date_peremption` date DEFAULT NULL,
  `notes` text COLLATE utf8mb4_general_ci,
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_document_reglements`
--

CREATE TABLE `d_document_reglements` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `document_id` bigint(20) UNSIGNED NOT NULL,
  `reglement_id` bigint(20) UNSIGNED NOT NULL,
  `date_liaison` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `montant_affecte` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_affecte_devise` decimal(18,6) DEFAULT NULL,
  `regle` tinyint(1) NOT NULL DEFAULT '0',
  `type_affectation` enum('ACOMPTE','REGLEMENT','AVANCE','AVOIR','ECART') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'REGLEMENT',
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `utilisateur_id` bigint(20) UNSIGNED DEFAULT NULL,
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_familles`
--

CREATE TABLE `d_familles` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_famille` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_famille` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci,
  `type_famille` enum('PRODUIT','SERVICE','NUMERIQUE','MATIERE_PREMIERE') COLLATE utf8mb4_general_ci NOT NULL,
  `suivi_stock` tinyint(1) NOT NULL DEFAULT '1',
  `mode_valorisation_stock` enum('CMUP','FIFO','LIFO','LOT','SN','FEFO','AUCUN') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'CMUP',
  `tva_id` bigint(20) UNSIGNED DEFAULT NULL,
  `gestion_lot` tinyint(1) NOT NULL DEFAULT '0',
  `gestion_numero_serie` tinyint(1) NOT NULL DEFAULT '0',
  `unite_id` bigint(20) UNSIGNED DEFAULT NULL,
  `depot_id` bigint(20) UNSIGNED DEFAULT NULL,
  `exclure_statistiques` tinyint(1) NOT NULL DEFAULT '0',
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_lots_sn`
--

CREATE TABLE `d_lots_sn` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `article_id` bigint(20) UNSIGNED NOT NULL,
  `numero_lot_sn` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `date_fabrication` date DEFAULT NULL,
  `date_peremption` date DEFAULT NULL,
  `quantite_initiale` decimal(18,4) NOT NULL DEFAULT '0.0000',
  `quantite_actuelle` decimal(18,4) NOT NULL DEFAULT '0.0000',
  `prix_achat_unitaire` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `depot_id` bigint(20) UNSIGNED NOT NULL,
  `fournisseur_id` bigint(20) UNSIGNED DEFAULT NULL,
  `document_entree_id` bigint(20) UNSIGNED DEFAULT NULL,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_mouvements_stock`
--

CREATE TABLE `d_mouvements_stock` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `article_id` bigint(20) UNSIGNED NOT NULL,
  `depot_id` bigint(20) UNSIGNED NOT NULL,
  `document_id` bigint(20) UNSIGNED DEFAULT NULL,
  `document_ligne_id` bigint(20) UNSIGNED DEFAULT NULL,
  `type_mouvement` enum('ENTREE','SORTIE','TRANSFERT','AJUSTEMENT','INVENTAIRE') COLLATE utf8mb4_general_ci NOT NULL,
  `sens_mouvement` enum('IN','OUT') COLLATE utf8mb4_general_ci NOT NULL,
  `quantite` decimal(18,4) NOT NULL,
  `prix_revient_unitaire` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `date_mouvement` datetime NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_projets`
--

CREATE TABLE `d_projets` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_projet` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_projet` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci,
  `tier_id` bigint(20) UNSIGNED DEFAULT NULL,
  `utilisateur_id` bigint(20) UNSIGNED DEFAULT NULL,
  `date_debut` date DEFAULT NULL,
  `date_fin_prevue` date DEFAULT NULL,
  `date_fin_reelle` date DEFAULT NULL,
  `priorite` enum('BASSE','NORMALE','HAUTE','URGENTE') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'NORMALE',
  `budget_prevu` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `budget_reel` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_facture` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `notes` text COLLATE utf8mb4_general_ci,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_reglements`
--

CREATE TABLE `d_reglements` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_reglement` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `utilisateur_id` bigint(20) UNSIGNED DEFAULT NULL,
  `tier_id` bigint(20) UNSIGNED NOT NULL,
  `date_reglement` datetime NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sens_reglement` enum('ENTREE','SORTIE') COLLATE utf8mb4_general_ci NOT NULL,
  `mode_reglement_id` bigint(20) UNSIGNED DEFAULT NULL,
  `devise_id` bigint(20) UNSIGNED DEFAULT NULL,
  `taux_change` decimal(18,6) NOT NULL DEFAULT '1.000000',
  `montant_total` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_devise` decimal(18,6) DEFAULT NULL,
  `montant_affecte` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_restant` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_commission` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `montant_net` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `caisse_id` bigint(20) UNSIGNED DEFAULT NULL,
  `numero_piece` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `date_echeance` datetime DEFAULT NULL,
  `statut_reglement` enum('BROUILLON','VALIDE','IMPUTE_PARTIEL','IMPUTE_TOTAL','ANNULE','IMPAYE') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'BROUILLON',
  `est_impute` tinyint(1) NOT NULL DEFAULT '0',
  `date_impaye` datetime DEFAULT NULL,
  `cloture` tinyint(1) NOT NULL DEFAULT '0',
  `valide` tinyint(1) NOT NULL DEFAULT '0',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_stock`
--

CREATE TABLE `d_stock` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `article_id` bigint(20) UNSIGNED NOT NULL,
  `depot_id` bigint(20) UNSIGNED NOT NULL,
  `quantite_stock` decimal(18,4) NOT NULL DEFAULT '0.0000',
  `quantite_reservee` decimal(18,4) NOT NULL DEFAULT '0.0000',
  `quantite_disponible` decimal(18,4) GENERATED ALWAYS AS ((`quantite_stock` - `quantite_reservee`)) STORED,
  `cout_moyen` decimal(18,6) NOT NULL DEFAULT '0.000000',
  `date_dernier_mouvement` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_tiers`
--

CREATE TABLE `d_tiers` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_tiers` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `raison_sociale` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_commercial` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `type_tiers` enum('CLIENT','FOURNISSEUR','PROSPECT','TRANSPORTEUR','AUTRE') COLLATE utf8mb4_general_ci NOT NULL,
  `contact_principal` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telephone` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telephone_secondaire` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `site_web` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `adresse` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `code_postal` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ville` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `region` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `pays` varchar(100) COLLATE utf8mb4_general_ci DEFAULT 'Maroc',
  `identifiant_fiscal` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ice` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rc` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `patente` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cnss` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tva_id` bigint(20) UNSIGNED DEFAULT NULL,
  `activite` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `plafond_credit` decimal(18,2) NOT NULL DEFAULT '0.00',
  `delai_paiement_jours` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `devise_id` bigint(20) UNSIGNED DEFAULT NULL,
  `mode_paiement_id` bigint(20) UNSIGNED DEFAULT NULL,
  `code_edi` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `type_edi` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `facture_electronique` tinyint(1) NOT NULL DEFAULT '0',
  `emission_fe` tinyint(1) NOT NULL DEFAULT '0',
  `application_fe` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `notes` text COLLATE utf8mb4_general_ci,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `d_utilisateur_depots`
--

CREATE TABLE `d_utilisateur_depots` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `utilisateur_id` bigint(20) UNSIGNED NOT NULL,
  `depot_id` bigint(20) UNSIGNED NOT NULL,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `journaux_audit`
--

CREATE TABLE `journaux_audit` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `utilisateur_id` bigint(20) UNSIGNED DEFAULT NULL,
  `action` enum('CREATE','UPDATE','DELETE','RESTORE','LOGIN','LOGOUT','VALIDATE','CANCEL','PRINT','EXPORT') COLLATE utf8mb4_general_ci NOT NULL,
  `table_cible` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `enregistrement_id` bigint(20) UNSIGNED DEFAULT NULL,
  `ancienne_valeur` json DEFAULT NULL,
  `nouvelle_valeur` json DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `adresse_ip` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `hostname` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `date_action` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_caisses`
--

CREATE TABLE `p_caisses` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_caisse` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_caisse` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `type_caisse` enum('CAISSE','BANQUE','TERMINAL_PAIEMENT','AUTRE') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'CAISSE',
  `banque_nom` varchar(150) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `numero_compte` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `iban` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rib` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_depots`
--

CREATE TABLE `p_depots` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_depot` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_depot` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `adresse` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_devises`
--

CREATE TABLE `p_devises` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_devise` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_devise` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `symbole` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `devise_principale` tinyint(1) NOT NULL DEFAULT '0',
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_informations_societe`
--

CREATE TABLE `p_informations_societe` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `raison_sociale` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_commercial` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `activite` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `identifiant_fiscal` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ice` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rc` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `patente` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cnss` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `adresse` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `code_postal` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ville` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `region` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `pays` varchar(100) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'Maroc',
  `telephone` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `site_web` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `logo_url` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `devise_id` bigint(20) UNSIGNED DEFAULT NULL,
  `tva_id` bigint(20) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_modes_reglement`
--

CREATE TABLE `p_modes_reglement` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_mode_reglement` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_mode_reglement` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `type_mode` enum('ESPECE','CHEQUE','VIREMENT','CARTE','EFFET','AVOIR','AUTRE') COLLATE utf8mb4_general_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `requiert_banque` tinyint(1) NOT NULL DEFAULT '0',
  `requiert_numero_piece` tinyint(1) NOT NULL DEFAULT '0',
  `requiert_date_echeance` tinyint(1) NOT NULL DEFAULT '0',
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_numerotation_documents`
--

CREATE TABLE `p_numerotation_documents` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `type_document_id` bigint(20) UNSIGNED NOT NULL,
  `prefixe` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `annee` int(10) UNSIGNED NOT NULL,
  `dernier_numero` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `longueur_numero` int(10) UNSIGNED NOT NULL DEFAULT '4',
  `actif` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_permissions`
--

CREATE TABLE `p_permissions` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `module` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `action` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_roles`
--

CREATE TABLE `p_roles` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `display_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_role_permissions`
--

CREATE TABLE `p_role_permissions` (
  `role_id` bigint(20) UNSIGNED NOT NULL,
  `permission_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_statuts_documents`
--

CREATE TABLE `p_statuts_documents` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_statut` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_statut` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `type_document_id` bigint(20) UNSIGNED NOT NULL,
  `ordre_affichage` int(11) NOT NULL DEFAULT '0',
  `couleur` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `document_verrouille` tinyint(1) NOT NULL DEFAULT '0',
  `impacte_stock` tinyint(1) NOT NULL DEFAULT '0',
  `impacte_reglement` tinyint(1) NOT NULL DEFAULT '0',
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_tvas`
--

CREATE TABLE `p_tvas` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_tva` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_tva` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `taux` decimal(6,3) NOT NULL DEFAULT '0.000',
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_types_documents`
--

CREATE TABLE `p_types_documents` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_type_document` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_type_document` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `domaine` enum('VENTE','ACHAT','STOCK','INTERNE') COLLATE utf8mb4_general_ci NOT NULL,
  `sens_stock` enum('AUCUN','ENTREE','SORTIE') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'AUCUN',
  `impacte_stock` tinyint(1) NOT NULL DEFAULT '0',
  `impacte_reglement` tinyint(1) NOT NULL DEFAULT '0',
  `actif` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_unites`
--

CREATE TABLE `p_unites` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_unite` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_unite` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `symbole` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `type_unite` enum('QUANTITE','POIDS','VOLUME','LONGUEUR','SURFACE','TEMPS','AUTRE') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'QUANTITE',
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_users_roles`
--

CREATE TABLE `p_users_roles` (
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `role_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_utilisateurs`
--

CREATE TABLE `p_utilisateurs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `nom_utilisateur` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `code_utilisateur` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `telephone` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mot_de_passe_hash` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `est_administrateur` tinyint(1) NOT NULL DEFAULT '0',
  `date_mot_de_passe` datetime DEFAULT NULL,
  `date_derniere_connexion` datetime DEFAULT NULL,
  `statut_mot_de_passe` enum('ACTIF','A_CHANGER','EXPIRE','BLOQUE') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'ACTIF',
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `tentatives_connexion` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `date_blocage` datetime DEFAULT NULL,
  `image_url` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cree_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modifie_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `supprime_par` bigint(20) UNSIGNED DEFAULT NULL,
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--


-- ------------------------------------------------------------------------
-- Required configuration data
-- Password for all application users: 12345678 (bcrypt)
-- ------------------------------------------------------------------------


INSERT INTO `p_devises` (`id`, `code_devise`, `nom_devise`, `symbole`, `devise_principale`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'MAD', 'Dirham Marocain', 'DH', 1, 1, NULL, '2026-05-31 10:30:00', 0),
  (2, 'EUR', 'Euro', '€', 0, 1, NULL, '2026-05-31 10:30:00', 0),
  (3, 'USD', 'Dollar Américain', '$', 0, 1, NULL, '2026-05-31 10:30:00', 0);

INSERT INTO `p_tvas` (`id`, `code_tva`, `nom_tva`, `taux`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'TVA0', 'Exonéré TVA', 0, 1, NULL, '2026-05-31 10:30:00', 0),
  (2, 'TVA7', 'TVA réduite 7%', 7, 1, NULL, '2026-05-31 10:30:00', 0),
  (3, 'TVA10', 'TVA intermédiaire 10%', 10, 1, NULL, '2026-05-31 10:30:00', 0),
  (4, 'TVA20', 'TVA normale 20%', 20, 1, NULL, '2026-05-31 10:30:00', 0);

INSERT INTO `p_unites` (`id`, `code_unite`, `nom_unite`, `symbole`, `type_unite`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'PCS', 'Pièce', 'pcs', 'QUANTITE', 1, NULL, '2026-08-01 10:00:00', 0),
  (2, 'KG', 'Kilogramme', 'kg', 'POIDS', 1, NULL, '2026-08-01 10:00:00', 0),
  (3, 'L', 'Litre', 'L', 'VOLUME', 1, NULL, '2026-08-01 10:00:00', 0),
  (4, 'H', 'Heure', 'h', 'TEMPS', 1, NULL, '2026-08-01 10:00:00', 0),
  (5, 'M', 'Mètre', 'm', 'LONGUEUR', 1, NULL, '2026-08-01 10:00:00', 0),
  (6, 'M2', 'Mètre carré', 'm²', 'SURFACE', 1, NULL, '2026-08-01 10:00:00', 0),
  (7, 'BOX', 'Boîte', 'boîte', 'QUANTITE', 1, NULL, '2026-08-01 10:00:00', 0),
  (8, 'PACK', 'Paquet', 'paq', 'QUANTITE', 1, NULL, '2026-08-01 10:00:00', 0),
  (9, 'DAY', 'Journée', 'j', 'TEMPS', 1, NULL, '2026-08-01 10:00:00', 0),
  (10, 'ML', 'Millilitre', 'ml', 'VOLUME', 1, NULL, '2026-08-01 10:00:00', 0);

INSERT INTO `p_types_documents` (`id`, `code_type_document`, `nom_type_document`, `domaine`, `sens_stock`, `impacte_stock`, `impacte_reglement`, `actif`) VALUES
  (1, 'DEV', 'Devis client', 'VENTE', 'AUCUN', 0, 0, 1),
  (2, 'BCV', 'Bon de commande client', 'VENTE', 'AUCUN', 0, 0, 1),
  (3, 'BLV', 'Bon de livraison vente', 'VENTE', 'SORTIE', 1, 0, 1),
  (4, 'FACV', 'Facture vente', 'VENTE', 'AUCUN', 0, 1, 1),
  (5, 'BCA', 'Bon de commande achat', 'ACHAT', 'AUCUN', 0, 0, 1),
  (6, 'BRA', 'Bon de réception achat', 'ACHAT', 'ENTREE', 1, 0, 1),
  (7, 'FACA', 'Facture achat', 'ACHAT', 'AUCUN', 0, 1, 1),
  (8, 'INV', 'Inventaire stock', 'STOCK', 'AUCUN', 1, 0, 1);

INSERT INTO `p_utilisateurs` (`id`, `nom_utilisateur`, `description`, `code_utilisateur`, `email`, `telephone`, `mot_de_passe_hash`, `est_administrateur`, `date_mot_de_passe`, `statut_mot_de_passe`, `actif`, `tentatives_connexion`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'admin', 'Administrateur système', 'ADMIN', 'admin@azenz.local', '0600000001', '$2b$12$pxa41rcBz9jrnsM3zIC8C.NU1/YVoMk1mJ6z3NJAOq1UtFDd.XndC', 1, '2026-08-01 10:00:00', 'ACTIF', 1, 0, NULL, '2026-08-01 10:00:00', 0);

INSERT INTO `p_depots` (`id`, `code_depot`, `nom_depot`, `description`, `adresse`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'DEP-PRINCIPAL', 'Dépôt principal', 'Dépôt par défaut', 'Zone industrielle, Casablanca', 1, 1, '2026-08-01 10:00:00', 0);

INSERT INTO `p_modes_reglement` (`id`, `code_mode_reglement`, `nom_mode_reglement`, `type_mode`, `description`, `requiert_banque`, `requiert_numero_piece`, `requiert_date_echeance`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'ESP', 'Espèces', 'ESPECE', 'Paiement en espèces', 0, 0, 0, 1, 1, '2026-08-01 10:00:00', 0),
  (2, 'CHQ', 'Chèque', 'CHEQUE', 'Paiement par chèque', 1, 1, 1, 1, 1, '2026-08-01 10:00:00', 0),
  (3, 'VIR', 'Virement bancaire', 'VIREMENT', 'Paiement par virement', 1, 1, 0, 1, 1, '2026-08-01 10:00:00', 0),
  (4, 'CB', 'Carte bancaire', 'CARTE', 'Paiement par carte', 0, 1, 0, 1, 1, '2026-08-01 10:00:00', 0),
  (5, 'EFF', 'Effet de commerce', 'EFFET', 'Paiement par effet', 1, 1, 1, 1, 1, '2026-08-01 10:00:00', 0),
  (6, 'AVO', 'Avoir', 'AVOIR', 'Compensation par avoir', 0, 1, 0, 1, 1, '2026-08-01 10:00:00', 0),
  (7, 'AUT', 'Autre moyen', 'AUTRE', 'Autre moyen de paiement', 0, 0, 0, 1, 1, '2026-08-01 10:00:00', 0);

INSERT INTO `p_caisses` (`id`, `code_caisse`, `nom_caisse`, `type_caisse`, `banque_nom`, `numero_compte`, `iban`, `rib`, `description`, `actif`, `cree_par`, `date_creation`, `supprime`) VALUES
  (1, 'CAISSE-PRINCIPALE', 'Caisse principale', 'CAISSE', NULL, NULL, NULL, NULL, 'Caisse par défaut', 1, 1, '2026-08-01 10:00:00', 0);

INSERT INTO `p_roles` (`id`, `name`, `display_name`, `description`, `active`, `date_creation`) VALUES
  (1, 'admin', 'Administrateur', 'Accès complet', 1, '2026-05-31 10:30:00'),
  (2, 'manager', 'Manager', 'Gestion commerciale', 1, '2026-05-31 10:30:00'),
  (3, 'vendeur', 'Vendeur', 'Vente et consultation stock', 1, '2026-05-31 10:30:00'),
  (4, 'magasinier', 'Magasinier', 'Stock et mouvements', 1, '2026-05-31 10:30:00'),
  (5, 'comptable', 'Comptable', 'Règlements et reporting', 1, '2026-05-31 10:30:00');

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

INSERT INTO `p_users_roles` (`user_id`, `role_id`) VALUES
  (1, 1);

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

INSERT INTO `p_numerotation_documents` (`id`, `type_document_id`, `prefixe`, `annee`, `dernier_numero`, `longueur_numero`, `actif`) VALUES
  (1, 1, 'DEV-', 2026, 26, 5, 1),
  (2, 2, 'BCV-', 2026, 27, 5, 1),
  (3, 3, 'BLV-', 2026, 28, 5, 1),
  (4, 4, 'FACV-', 2026, 29, 5, 1),
  (5, 5, 'BCA-', 2026, 30, 5, 1),
  (6, 6, 'BRA-', 2026, 31, 5, 1),
  (7, 7, 'FACA-', 2026, 32, 5, 1),
  (8, 8, 'INV-', 2026, 33, 5, 1);

INSERT INTO `p_informations_societe` (`id`, `raison_sociale`, `nom_commercial`, `activite`, `identifiant_fiscal`, `ice`, `rc`, `patente`, `cnss`, `adresse`, `code_postal`, `ville`, `region`, `pays`, `telephone`, `email`, `site_web`, `logo_url`, `devise_id`, `tva_id`) VALUES
  (1, 'Azenz Test Company SARL', 'Azenz Test Company', 'Commerce et services', 'IF10000001', '001234567890123', 'RC-CAS-100001', 'PAT-100001', 'CNSS-100001', 'Boulevard Zerktouni, Casablanca', '20000', 'Casablanca', 'Casablanca-Settat', 'Maroc', '0522000000', 'contact@azenz.local', 'https://azenz.local', NULL, 1, 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `d_adresses_livraison`
--
ALTER TABLE `d_adresses_livraison`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_adresse_createur` (`cree_par`),
  ADD KEY `fk_adresse_modificateur` (`modifie_par`),
  ADD KEY `fk_adresse_supprimeur` (`supprime_par`),
  ADD KEY `idx_tier` (`tier_id`),
  ADD KEY `idx_ville` (`ville`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `d_articles`
--
ALTER TABLE `d_articles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_article` (`code_article`),
  ADD KEY `fk_articles_unite_secondaire` (`unite_secondaire_id`),
  ADD KEY `fk_articles_createur` (`cree_par`),
  ADD KEY `fk_articles_modificateur` (`modifie_par`),
  ADD KEY `fk_articles_supprimeur` (`supprime_par`),
  ADD KEY `idx_famille` (`famille_id`),
  ADD KEY `idx_type_article` (`type_article`),
  ADD KEY `idx_unite` (`unite_id`),
  ADD KEY `idx_tva` (`tva_id`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `d_documents`
--
ALTER TABLE `d_documents`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_document_reference` (`type_document_id`,`reference_document`),
  ADD KEY `fk_documents_origine` (`document_origine_id`),
  ADD KEY `fk_documents_adresse_livraison` (`adresse_livraison_id`),
  ADD KEY `fk_documents_utilisateur` (`utilisateur_id`),
  ADD KEY `fk_documents_vendeur` (`vendeur_id`),
  ADD KEY `fk_documents_createur` (`cree_par`),
  ADD KEY `fk_documents_modificateur` (`modifie_par`),
  ADD KEY `fk_documents_supprimeur` (`supprime_par`),
  ADD KEY `idx_type_document` (`type_document_id`),
  ADD KEY `idx_tier` (`tier_id`),
  ADD KEY `idx_statut` (`statut_document_id`),
  ADD KEY `idx_date_document` (`date_document`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `d_document_lignes`
--
ALTER TABLE `d_document_lignes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_document_numero_ligne` (`document_id`,`numero_ligne`),
  ADD KEY `fk_lignes_tva` (`tva_id`),
  ADD KEY `fk_lignes_ligne_source` (`ligne_source_id`),
  ADD KEY `fk_lignes_document_source` (`document_source_id`),
  ADD KEY `fk_lignes_createur` (`cree_par`),
  ADD KEY `fk_lignes_modificateur` (`modifie_par`),
  ADD KEY `fk_lignes_supprimeur` (`supprime_par`),
  ADD KEY `idx_document` (`document_id`),
  ADD KEY `idx_article` (`article_id`),
  ADD KEY `idx_unite` (`unite_id`),
  ADD KEY `idx_depot` (`depot_id`),
  ADD KEY `idx_projet` (`projet_id`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `d_document_reglements`
--
ALTER TABLE `d_document_reglements`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_document_reglement` (`document_id`,`reglement_id`),
  ADD KEY `fk_document_reglements_utilisateur` (`utilisateur_id`),
  ADD KEY `fk_document_reglements_createur` (`cree_par`),
  ADD KEY `fk_document_reglements_modificateur` (`modifie_par`),
  ADD KEY `fk_document_reglements_supprimeur` (`supprime_par`),
  ADD KEY `idx_document` (`document_id`),
  ADD KEY `idx_reglement` (`reglement_id`),
  ADD KEY `idx_date_liaison` (`date_liaison`),
  ADD KEY `idx_type_affectation` (`type_affectation`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `d_familles`
--
ALTER TABLE `d_familles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_famille` (`code_famille`),
  ADD KEY `fk_familles_createur` (`cree_par`),
  ADD KEY `fk_familles_modificateur` (`modifie_par`),
  ADD KEY `fk_familles_supprimeur` (`supprime_par`),
  ADD KEY `idx_type_famille` (`type_famille`),
  ADD KEY `idx_tva` (`tva_id`),
  ADD KEY `idx_unite` (`unite_id`),
  ADD KEY `idx_depot` (`depot_id`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `d_lots_sn`
--
ALTER TABLE `d_lots_sn`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_lot_article_depot` (`article_id`,`depot_id`,`numero_lot_sn`),
  ADD KEY `fk_lots_document_entree` (`document_entree_id`),
  ADD KEY `fk_lots_createur` (`cree_par`),
  ADD KEY `fk_lots_modificateur` (`modifie_par`),
  ADD KEY `fk_lots_supprimeur` (`supprime_par`),
  ADD KEY `idx_article` (`article_id`),
  ADD KEY `idx_depot` (`depot_id`),
  ADD KEY `idx_fournisseur` (`fournisseur_id`),
  ADD KEY `idx_date_peremption` (`date_peremption`),
  ADD KEY `idx_actif` (`actif`);

--
-- Indexes for table `d_mouvements_stock`
--
ALTER TABLE `d_mouvements_stock`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_mouvements_createur` (`cree_par`),
  ADD KEY `fk_mouvements_modificateur` (`modifie_par`),
  ADD KEY `fk_mouvements_supprimeur` (`supprime_par`),
  ADD KEY `idx_article` (`article_id`),
  ADD KEY `idx_depot` (`depot_id`),
  ADD KEY `idx_document` (`document_id`),
  ADD KEY `idx_document_ligne` (`document_ligne_id`),
  ADD KEY `idx_type_mouvement` (`type_mouvement`),
  ADD KEY `idx_date_mouvement` (`date_mouvement`);

--
-- Indexes for table `d_projets`
--
ALTER TABLE `d_projets`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_projet` (`code_projet`),
  ADD KEY `fk_projets_createur` (`cree_par`),
  ADD KEY `fk_projets_modificateur` (`modifie_par`),
  ADD KEY `fk_projets_supprimeur` (`supprime_par`),
  ADD KEY `idx_tier` (`tier_id`),
  ADD KEY `idx_utilisateur` (`utilisateur_id`),
  ADD KEY `idx_priorite` (`priorite`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `d_reglements`
--
ALTER TABLE `d_reglements`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_reglement` (`code_reglement`),
  ADD KEY `fk_reglements_createur` (`cree_par`),
  ADD KEY `fk_reglements_modificateur` (`modifie_par`),
  ADD KEY `fk_reglements_supprimeur` (`supprime_par`),
  ADD KEY `idx_tier` (`tier_id`),
  ADD KEY `idx_utilisateur` (`utilisateur_id`),
  ADD KEY `idx_mode_reglement` (`mode_reglement_id`),
  ADD KEY `idx_devise` (`devise_id`),
  ADD KEY `idx_caisse` (`caisse_id`),
  ADD KEY `idx_date_reglement` (`date_reglement`),
  ADD KEY `idx_statut_reglement` (`statut_reglement`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `d_stock`
--
ALTER TABLE `d_stock`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_stock_article_depot` (`article_id`,`depot_id`),
  ADD KEY `idx_article` (`article_id`),
  ADD KEY `idx_depot` (`depot_id`);

--
-- Indexes for table `d_tiers`
--
ALTER TABLE `d_tiers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_tiers` (`code_tiers`),
  ADD KEY `fk_tiers_mode_paiement` (`mode_paiement_id`),
  ADD KEY `fk_tiers_createur` (`cree_par`),
  ADD KEY `fk_tiers_modificateur` (`modifie_par`),
  ADD KEY `fk_tiers_supprimeur` (`supprime_par`),
  ADD KEY `idx_type_tiers` (`type_tiers`),
  ADD KEY `idx_raison_sociale` (`raison_sociale`),
  ADD KEY `idx_ville` (`ville`),
  ADD KEY `idx_tva` (`tva_id`),
  ADD KEY `idx_devise` (`devise_id`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `d_utilisateur_depots`
--
ALTER TABLE `d_utilisateur_depots`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_utilisateur_depot` (`utilisateur_id`,`depot_id`),
  ADD KEY `fk_utilisateur_depots_createur` (`cree_par`),
  ADD KEY `fk_utilisateur_depots_modificateur` (`modifie_par`),
  ADD KEY `fk_utilisateur_depots_supprimeur` (`supprime_par`),
  ADD KEY `idx_utilisateur` (`utilisateur_id`),
  ADD KEY `idx_depot` (`depot_id`);

--
-- Indexes for table `journaux_audit`
--
ALTER TABLE `journaux_audit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_utilisateur` (`utilisateur_id`),
  ADD KEY `idx_action` (`action`),
  ADD KEY `idx_table_cible` (`table_cible`),
  ADD KEY `idx_enregistrement` (`table_cible`,`enregistrement_id`),
  ADD KEY `idx_date_action` (`date_action`);

--
-- Indexes for table `p_caisses`
--
ALTER TABLE `p_caisses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_caisse` (`code_caisse`),
  ADD KEY `fk_caisses_createur` (`cree_par`),
  ADD KEY `fk_caisses_modificateur` (`modifie_par`),
  ADD KEY `fk_caisses_supprimeur` (`supprime_par`),
  ADD KEY `idx_nom_caisse` (`nom_caisse`),
  ADD KEY `idx_type_caisse` (`type_caisse`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `p_depots`
--
ALTER TABLE `p_depots`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_depot` (`code_depot`),
  ADD KEY `fk_depots_createur` (`cree_par`),
  ADD KEY `fk_depots_modificateur` (`modifie_par`),
  ADD KEY `fk_depots_supprimeur` (`supprime_par`),
  ADD KEY `idx_nom_depot` (`nom_depot`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `p_devises`
--
ALTER TABLE `p_devises`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_devise` (`code_devise`),
  ADD KEY `fk_devises_createur` (`cree_par`),
  ADD KEY `fk_devises_modificateur` (`modifie_par`),
  ADD KEY `fk_devises_supprimeur` (`supprime_par`),
  ADD KEY `idx_nom_devise` (`nom_devise`),
  ADD KEY `idx_devise_principale` (`devise_principale`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `p_informations_societe`
--
ALTER TABLE `p_informations_societe`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_devise` (`devise_id`),
  ADD KEY `idx_tva` (`tva_id`);

--
-- Indexes for table `p_modes_reglement`
--
ALTER TABLE `p_modes_reglement`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_mode_reglement` (`code_mode_reglement`),
  ADD KEY `fk_modes_reglement_createur` (`cree_par`),
  ADD KEY `fk_modes_reglement_modificateur` (`modifie_par`),
  ADD KEY `fk_modes_reglement_supprimeur` (`supprime_par`),
  ADD KEY `idx_nom_mode_reglement` (`nom_mode_reglement`),
  ADD KEY `idx_type_mode` (`type_mode`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `p_numerotation_documents`
--
ALTER TABLE `p_numerotation_documents`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_numerotation_type_annee` (`type_document_id`,`annee`),
  ADD KEY `idx_type_document` (`type_document_id`),
  ADD KEY `idx_annee` (`annee`),
  ADD KEY `idx_actif` (`actif`);

--
-- Indexes for table `p_permissions`
--
ALTER TABLE `p_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD UNIQUE KEY `uq_permission_module_action` (`module`,`action`),
  ADD KEY `idx_module` (`module`),
  ADD KEY `idx_action` (`action`);

--
-- Indexes for table `p_roles`
--
ALTER TABLE `p_roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `idx_name` (`name`),
  ADD KEY `idx_active` (`active`);

--
-- Indexes for table `p_role_permissions`
--
ALTER TABLE `p_role_permissions`
  ADD PRIMARY KEY (`role_id`,`permission_id`),
  ADD KEY `idx_permission` (`permission_id`);

--
-- Indexes for table `p_statuts_documents`
--
ALTER TABLE `p_statuts_documents`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_statut_type_code` (`type_document_id`,`code_statut`),
  ADD KEY `fk_statuts_documents_createur` (`cree_par`),
  ADD KEY `fk_statuts_documents_modificateur` (`modifie_par`),
  ADD KEY `idx_type_document` (`type_document_id`),
  ADD KEY `idx_ordre_affichage` (`ordre_affichage`),
  ADD KEY `idx_actif` (`actif`);

--
-- Indexes for table `p_tvas`
--
ALTER TABLE `p_tvas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_tva` (`code_tva`),
  ADD KEY `fk_tvas_createur` (`cree_par`),
  ADD KEY `fk_tvas_modificateur` (`modifie_par`),
  ADD KEY `fk_tvas_supprimeur` (`supprime_par`),
  ADD KEY `idx_nom_tva` (`nom_tva`),
  ADD KEY `idx_taux` (`taux`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `p_types_documents`
--
ALTER TABLE `p_types_documents`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_type_document` (`code_type_document`),
  ADD KEY `idx_domaine` (`domaine`),
  ADD KEY `idx_sens_stock` (`sens_stock`),
  ADD KEY `idx_actif` (`actif`);

--
-- Indexes for table `p_unites`
--
ALTER TABLE `p_unites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_unite` (`code_unite`),
  ADD KEY `fk_unites_createur` (`cree_par`),
  ADD KEY `fk_unites_modificateur` (`modifie_par`),
  ADD KEY `fk_unites_supprimeur` (`supprime_par`),
  ADD KEY `idx_nom_unite` (`nom_unite`),
  ADD KEY `idx_type_unite` (`type_unite`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- Indexes for table `p_users_roles`
--
ALTER TABLE `p_users_roles`
  ADD PRIMARY KEY (`user_id`,`role_id`),
  ADD KEY `idx_role` (`role_id`);

--
-- Indexes for table `p_utilisateurs`
--
ALTER TABLE `p_utilisateurs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nom_utilisateur` (`nom_utilisateur`),
  ADD UNIQUE KEY `code_utilisateur` (`code_utilisateur`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `fk_utilisateurs_createur` (`cree_par`),
  ADD KEY `fk_utilisateurs_modificateur` (`modifie_par`),
  ADD KEY `fk_utilisateurs_supprimeur` (`supprime_par`),
  ADD KEY `idx_nom_utilisateur` (`nom_utilisateur`),
  ADD KEY `idx_code_utilisateur` (`code_utilisateur`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_actif` (`actif`),
  ADD KEY `idx_statut_mot_de_passe` (`statut_mot_de_passe`),
  ADD KEY `idx_supprime` (`supprime`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `d_adresses_livraison`
--
ALTER TABLE `d_adresses_livraison`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_articles`
--
ALTER TABLE `d_articles`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_documents`
--
ALTER TABLE `d_documents`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_document_lignes`
--
ALTER TABLE `d_document_lignes`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_document_reglements`
--
ALTER TABLE `d_document_reglements`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_familles`
--
ALTER TABLE `d_familles`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_lots_sn`
--
ALTER TABLE `d_lots_sn`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_mouvements_stock`
--
ALTER TABLE `d_mouvements_stock`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_projets`
--
ALTER TABLE `d_projets`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_reglements`
--
ALTER TABLE `d_reglements`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_stock`
--
ALTER TABLE `d_stock`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_tiers`
--
ALTER TABLE `d_tiers`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `d_utilisateur_depots`
--
ALTER TABLE `d_utilisateur_depots`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `journaux_audit`
--
ALTER TABLE `journaux_audit`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_caisses`
--
ALTER TABLE `p_caisses`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_depots`
--
ALTER TABLE `p_depots`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_devises`
--
ALTER TABLE `p_devises`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_informations_societe`
--
ALTER TABLE `p_informations_societe`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_modes_reglement`
--
ALTER TABLE `p_modes_reglement`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_numerotation_documents`
--
ALTER TABLE `p_numerotation_documents`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_permissions`
--
ALTER TABLE `p_permissions`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_roles`
--
ALTER TABLE `p_roles`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_statuts_documents`
--
ALTER TABLE `p_statuts_documents`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_tvas`
--
ALTER TABLE `p_tvas`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_types_documents`
--
ALTER TABLE `p_types_documents`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_unites`
--
ALTER TABLE `p_unites`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `p_utilisateurs`
--
ALTER TABLE `p_utilisateurs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `d_adresses_livraison`
--
ALTER TABLE `d_adresses_livraison`
  ADD CONSTRAINT `fk_adresse_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_adresse_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_adresse_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_adresse_tiers` FOREIGN KEY (`tier_id`) REFERENCES `d_tiers` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Constraints for table `d_articles`
--
ALTER TABLE `d_articles`
  ADD CONSTRAINT `fk_articles_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_articles_famille` FOREIGN KEY (`famille_id`) REFERENCES `d_familles` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_articles_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_articles_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_articles_tva` FOREIGN KEY (`tva_id`) REFERENCES `p_tvas` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_articles_unite` FOREIGN KEY (`unite_id`) REFERENCES `p_unites` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_articles_unite_secondaire` FOREIGN KEY (`unite_secondaire_id`) REFERENCES `p_unites` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `d_documents`
--
ALTER TABLE `d_documents`
  ADD CONSTRAINT `fk_documents_adresse_livraison` FOREIGN KEY (`adresse_livraison_id`) REFERENCES `d_adresses_livraison` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_documents_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_documents_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_documents_origine` FOREIGN KEY (`document_origine_id`) REFERENCES `d_documents` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_documents_statut` FOREIGN KEY (`statut_document_id`) REFERENCES `p_statuts_documents` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_documents_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_documents_tier` FOREIGN KEY (`tier_id`) REFERENCES `d_tiers` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_documents_type` FOREIGN KEY (`type_document_id`) REFERENCES `p_types_documents` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_documents_utilisateur` FOREIGN KEY (`utilisateur_id`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_documents_vendeur` FOREIGN KEY (`vendeur_id`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `d_document_lignes`
--
ALTER TABLE `d_document_lignes`
  ADD CONSTRAINT `fk_lignes_article` FOREIGN KEY (`article_id`) REFERENCES `d_articles` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lignes_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lignes_depot` FOREIGN KEY (`depot_id`) REFERENCES `p_depots` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lignes_document` FOREIGN KEY (`document_id`) REFERENCES `d_documents` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lignes_document_source` FOREIGN KEY (`document_source_id`) REFERENCES `d_documents` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lignes_ligne_source` FOREIGN KEY (`ligne_source_id`) REFERENCES `d_document_lignes` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lignes_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lignes_projet` FOREIGN KEY (`projet_id`) REFERENCES `d_projets` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lignes_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lignes_tva` FOREIGN KEY (`tva_id`) REFERENCES `p_tvas` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lignes_unite` FOREIGN KEY (`unite_id`) REFERENCES `p_unites` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `d_document_reglements`
--
ALTER TABLE `d_document_reglements`
  ADD CONSTRAINT `fk_document_reglements_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_document_reglements_document` FOREIGN KEY (`document_id`) REFERENCES `d_documents` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_document_reglements_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_document_reglements_reglement` FOREIGN KEY (`reglement_id`) REFERENCES `d_reglements` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_document_reglements_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_document_reglements_utilisateur` FOREIGN KEY (`utilisateur_id`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `d_familles`
--
ALTER TABLE `d_familles`
  ADD CONSTRAINT `fk_familles_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_familles_depot` FOREIGN KEY (`depot_id`) REFERENCES `p_depots` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_familles_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_familles_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_familles_tva` FOREIGN KEY (`tva_id`) REFERENCES `p_tvas` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_familles_unite` FOREIGN KEY (`unite_id`) REFERENCES `p_unites` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `d_lots_sn`
--
ALTER TABLE `d_lots_sn`
  ADD CONSTRAINT `fk_lots_article` FOREIGN KEY (`article_id`) REFERENCES `d_articles` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lots_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lots_depot` FOREIGN KEY (`depot_id`) REFERENCES `p_depots` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lots_document_entree` FOREIGN KEY (`document_entree_id`) REFERENCES `d_documents` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lots_fournisseur` FOREIGN KEY (`fournisseur_id`) REFERENCES `d_tiers` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lots_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lots_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `d_mouvements_stock`
--
ALTER TABLE `d_mouvements_stock`
  ADD CONSTRAINT `fk_mouvements_article` FOREIGN KEY (`article_id`) REFERENCES `d_articles` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_mouvements_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_mouvements_depot` FOREIGN KEY (`depot_id`) REFERENCES `p_depots` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_mouvements_document` FOREIGN KEY (`document_id`) REFERENCES `d_documents` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_mouvements_document_ligne` FOREIGN KEY (`document_ligne_id`) REFERENCES `d_document_lignes` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_mouvements_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_mouvements_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `d_projets`
--
ALTER TABLE `d_projets`
  ADD CONSTRAINT `fk_projets_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_projets_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_projets_responsable` FOREIGN KEY (`utilisateur_id`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_projets_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_projets_tier` FOREIGN KEY (`tier_id`) REFERENCES `d_tiers` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `d_reglements`
--
ALTER TABLE `d_reglements`
  ADD CONSTRAINT `fk_reglements_caisse` FOREIGN KEY (`caisse_id`) REFERENCES `p_caisses` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_reglements_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_reglements_devise` FOREIGN KEY (`devise_id`) REFERENCES `p_devises` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_reglements_mode` FOREIGN KEY (`mode_reglement_id`) REFERENCES `p_modes_reglement` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_reglements_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_reglements_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_reglements_tier` FOREIGN KEY (`tier_id`) REFERENCES `d_tiers` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_reglements_utilisateur` FOREIGN KEY (`utilisateur_id`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `d_stock`
--
ALTER TABLE `d_stock`
  ADD CONSTRAINT `fk_stock_article` FOREIGN KEY (`article_id`) REFERENCES `d_articles` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_stock_depot` FOREIGN KEY (`depot_id`) REFERENCES `p_depots` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Constraints for table `d_tiers`
--
ALTER TABLE `d_tiers`
  ADD CONSTRAINT `fk_tiers_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_tiers_devise` FOREIGN KEY (`devise_id`) REFERENCES `p_devises` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_tiers_mode_paiement` FOREIGN KEY (`mode_paiement_id`) REFERENCES `p_modes_reglement` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_tiers_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_tiers_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_tiers_tva` FOREIGN KEY (`tva_id`) REFERENCES `p_tvas` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `d_utilisateur_depots`
--
ALTER TABLE `d_utilisateur_depots`
  ADD CONSTRAINT `fk_utilisateur_depots_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_utilisateur_depots_depot` FOREIGN KEY (`depot_id`) REFERENCES `p_depots` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_utilisateur_depots_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_utilisateur_depots_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_utilisateur_depots_utilisateur` FOREIGN KEY (`utilisateur_id`) REFERENCES `p_utilisateurs` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `journaux_audit`
--
ALTER TABLE `journaux_audit`
  ADD CONSTRAINT `fk_journaux_audit_utilisateur` FOREIGN KEY (`utilisateur_id`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `p_caisses`
--
ALTER TABLE `p_caisses`
  ADD CONSTRAINT `fk_caisses_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_caisses_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_caisses_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `p_depots`
--
ALTER TABLE `p_depots`
  ADD CONSTRAINT `fk_depots_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_depots_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_depots_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `p_devises`
--
ALTER TABLE `p_devises`
  ADD CONSTRAINT `fk_devises_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_devises_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_devises_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `p_informations_societe`
--
ALTER TABLE `p_informations_societe`
  ADD CONSTRAINT `fk_infos_societe_devise` FOREIGN KEY (`devise_id`) REFERENCES `p_devises` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_infos_societe_tva` FOREIGN KEY (`tva_id`) REFERENCES `p_tvas` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `p_modes_reglement`
--
ALTER TABLE `p_modes_reglement`
  ADD CONSTRAINT `fk_modes_reglement_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_modes_reglement_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_modes_reglement_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `p_numerotation_documents`
--
ALTER TABLE `p_numerotation_documents`
  ADD CONSTRAINT `fk_numerotation_type_document` FOREIGN KEY (`type_document_id`) REFERENCES `p_types_documents` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `p_role_permissions`
--
ALTER TABLE `p_role_permissions`
  ADD CONSTRAINT `fk_role_permissions_permission` FOREIGN KEY (`permission_id`) REFERENCES `p_permissions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_role_permissions_role` FOREIGN KEY (`role_id`) REFERENCES `p_roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `p_statuts_documents`
--
ALTER TABLE `p_statuts_documents`
  ADD CONSTRAINT `fk_statuts_documents_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_statuts_documents_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_statuts_documents_type` FOREIGN KEY (`type_document_id`) REFERENCES `p_types_documents` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `p_tvas`
--
ALTER TABLE `p_tvas`
  ADD CONSTRAINT `fk_tvas_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_tvas_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_tvas_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `p_unites`
--
ALTER TABLE `p_unites`
  ADD CONSTRAINT `fk_unites_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_unites_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_unites_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `p_users_roles`
--
ALTER TABLE `p_users_roles`
  ADD CONSTRAINT `fk_users_roles_role` FOREIGN KEY (`role_id`) REFERENCES `p_roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_users_roles_user` FOREIGN KEY (`user_id`) REFERENCES `p_utilisateurs` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `p_utilisateurs`
--
ALTER TABLE `p_utilisateurs`
  ADD CONSTRAINT `fk_utilisateurs_createur` FOREIGN KEY (`cree_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_utilisateurs_modificateur` FOREIGN KEY (`modifie_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_utilisateurs_supprimeur` FOREIGN KEY (`supprime_par`) REFERENCES `p_utilisateurs` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
