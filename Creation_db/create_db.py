import psycopg2
from psycopg2 import OperationalError, errors


"""Configuration data"""""
settings = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'Citro123456ok',
    'dbname': 'postgres'  # Default database for creating a new database   /DLA KOLEJNYCH SKRYPTÓW PAMIĘTAJ!
}

target_db_name = 'my_db'

"""Function to create database if it doesn't exist"""


def create_database(settings, db_name):
    config_settings = settings.copy()
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(**config_settings)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Baza danych {db_name} została stworzona.")
    except errors.DuplicateDatabase:
        print(f"Baza danych {db_name} już istnieje.")
    except OperationalError as e:
        print(f"Błąd połączenia: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


""""Function to create tables"""


def create_tables(settings, db_name):
    settings = settings.copy()
    settings['dbname'] = db_name  # Switching to the newly created database
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(**settings)
        connection.autocommit = True
        cursor = connection.cursor()

        """# Create a user table"""
        try:
            cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE,
                    hashed_password VARCHAR(80)
                );
            """)
            print("Tabela 'users' została stworzona.")
        except errors.DuplicateTable:
            print("Tabela 'users' już istnieje.")

        """"Creating a message table"""
        try:
            cursor.execute("""
                CREATE TABLE messages (
                    id SERIAL PRIMARY KEY,
                    from_id INTEGER REFERENCES users(id),
                    to_id INTEGER REFERENCES users(id),
                    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                    text VARCHAR(255)
                );
            """)
            """creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  --JEżeli przy wstawianiu rekordu nie zostanie 
            podana wartość dla tej kolumny, automatycznie zostanie użyta bieżąca data i godzina"""
            print("Tabela 'messages' została stworzona.")
        except errors.DuplicateTable:
            print("Tabela 'messages' już istnieje.")

    except OperationalError as e:
        print(f"Błąd połączenia z bazą danych {db_name}: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


"""Calling functions that create a database and tablesCalling functions that create a database and tables"""
create_database(settings, target_db_name)
create_tables(settings, target_db_name)
