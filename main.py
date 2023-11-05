from connection_db import connect
from models import User, Message


def main_menu():
    """
        Wyświetla główne menu aplikacji.
        Displays the main menu of the application.
        """
    print("1. Zarządzaj użytkownikami")
    print("2. Zarządzaj wiadomościami")
    print("0. Wyjście")

    choice = input("Wybierz opcję: ")
    if choice == "1":
        manage_users()
    elif choice == "2":
        manage_messages()
    elif choice == "0":
        exit()
    else:
        print("Nieprawidłowa opcja!")


def manage_users():
    """
        Wyświetla menu zarządzania użytkownikami.
        Displays the user management menu.
        """
    print("1. Dodaj użytkownika")
    print("2. Zmodyfikuj użytkownika")
    print("3. Usuń użytkownika")
    print("4. Pokaż wszystkich użytkowników")
    print("0. Powrót do głównego menu")

    choice = input("Wybierz opcję: ")
    if choice == "1":
        add_user()
    elif choice == "2":
        modify_user()
    elif choice == "3":
        delete_user()
    elif choice == "4":
        list_users()
    elif choice == "0":
        return
    else:
        print("Nieprawidłowa opcja!")


def add_user():
    """
        Pozwala na dodanie nowego użytkownika.
        Allows adding a new user.
        """
    username = input("Podaj nazwę użytkownika: ")
    password = input("Podaj hasło: ")
    user = User(username=username, password=password)
    with connect() as conn:
        with conn.cursor() as cursor:
            user.save_to_db(cursor)
    print("Użytkownik został dodany.")


def modify_user():
    """
       Pozwala na modyfikację istniejącego użytkownika.
       Allows modifying an existing user.
       """
    user_id = input("Podaj ID użytkownika do modyfikacji: ")
    new_username = input("Podaj nową nazwę użytkownika: ")
    new_password = input("Podaj nowe hasło: ")
    with connect() as conn:
        with conn.cursor() as cursor:
            user = User.load_user_by_id(cursor, user_id)
            if user:
                user.username = new_username
                user.set_password(new_password)
                user.save_to_db(cursor)
                print("Użytkownik został zaktualizowany.")
            else:
                print("Nie znaleziono użytkownika.")


def delete_user():
    """
       Umożliwia usunięcie użytkownika.
       Enables the deletion of a user.
       """
    user_id = input("Podaj ID użytkownika do usunięcia: ")
    with connect() as conn:
        with conn.cursor() as cursor:
            user = User.load_user_by_id(cursor, user_id)
            if user:
                user.delete(cursor)
                print("Użytkownik został usunięty.")
            else:
                print("Nie znaleziono użytkownika.")


def list_users():
    """
        Wyświetla listę wszystkich użytkowników.
        Displays a list of all users.
        """
    with connect() as conn:
        with conn.cursor() as cursor:
            users = User.load_all_users(cursor)
            for user in users:
                print(f"ID: {user.id}, Nazwa użytkownika: {user.username}")


def manage_messages():
    """
       Wyświetla menu zarządzania wiadomościami.
       Displays the message management menu.
       """
    print("1. Wyślij wiadomość")
    print("2. Pokaż moje wiadomości")
    print("0. Powrót do głównego menu")

    choice = input("Wybierz opcję: ")
    if choice == "1":
        send_message()
    elif choice == "2":
        list_messages()
    elif choice == "0":
        return
    else:
        print("Nieprawidłowa opcja!")


def send_message():
    """
       Pozwala na wysłanie wiadomości do innego użytkownika.
       Allows sending a message to another user.
       """
    from_id = input("Podaj swoje ID: ")
    to_id = input("Podaj ID odbiorcy: ")
    text = input("Wpisz wiadomość: ")
    message = Message(from_id=from_id, to_id=to_id, text=text)
    with connect() as conn:
        with conn.cursor() as cursor:
            message.save_to_db(cursor)
    print("Wiadomość została wysłana.")


def list_messages():
    """
       Wyświetla wszystkie wiadomości dla danego użytkownika.
       Displays all messages for a given user.
       """
    user_id = input(int("Podaj swoje ID, aby zobaczyć wiadomości: "))
    with connect() as conn:
        with conn.cursor() as cursor:
            messages = Message.load_all_messages(cursor, user_id)
            for msg in messages:
                print(f"Od: {msg.from_id}, Do: {msg.to_id}, Wiadomość: {msg.text}, Data: {msg.creation_date}")


if __name__ == "__main__":
    """
        Główny punkt wejścia do aplikacji. Wywołuje główne menu w pętli.
        The main entry point of the application. Calls the main menu in a loop.
        """
    while True:
        main_menu()
