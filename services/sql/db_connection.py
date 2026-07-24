from functools import wraps
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def with_cursor(dictionary=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                charset=os.getenv("DB_CHARSET"),
                collation=os.getenv("DB_COLLATION"),
            )

            cursor = connection.cursor(dictionary=dictionary)

            try:
                result = func(*args, **kwargs, cursor=cursor)
                connection.commit()
                return result

            except Exception:
                connection.rollback()
                raise

            finally:
                cursor.close()
                connection.close()

        return wrapper
    return decorator
