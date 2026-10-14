import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def create_connection():
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME")
    port = int(os.getenv("DB_PORT", "3306"))

    if not host or not user or not database:
        raise ValueError("Set DB_HOST, DB_USER, and DB_NAME in the .env file.")

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )


if __name__ == "__main__":
    connection = None

    try:
        connection = create_connection()
    except (mysql.connector.Error, ValueError) as error:
        print(f"Database connection failed: {error}")
    else:
        print("Database connection successful.")
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("Database connection closed.")