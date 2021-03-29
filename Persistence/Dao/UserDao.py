import pandas.io.sql as sqlio
from pandas import DataFrame
from Persistence import DBConnector


class UserDao:
    """
    Data access object for users
    """

    def get_user_by_login(self, login: str):
        """
        Finds the user with the given login
        :param login: a string that should be login of the wanted user
        :return: a dataframe with the user. Null, if no user with given
        login exists
        """

        query = """SELECT id, username, "passwordHash" FROM registered_user WHERE username = %s"""
        with DBConnector.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (login,))
                return cursor.fetchone()

    def get_user(self, user_id: int) -> tuple:
        """
        Finds the user with the given ID
        :param user_id: ID of the wanted user
        :return: tuple containing information about the user with given ID.
        Null if the user was not found 
        """

        query = """SELECT id, username FROM registered_user WHERE id = %s"""
        with DBConnector.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()

    def create(self, username: str, password_hash: str) -> None:
        """
        Stores a new user into the database
        :param username: a username of the new user
        :param password_hash: hashed password of the new user
        """

        query = """INSERT INTO registered_user (username, "passwordHash") VALUES (%s, %s)"""

        with DBConnector.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (username, password_hash))
                connection.commit()
