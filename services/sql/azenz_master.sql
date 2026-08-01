-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 31, 2026 at 05:17 AM
-- Server version: 8.0.17
-- PHP Version: 7.3.10

CREATE DATABASE azenz_master DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE azenz_master;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `azenz_master`
--

-- --------------------------------------------------------

--
-- Table structure for table `societes_connexions`
--

CREATE TABLE `societes_connexions` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `code_societe` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_societe` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `db_host` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `db_port` int(10) UNSIGNED NOT NULL DEFAULT '3306',
  `db_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `db_user` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `db_password_encrypted` varbinary(255) DEFAULT NULL,
  `db_charset` varchar(50) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'utf8mb4',
  `db_collation` varchar(100) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'utf8mb4_general_ci',
  `ssl_active` tinyint(1) NOT NULL DEFAULT '0',
  `ssl_ca_path` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `connection_timeout` int(10) UNSIGNED NOT NULL DEFAULT '10',
  `logo_url` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  `est_defaut` tinyint(1) NOT NULL DEFAULT '0',
  `ordre_affichage` int(11) NOT NULL DEFAULT '0',
  `date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_modification` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `supprime` tinyint(1) NOT NULL DEFAULT '0',
  `date_suppression` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `societes_connexions`
--

INSERT INTO `societes_connexions` (`id`, `code_societe`, `nom_societe`, `description`, `db_host`, `db_port`, `db_name`, `db_user`, `db_password_encrypted`, `db_charset`, `db_collation`, `ssl_active`, `ssl_ca_path`, `connection_timeout`, `logo_url`, `actif`, `est_defaut`, `ordre_affichage`, `date_creation`, `date_modification`, `supprime`, `date_suppression`) VALUES
(1, 'SOC001', 'Lak Software', NULL, 'localhost', 3306, 'azenz_commercial', 'root', 0x5c86a761143cc92c93ee82160645399a, 'utf8mb4', 'utf8mb4_general_ci', 0, NULL, 10, NULL, 1, 0, 0, '2026-05-29 10:29:34', '2026-05-31 04:45:55', 0, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `societes_connexions`
--
ALTER TABLE `societes_connexions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code_societe` (`code_societe`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `societes_connexions`
--
ALTER TABLE `societes_connexions`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
