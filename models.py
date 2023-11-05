import hashlib
import random
import datetime

# Определите ALPHABET где-то в начале файла/# Define ALPHABET at the beginning of the file
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def hash_password(password, salt=None):
    """
    Hashes the password with salt as an optional parameter.

    If salt is not provided, generates random salt.
    If salt is less than 16 chars, fills the string to 16 chars.
    If salt is longer than 16 chars, cuts salt to 16 chars.

    :param str password: password to hash
    :param str salt: salt to hash, default None

    :rtype: str
    :return: hashed password
    """

    # generate salt if not provided
    if salt is None:
        salt = generate_salt()

    # fill to 16 chars if too short
    if len(salt) < 16:
        salt += ("a" * (16 - len(salt)))

    # cut to 16 if too long
    if len(salt) > 16:
        salt = salt[:16]

    # use sha256 algorithm to generate haintegersh
    t_sha = hashlib.sha256()

    # we have to encode salt & password to utf-8, this is required by the
    # hashlib library.
    t_sha.update(salt.encode('utf-8') + password.encode('utf-8'))

    # return salt & hash joined
    return salt + t_sha.hexdigest()


def check_password(pass_to_check, hashed):
    """
    Checks the password.
    The function does the following:
        - gets the salt + hash joined,
        - extracts salt and hash,
        - hashes `pass_to_check` with extracted salt,
        - compares `hashed` with hashed `pass_to_check`.
        - returns True if password is correct, or False. :)

    :param str pass_to_check: not #hashed password
    :param str hashed: #hashed password

    :rtype: bool
    :return: True if password is correct, False elsewhere
    """

    # extract salt
    salt = hashed[:16]

    # extract hash to compare with
    hash_to_check = hashed[16:]

    # hash password with extracted salt
    new_hash = hash_password(pass_to_check, salt)

    # compare hashes. If equal, return True
    return new_hash[16:] == hash_to_check


def generate_salt():
    """
    Generates a 16-character random salt.

    :rtype: str
    :return: str with generated salt
    """
    salt = ""
    for i in range(0, 16):
        # get a random element from the iterable
        salt += random.choice(ALPHABET)
    return salt


class User:
    def __init__(self, username="", password="", salt=""):
        """
               Initialize a new User instance.

               :param str username: The username of the user (default is empty string).
               :param str password: The password of the user before hashing (default is empty string).
               :param str salt: The salt used for hashing the password (default is empty string).

               Inicjalizuje nową instancję klasy Użytkownik.

               :param str username: Nazwa użytkownika (domyślnie pusty ciąg).
               :param str password: Hasło użytkownika przed zahashowaniem (domyślnie pusty ciąg).
               :param str salt: Sól używana do hashowania hasła (domyślnie pusty ciąg).
               """
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        """
              The user's ID property.

              :return: Returns the user's ID.
              :rtype: int

              Właściwość ID użytkownika.

              :return: Zwraca ID użytkownika.
              :rtype: int
              """
        return self._id

    @property
    def hashed_password(self):
        """
                The user's hashed password property.

                :return: Returns the user's hashed password.
                :rtype: str

                Właściwość zahashowanego hasła użytkownika.

                :return: Zwraca zahashowane hasło użytkownika.
                :rtype: str
                """
        return self._hashed_password

    def set_password(self, password, salt=""):
        """
               Sets the user's password after hashing it with the given salt.

               :param str password: The password to be set for the user.
               :param str salt: The salt to be used for hashing (default is empty string).

               Ustawia hasło użytkownika po jego zahashowaniu z użyciem danej soli.

               :param str password: Hasło do ustawienia dla użytkownika.
               :param str salt: Sól używana do hashowania (domyślnie pusty ciąg).
               """
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        """
                Setter for the hashed password. It sets the password using the set_password method.

                :param str password: The password to hash and set.

                Setter dla zahashowanego hasła. Ustawia hasło przy użyciu metody set_password.

                :param str password: Hasło do zahashowania i ustawienia.
                """
        self.set_password(password)

    def save_to_db(self, cursor):
        """
                Saves the user to the database. Inserts a new record if the user's ID is -1,
                otherwise updates the existing record.

                :param cursor: The database cursor.
                :return: Returns True if the operation was successful.
                :rtype: bool

                Zapisuje użytkownika do bazy danych. Wstawia nowy rekord, jeśli ID użytkownika to -1,
                w przeciwnym razie aktualizuje istniejący rekord.

                :param cursor: Kursor bazy danych.
                :return: Zwraca True, jeśli operacja się powiodła.
                :rtype: bool
                """
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        """
               Loads a user from the database by the user ID.

               :param cursor: The database cursor.
               :param int id_: The ID of the user to load.
               :return: Returns a User instance if found, otherwise None.
               :rtype: User or None

               Ładuje użytkownika z bazy danych po ID użytkownika.

               :param cursor: Kursor bazy danych.
               :param int id_: ID użytkownika do załadowania.
               :return: Zwraca instancję Użytkownika jeśli znajdzie, w przeciwnym razie None.
               :rtype: User or None
               """
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        """
               Loads all users from the database.

               :param cursor: The database cursor.
               :return: Returns a list of User instances.
               :rtype: list of User

               Ładuje wszystkich użytkowników z bazy danych.

               :param cursor: Kursor bazy danych.
               :return: Zwraca listę instancji Użytkowników.
               :rtype: list of User
               """
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        """
              Deletes the user from the database.

              :param cursor: The database cursor.
              :return: Returns True if the user was successfully deleted.
              :rtype: bool

              Usuwa użytkownika z bazy danych.

              :param cursor: Kursor bazy danych.
              :return: Zwraca True, jeśli użytkownik został pomyślnie usunięty.
              :rtype: bool
              """
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Message:
    def __init__(self, from_id, to_id, text, creation_date=None):
        """
               Initializes a new instance of the Message class.

               :param from_id: Sender's identifier.
               :param to_id: Recipient's identifier.
               :param text: Content of the message.
               :param creation_date: The date and time the message was created. Defaults to the current time if not provided.

               :type from_id: int
               :type to_id: int
               :type text: str
               :type creation_date: datetime

               EN: Initializes a message with sender, receiver, message text, and creation date.
               PL: Inicjalizuje wiadomość z nadawcą, odbiorcą, tekstem wiadomości i datą utworzenia.
               """
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date if creation_date else datetime.datetime.now()

    @property
    def id(self):
        """
              EN: Gets the identifier of the message.
              PL: Pobiera identyfikator wiadomości.

              :rtype: int
              :return: The unique identifier for this message.
              """
        return self._id

    def save_to_db(self, cursor):
        """
               Saves the message to the database.

               EN: Saves the message to the database using the provided cursor. If the message is new, it inserts it;
               otherwise, it updates the existing message.
               PL: Zapisuje wiadomość do bazy danych za pomocą dostarczonego kursora. Jeśli wiadomość jest nowa,
               ona jest wstawiana; w przeciwnym razie aktualizuje istniejącą wiadomość.

               :param cursor: The database cursor to use for the operation.
               :type cursor: cursor

               :rtype: bool
               :return: True if the message was saved successfully, False otherwise.
               """
        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text, creation_date)
                     VALUES(%s, %s, %s, %s) RETURNING id"""
            values = (self.from_id, self.to_id, self.text, self.creation_date)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE messages SET from_id=%s, to_id=%s, text=%s, creation_date=%s
                      WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self.creation_date, self._id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_message_by_id(cursor, id_):
        """
               Loads a message by its identifier.

               EN: Retrieves a message from the database using its unique identifier.
               PL: Pobiera wiadomość z bazy danych za pomocą jej unikalnego identyfikatora.

               :param cursor: The database cursor to use for the query.
               :param id_: The unique identifier of the message to retrieve.

               :type cursor: cursor
               :type id_: int

               :rtype: Message or None
               :return: The loaded message if found, None otherwise.
               """
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE id=%s"
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, from_id, to_id, text, creation_date = data
            loaded_message = Message(from_id, to_id, text, creation_date)
            loaded_message._id = id_
            return loaded_message
        return None

    @staticmethod
    def load_all_messages(cursor):
        """
                Loads all messages from the database.

                EN: Retrieves all messages from the database and returns them as a list of Message objects.
                PL: Pobiera wszystkie wiadomości z bazy danych i zwraca je jako listę obiektów Message.

                :param cursor: The database cursor to use for the query.
                :type cursor: cursor

                :rtype: list[Message]
                :return: A list of all loaded messages.
                """
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Message(from_id, to_id, text, creation_date)
            loaded_message._id = id_
            messages.append(loaded_message)
        return messages
