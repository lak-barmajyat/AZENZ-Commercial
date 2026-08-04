-- Demo connections for azenz_master
-- Test-only encryption key: azenz-local-test-key
-- The application must use the same key with AES_DECRYPT to recover the password.

SET NAMES utf8mb4;
START TRANSACTION;

INSERT INTO `societes_connexions`
(`code_societe`, `nom_societe`, `description`, `db_host`, `db_port`, `db_name`,
 `db_user`, `db_password_encrypted`, `db_charset`, `db_collation`, `ssl_active`,
 `connection_timeout`, `actif`, `est_defaut`, `ordre_affichage`)
VALUES
('SOC001', 'Atlas Digital Solutions', 'Commercial test company in Casablanca', 'localhost', 3306,
 'azenz_commercial_1', 'azenz', AES_ENCRYPT('12345678', 'azenz-local-test-key'),
 'utf8mb4', 'utf8mb4_general_ci', 0, 10, 1, 1, 1),
('SOC002', 'Rif Business Services', 'Commercial test company in Tangier', 'localhost', 3306,
 'azenz_commercial_2', 'azenz', AES_ENCRYPT('12345678', 'azenz-local-test-key'),
 'utf8mb4', 'utf8mb4_general_ci', 0, 10, 1, 0, 2),
('SOC003', 'Sahara Office Distribution', 'Commercial test company in Marrakech', 'localhost', 3306,
 'azenz_commercial_3', 'azenz', AES_ENCRYPT('12345678', 'azenz-local-test-key'),
 'utf8mb4', 'utf8mb4_general_ci', 0, 10, 1, 0, 3),
('SOC004', 'Andalus Technology Group', 'Commercial test company in Rabat', 'localhost', 3306,
 'azenz_commercial_4', 'azenz', AES_ENCRYPT('12345678', 'azenz-local-test-key'),
 'utf8mb4', 'utf8mb4_general_ci', 0, 10, 1, 0, 4);

COMMIT;
