from psycopg2.extras import RealDictCursor, RealDictRow
from persistence import db_connector, query_storage


class UserDao:
    """
    Data access object for users
    """

    def get_user_by_login(self, login: str) -> RealDictRow:
        """
        Finds the user with the given login
        :param login: a string that should be login of the wanted user
        :return: a tuple with the user. Null, if no user with given
        login exists
        """

        query = query_storage.find_user_by_login_query()
        with db_connector.create_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (login,))
                return cursor.fetchone()

    def get_user(self, user_id: int) -> RealDictRow:
        """
        Finds the user with the given ID
        :param user_id: ID of the wanted user
        :return: tuple containing information about the user with given ID.
        Null if the user was not found 
        """

        query = query_storage.find_user_by_id_query()
        with db_connector.create_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()

    def create(self, username: str, password_hash: str) -> None:
        """
        Stores a new user into the database
        :param username: a username of the new user
        :param password_hash: hashed password of the new user
        """

        query = query_storage.insert_user_query()
        with db_connector.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (username, password_hash))
                connection.commit()
