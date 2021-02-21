import pandas.io.sql as sqlio
import DBConnector
from pandas import DataFrame
from BusinessLogic.DomainObjects import User


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

    def create(self, user: User) -> None:
        """
        Stores a new user into the database
        :param user: a new user that will be stored
        """

        query = """INSERT INTO users VALUES(id, login, password_hash)
                    VALUES (%d, %s, %s)"""

        connection = DBConnector.create_connection()

        connection.close()
