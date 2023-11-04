import psycopg2
from psycopg2 import OperationalError, errors
import random


# Функция-заглушка для хеширования пароля
def dummy_hash_password(password):
    # Здесь будет ваш код хеширования
    return "hashed_" + password


# Dane konfiguracyjne___________________________________________________________________________________________________
settings = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'Citro123456ok',
    'dbname': 'postgres'  # Baza danych domyślna do tworzenia nowej bazy    DLA KOLEJNYCH SKRYPTÓW PAMIĘTAJ!
}
target_db_name = 'my_db'


# Функция для вставки тестовых данных
def insert_test_data(settings, db_name, hash_function, num_records=30):
    settings = settings.copy()
    settings['dbname'] = db_name
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(**settings)
        connection.autocommit = True
        cursor = connection.cursor()

        # Вставляем тестовых пользователей
        for i in range(num_records):
            username = f'user{i}'
            password = f'password{i}'
            hashed_password = hash_function(password)  # Используем переданную функцию хеширования
            cursor.execute("""
                INSERT INTO users(username, hashed_password)
                VALUES(%s, %s);
            """, (username, hashed_password))

        # Вставляем тестовые сообщения
        for i in range(num_records):
            from_id = random.randint(1, num_records)
            to_id = random.randint(1, num_records)
            text = f'message text {i}'
            cursor.execute("""
                INSERT INTO messages(from_id, to_id, text)
                VALUES(%s, %s, %s);
            """, (from_id, to_id, text))

        print(f"Wstawiono {num_records} użytkowników i {num_records} wiadomości do bazy danych.")

    except OperationalError as e:
        print(f"Błąd połączenia z bazą danych {db_name}: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Wywołanie функции wstawiającej testowe dane с заглушкой функции хеширования__________________________________________
insert_test_data(settings, target_db_name, dummy_hash_password)
