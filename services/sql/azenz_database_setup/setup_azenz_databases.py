from __future__ import annotations

import getpass
from pathlib import Path
from typing import Iterable

try:
    import pymysql
except ImportError:
    print("Missing dependency: PyMySQL")
    print("Install it with: python -m pip install pymysql")
    raise SystemExit(1)

HOST = "localhost"
PORT = 3306
ADMIN_USER = "root"
APP_USER = "azenz"
APP_PASSWORD = "12345678"
MASTER_DATABASE = "azenz_master"
COMMERCIAL_DATABASES = [f"azenz_commercial_{number}" for number in range(1, 5)]

BASE_DIR = Path(__file__).resolve().parent
MASTER_SCHEMA = BASE_DIR / "azenz_master.sql"
MASTER_DEMO = BASE_DIR / "azenz_master_demo.sql"
COMMERCIAL_SCHEMA = BASE_DIR / "azenz_commercial.sql"
COMMERCIAL_DEMO = BASE_DIR / "azenz_commercial_demo.sql"


def ask_yes_no(message: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        answer = input(f"{message} {suffix}: ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer y or n.")


def split_sql_statements(sql: str) -> Iterable[str]:
    """Split ordinary MySQL dump statements without breaking quoted strings."""
    buffer: list[str] = []
    quote: str | None = None
    escaped = False
    line_comment = False
    block_comment = False
    index = 0

    while index < len(sql):
        char = sql[index]
        next_char = sql[index + 1] if index + 1 < len(sql) else ""

        if line_comment:
            if char == "\n":
                line_comment = False
                buffer.append(char)
            index += 1
            continue

        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
            else:
                index += 1
            continue

        if quote is not None:
            buffer.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                # SQL escapes a quote by doubling it: '' or "".
                if next_char == quote:
                    buffer.append(next_char)
                    index += 1
                else:
                    quote = None
            index += 1
            continue

        if char in {"'", '"', "`"}:
            quote = char
            buffer.append(char)
            index += 1
            continue

        if char == "#":
            line_comment = True
            index += 1
            continue

        if char == "-" and next_char == "-":
            after = sql[index + 2] if index + 2 < len(sql) else " "
            if after.isspace():
                line_comment = True
                index += 2
                continue

        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue

        if char == ";":
            statement = "".join(buffer).strip()
            if statement:
                yield statement
            buffer.clear()
        else:
            buffer.append(char)
        index += 1

    statement = "".join(buffer).strip()
    if statement:
        yield statement


def run_sql_file(connection, path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")

    sql = path.read_text(encoding="utf-8-sig")
    statements = list(split_sql_statements(sql))
    with connection.cursor() as cursor:
        for number, statement in enumerate(statements, start=1):
            try:
                cursor.execute(statement)
            except Exception as exc:
                preview = " ".join(statement.split())[:180]
                raise RuntimeError(
                    f"Failed in {path.name}, statement {number}: {preview}"
                ) from exc
    connection.commit()


def recreate_database(connection, database_name: str) -> None:
    # Names are hardcoded constants, never raw user input.
    with connection.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS `{database_name}`")
        cursor.execute(
            f"CREATE DATABASE `{database_name}` "
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
        )
    connection.commit()


def select_database(connection, database_name: str) -> None:
    connection.select_db(database_name)


def ensure_application_user(connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"CREATE USER IF NOT EXISTS '{APP_USER}'@'localhost' "
            f"IDENTIFIED BY '{APP_PASSWORD}'"
        )
        # Always restore the hardcoded test password, even when the account existed.
        cursor.execute(
            f"ALTER USER '{APP_USER}'@'localhost' IDENTIFIED BY '{APP_PASSWORD}'"
        )
    connection.commit()


def grant_application_user(connection, databases: list[str]) -> None:
    with connection.cursor() as cursor:
        for database in databases:
            cursor.execute(
                f"GRANT ALL PRIVILEGES ON `{database}`.* "
                f"TO '{APP_USER}'@'localhost'"
            )
        cursor.execute("FLUSH PRIVILEGES")
    connection.commit()


def test_application_connection(database_name: str) -> None:
    connection = pymysql.connect(
        host=HOST,
        port=PORT,
        user=APP_USER,
        password=APP_PASSWORD,
        database=database_name,
        charset="utf8mb4",
        autocommit=True,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            selected = cursor.fetchone()[0]
            if selected != database_name:
                raise RuntimeError(f"Connected to unexpected database: {selected}")
    finally:
        connection.close()


def main() -> int:
    print("=" * 62)
    print("Azenz local database setup")
    print("This destroys and recreates every selected Azenz database.")
    print("=" * 62)

    admin_password = getpass.getpass("MySQL root password (press Enter if empty): ")
    create_commercial = ask_yes_no(
        "Create the four commercial databases?", default=True
    )
    try:
        connection = pymysql.connect(
            host=HOST,
            port=PORT,
            user=ADMIN_USER,
            password=admin_password,
            charset="utf8mb4",
            autocommit=False,
        )
    except Exception as exc:
        print(f"Could not connect to MySQL as {ADMIN_USER}: {exc}")
        return 1

    created_databases = [MASTER_DATABASE]
    if create_commercial:
        created_databases.extend(COMMERCIAL_DATABASES)

    try:
        print(f"\nCreating or updating MySQL user {APP_USER}...")
        ensure_application_user(connection)

        print(f"Recreating {MASTER_DATABASE}...")
        recreate_database(connection, MASTER_DATABASE)
        select_database(connection, MASTER_DATABASE)
        run_sql_file(connection, MASTER_SCHEMA)

        if create_commercial:
            for database in COMMERCIAL_DATABASES:
                print(f"Recreating {database}...")
                recreate_database(connection, database)
                select_database(connection, database)
                run_sql_file(connection, COMMERCIAL_SCHEMA)
                run_sql_file(connection, COMMERCIAL_DEMO)

            select_database(connection, MASTER_DATABASE)
            run_sql_file(connection, MASTER_DEMO)

        grant_application_user(connection, created_databases)

    except Exception as exc:
        connection.rollback()
        print(f"\nSetup failed: {exc}")
        cause = exc.__cause__
        if cause is not None:
            print(f"MySQL error: {cause}")
        return 1
    finally:
        connection.close()

    print("\nTesting the azenz MySQL account...")
    try:
        for database in created_databases:
            test_application_connection(database)
            print(f"  OK: {database}")
    except Exception as exc:
        print(f"Connection test failed: {exc}")
        return 1

    print("\nSetup completed successfully.")
    print(f"MySQL application user: {APP_USER}")
    print(f"MySQL/application test password: {APP_PASSWORD}")
    print("Application login: admin / 12345678")
    if create_commercial:
        print("Commercial databases:")
        for database in COMMERCIAL_DATABASES:
            print(f"  - {database}")
    else:
        print("Commercial databases were not created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
