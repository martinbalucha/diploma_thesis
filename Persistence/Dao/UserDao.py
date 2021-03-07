import bcrypt
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

        connection = DBConnector.create_connection()
        query = "SELECT * FROM user WHERE login = %s"
        user = sqlio.read_sql(query, params=login, con=connection)
        connection.close()
        return user

    def get_users(self) -> DataFrame:
        """
        Gets IDs of all registered users
        :return: a dataframe of all users registered in the system
        """

        query = "SELECT id FROM users"
        connection = DBConnector.create_connection()
        users = sqlio.read_sql(query, connection)
        connection.close()
        return users

    def create(self, username: str, password: str) -> None:
        """
        Stores a new user into the database
        :param username: a username of the new user
        :param password: password of the new user
        """

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        query = """INSERT INTO users VALUES(login, password_hash)
                    VALUES (%s, %s)"""

        with DBConnector.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (username, hashed_password))
                connection.commit()
