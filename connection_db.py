import psycopg2


class DatabaseConnection:
    def __init__(self, dsn):
        """
        Initialize a new database connection instance.

        :param dsn: A dictionary containing connection parameters.

        Inicjalizuje nową instancję połączenia z bazą danych.

        :param dsn: Słownik zawierający parametry połączenia.
        """
        self.dsn = dsn  # Data Source Name - szczegóły połączenia
        self.conn = None  # Przechowuje połączenie z bazą danych

    def __enter__(self):
        """
        Establish the database connection.

        :return: The connection object.
        :raises Exception: If connection cannot be established.

        Nawiązuje połączenie z bazą danych.

        :return: Obiekt połączenia.
        :raises Exception: Jeśli nie można nawiązać połączenia.
        """
        try:
            self.conn = psycopg2.connect(**self.dsn)  # Użyj parametrów z dsn do nawiązania połączenia
            self.conn.autocommit = True  # Ustaw tryb autocommit dla połączenia
            return self.conn  # Zwróć obiekt połączenia
        except psycopg2.OperationalError as e:
            raise Exception(f"Nie można nawiązać połączenia z bazą danych: {e}")  # Wyjątek gdy połączenie nieudane

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the database connection on exit.

        :param exc_type: The exception type.
        :param exc_val: The exception value.
        :param exc_tb: The traceback object.

        Zamyka połączenie z bazą danych przy wyjściu.

        :param exc_type: Typ wyjątku.
        :param exc_val: Wartość wyjątku.
        :param exc_tb: Obiekt traceback.
        """
        if self.conn:
            self.conn.close()  # Zamknij połączenie jeśli istnieje


def connect():
    """
    Connect to the database using predefined settings.

    :return: An instance of DatabaseConnection.

    Łączy się z bazą danych używając predefiniowanych ustawień.

    :return: Instancja DatabaseConnection.
    """
    settings = {
        'host': 'localhost',  # Adres hosta
        'user': 'postgres',  # Nazwa użytkownika
        'password': 'Citro123456ok',  # Hasło
        'database': 'my_db'  # Nazwa bazy danych
    }
    return DatabaseConnection(settings)  # Zwróć nową instancję DatabaseConnection
