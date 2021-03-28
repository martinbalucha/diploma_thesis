import pandas.io.sql as sqlio
from pandas import DataFrame
from Persistence import DBConnector


class UserDao:
    """
    Data access object for users
    """

    def get_user(self, login: str):
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

    def get_users(self) -> DataFrame:
        """
        Gets IDs of all registered users
        :return: a dataframe of all users registered in the system
        """

        query = "SELECT id FROM users"
        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, connection)

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
