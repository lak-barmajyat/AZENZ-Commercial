import os

import bcrypt
import dotenv
import mysql.connector

from services.sql.db_connection import with_cursor


class LoginModel:
    @with_cursor()
    def get_societes(self, cursor):
        query = """
            SELECT code_societe
            FROM societes_connexions
            WHERE actif = 1
        """
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]

    def check_database_connection(self, code_societe):
        dotenv.load_dotenv(".env", override=True)

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset=os.getenv("DB_CHARSET"),
            collation=os.getenv("DB_COLLATION"),
        )

        cursor = connection.cursor()
        encryption_key = os.getenv("ENCRYPTION_KEY")

        query = """
            SELECT
                db_host,
                db_port,
                db_name,
                db_user,
                CAST(
                    AES_DECRYPT(db_password_encrypted, %s)
                    AS CHAR
                ),
                db_charset,
                db_collation
            FROM societes_connexions
            WHERE code_societe = %s
            LIMIT 1
        """

        try:
            cursor.execute(query, (encryption_key, code_societe))
            row = cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

        if row is None:
            raise ValueError(
                f"No database configuration found for code_societe: "
                f"{code_societe}"
            )

        (
            db_host,
            db_port,
            db_name,
            db_user,
            db_password,
            db_charset,
            db_collation,
        ) = row

        if isinstance(db_password, bytes):
            db_password = db_password.decode()

        try:
            connection = mysql.connector.connect(
                host=db_host,
                port=int(db_port),
                user=db_user,
                password=db_password,
                database=db_name,
                charset=db_charset,
                collation=db_collation,
            )
            connection.close()
        except mysql.connector.Error:
            return False

        os.environ["DB_HOST"] = db_host
        os.environ["DB_PORT"] = str(db_port)
        os.environ["DB_NAME"] = db_name
        os.environ["DB_USER"] = db_user
        os.environ["DB_PASSWORD"] = db_password
        os.environ["DB_CHARSET"] = db_charset
        os.environ["DB_COLLATION"] = db_collation

        return True

    @with_cursor()
    def authenticate_user(self, username, password, cursor):
        if not username or not password:
            return False

        query = """
            SELECT mot_de_passe_hash
            FROM p_utilisateurs
            WHERE LOWER(nom_utilisateur) = LOWER(%s)
            LIMIT 1
        """
        cursor.execute(query, (username,))
        row = cursor.fetchone()

        if row is None:
            return False

        password_hash = row[0]
        if isinstance(password_hash, str):
            password_hash = password_hash.encode()

        return bcrypt.checkpw(password.encode(), password_hash)