-- Required schema for azenz_master
-- The Python installer creates and selects the database before running this file.

SET NAMES utf8mb4;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';
START TRANSACTION;

CREATE TABLE `societes_connexions` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `code_societe` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_societe` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `db_host` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `db_port` int(10) UNSIGNED NOT NULL DEFAULT 3306,
  `db_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `db_user` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `db_password_encrypted` varbinary(255) DEFAULT NULL,
  `db_charset` varchar(50) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'utf8mb4',
  `db_collation` varchar(100) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'utf8mb4_general_ci',
  `ssl_active` tinyint(1) NOT NULL DEFAULT 0,
  `ssl_ca_path` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `connection_timeout` int(10) UNSIGNED NOT NULL DEFAULT 10,
  `logo_url` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `actif` tinyint(1) NOT NULL DEFAULT 1,
  `est_defaut` tinyint(1) NOT NULL DEFAULT 0,
  `ordre_affichage` int(11) NOT NULL DEFAULT 0,
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT 0,
  `date_suppression` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_societe_code` (`code_societe`),
  UNIQUE KEY `uq_societe_database` (`db_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

COMMIT;
