import psycopg2
from psycopg2 import extensions


class DatabaseConnection:
    def __init__(self, dsn):
        self.dsn = dsn
        self.conn = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(**self.dsn)
            self.conn.autocommit = True
            return self.conn
        except psycopg2.OperationalError as e:
            raise Exception(f"Nie można nawiązać połączenia z bazą danych: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


def connect():
    settings = {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'Citro123456ok',
        'database': 'my_db'
    }
    return DatabaseConnection(settings)
