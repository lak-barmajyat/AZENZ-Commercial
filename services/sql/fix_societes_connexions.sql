CREATE TABLE IF NOT EXISTS `societes_connexions` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `code_societe` varchar(100) NOT NULL,
  `db_host` varchar(255) NOT NULL DEFAULT 'localhost',
  `db_port` int(11) NOT NULL DEFAULT 3306,
  `db_name` varchar(255) NOT NULL,
  `db_user` varchar(255) NOT NULL,
  `db_password_encrypted` varbinary(500) DEFAULT NULL,
  `db_charset` varchar(50) NOT NULL DEFAULT 'utf8mb4',
  `db_collation` varchar(50) NOT NULL DEFAULT 'utf8mb4_general_ci',
  `actif` tinyint(1) NOT NULL DEFAULT 1,
  `date_creation` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_societe` (`code_societe`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

SET @encryption_key = '4f61b7e2c9a3d5f8e10b24c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6';
SET @password = '12345678';

INSERT IGNORE INTO `societes_connexions` (`code_societe`, `db_host`, `db_port`, `db_name`, `db_user`, `db_password_encrypted`, `db_charset`, `db_collation`, `actif`)
VALUES (
  'AZENZ',
  'localhost',
  3306,
  'azenz_commercial',
  'moss',
  AES_ENCRYPT(@password, @encryption_key),
  'utf8mb4',
  'utf8mb4_general_ci',
  1
);
