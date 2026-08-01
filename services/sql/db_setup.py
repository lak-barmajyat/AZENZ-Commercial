from __future__ import annotations

import argparse
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
SQL_DIR = ROOT_DIR / "services" / "sql"
MASTER_DB = "azenz_master"
APP_DB = "azenz_commercial"


def mysql_config(database: str | None = None) -> dict:
    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "charset": os.getenv("DB_CHARSET", "utf8mb4"),
        "collation": os.getenv("DB_COLLATION", "utf8mb4_general_ci"),
    }
    if database:
        config["database"] = database
    return config


def split_sql(script: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    quote: str | None = None
    escape = False
    line_comment = False
    block_comment = False
    i = 0

    while i < len(script):
        char = script[i]
        next_char = script[i + 1] if i + 1 < len(script) else ""

        if line_comment:
            if char == "\n":
                line_comment = False
            i += 1
            continue

        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                i += 2
            else:
                i += 1
            continue

        if quote is None:
            if char == "-" and next_char == "-":
                line_comment = True
                i += 2
                continue
            if char == "#":
                line_comment = True
                i += 1
                continue
            if char == "/" and next_char == "*":
                block_comment = True
                i += 2
                continue
            if char in ("'", '"', "`"):
                quote = char
                current.append(char)
                i += 1
                continue
            if char == ";":
                statement = "".join(current).strip()
                if statement:
                    statements.append(statement)
                current = []
                i += 1
                continue
        else:
            current.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = None
            i += 1
            continue

        current.append(char)
        i += 1

    statement = "".join(current).strip()
    if statement:
        statements.append(statement)
    return statements


def execute_sql_file(cursor, path: Path) -> None:
    print(f"Importing {path.relative_to(ROOT_DIR)}")
    script = path.read_text(encoding="utf-8-sig")
    for statement in split_sql(script):
        cursor.execute(statement)


def database_exists(cursor, database: str) -> bool:
    cursor.execute(
        "SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = ?",
        (database,),
    )
    return cursor.fetchone()[0] > 0


def configure_master_connection(cursor) -> None:
    encryption_key = os.getenv("ENCRYPTION_KEY")
    if not encryption_key:
        raise RuntimeError("ENCRYPTION_KEY is required in .env")

    cursor.execute(f"USE `{MASTER_DB}`")
    params = (
        "SOC001",
        "Lak Software",
        os.getenv("DB_HOST", "localhost"),
        int(os.getenv("DB_PORT", "3306")),
        APP_DB,
        os.getenv("DB_USER", "root"),
        os.getenv("DB_PASSWORD", ""),
        encryption_key,
        os.getenv("DB_CHARSET", "utf8mb4"),
        os.getenv("DB_COLLATION", "utf8mb4_general_ci"),
    )
    cursor.execute(
        """
        INSERT INTO societes_connexions (
            code_societe,
            nom_societe,
            db_host,
            db_port,
            db_name,
            db_user,
            db_password_encrypted,
            db_charset,
            db_collation,
            actif
        ) VALUES (%s, %s, %s, %s, %s, %s, AES_ENCRYPT(%s, %s), %s, %s, 1)
        ON DUPLICATE KEY UPDATE
            nom_societe = VALUES(nom_societe),
            db_host = VALUES(db_host),
            db_port = VALUES(db_port),
            db_name = VALUES(db_name),
            db_user = VALUES(db_user),
            db_password_encrypted = VALUES(db_password_encrypted),
            db_charset = VALUES(db_charset),
            db_collation = VALUES(db_collation),
            actif = 1
        """,
        params,
    )


def verify(cursor) -> None:
    checks = {
        MASTER_DB: ["societes_connexions"],
        APP_DB: [
            "p_utilisateurs",
            "d_documents",
            "p_types_documents",
            "p_numerotation_documents",
        ],
    }
    for database, tables in checks.items():
        cursor.execute(f"USE `{database}`")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            cursor.fetchone()

    cursor.execute(f"USE `{MASTER_DB}`")
    cursor.execute(
        """
        SELECT CAST(AES_DECRYPT(db_password_encrypted, %s) AS CHAR)
        FROM societes_connexions
        WHERE code_societe = 'SOC001'
        """,
        (os.getenv("ENCRYPTION_KEY"),),
    )
    decrypted_password = cursor.fetchone()[0]
    if decrypted_password != os.getenv("DB_PASSWORD", ""):
        raise RuntimeError("Master company DB password encryption verification failed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Set up local AZENZ MySQL databases.")
    parser.add_argument("--seed", action="store_true", help="Import demo seed data.")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate local databases first.")
    args = parser.parse_args()

    load_dotenv(ROOT_DIR / ".env", override=True)

    connection = mysql.connector.connect(**mysql_config())
    cursor = connection.cursor()
    try:
        if args.reset:
            cursor.execute(f"DROP DATABASE IF EXISTS `{APP_DB}`")
            cursor.execute(f"DROP DATABASE IF EXISTS `{MASTER_DB}`")

        if database_exists(cursor, MASTER_DB):
            print(f"Database {MASTER_DB} already exists; reusing it")
        else:
            execute_sql_file(cursor, SQL_DIR / "azenz_master.sql")

        if database_exists(cursor, APP_DB):
            print(f"Database {APP_DB} already exists; reusing it")
        else:
            execute_sql_file(cursor, SQL_DIR / "azenz_commercial.sql")
        if args.seed:
            cursor.execute(f"USE `{APP_DB}`")
            execute_sql_file(cursor, SQL_DIR / "azenz_commercial_seed_full.sql")

        configure_master_connection(cursor)
        verify(cursor)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

    print("Database setup completed successfully.")


if __name__ == "__main__":
    main()
