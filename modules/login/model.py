from services.sql.db_connection import with_cursor
import bcrypt
import mysql.connector
import os
import dotenv
import logging

logger = logging.getLogger("app")


class LoginModel:
    @with_cursor()
    def get_societes(self, cursor):
        query = "SELECT id, code_societe FROM societes_connexions WHERE actif = 1"
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            logger.warning("No active societes found in the database.")
            return []
        if not self.check_database_connection(result[0][1]):
            logger.error(f"Failed to connect to database for code_societe: {result[0][1]}")
        return [row[1] for row in result]

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
        print(1, os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))
        cursor = connection.cursor()
        ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
        query = f"""
        SELECT
        `db_host`,
        `db_port`,
        `db_name`,
        `db_user`,
        CAST(AES_DECRYPT(`db_password_encrypted`, '{ENCRYPTION_KEY}') AS CHAR) AS `db_password_encrypted`,
        `db_charset`,
        `db_collation`
        FROM `societes_connexions` WHERE `code_societe` = '{code_societe}' LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        if row:
            db_host, db_port, db_name, db_user, db_password_encrypted, db_charset, db_collation = row
        else:
            logger.error(f"No database configuration found for code_societe: {code_societe}")
            raise ValueError(f"No database configuration found for code_societe: {code_societe}")
        try:
            connection = mysql.connector.connect(
                        host=db_host,
                        port=int(db_port),
                        user=db_user,
                        password=db_password_encrypted,
                        database=db_name,
                        charset=db_charset,
                        collation=db_collation,
                    )
            connection.close()
            os.environ["DB_HOST"] = db_host
            os.environ["DB_PORT"] = str(db_port)
            os.environ["DB_NAME"] = db_name
            os.environ["DB_USER"] = db_user
            os.environ["DB_PASSWORD"] = db_password_encrypted
            os.environ["DB_CHARSET"] = db_charset
            os.environ["DB_COLLATION"] = db_collation
            print(2, os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))
        except Exception:
            logger.error(f"Database connection failed for {code_societe}")
            return False
        return True


    @with_cursor()
    def authenticate_user(self, username, password, cursor):

        if not username or not password:
            return False

        query = f"""
            SELECT mot_de_passe_hash FROM P_utilisateurs
            WHERE nom_utilisateur = '{username}'
            LIMIT 1
        """
        cursor.execute(query)
        pwd_hash = cursor.fetchone()[0]

        if pwd_hash is None:
            return False

        query = f"""
            SELECT id FROM P_utilisateurs
            WHERE nom_utilisateur = '{username}'
        """
        cursor.execute(query)
        user_id = cursor.fetchone()

        pwd_hash = pwd_hash.encode()

        return bcrypt.checkpw(password.encode(), pwd_hash)

 