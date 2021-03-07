from typing import List

from pandas import DataFrame
import pandas.io.sql as sqlio
from Persistence import DBConnector


class BookDao:
    """
    Data access object for books
    """

    def get_books(self) -> DataFrame:
        """
        Gets the set of all books in the table
        :return: a dataframe containing all stored books
        """

        connection = DBConnector.create_connection()
        query = "SELECT * FROM book"
        books = sqlio.read_sql(query, connection)
        connection.close()
        return books

    def get_user_item_matrix(self):
        pass

    def find_books(self, criteria: List[str] = None) -> DataFrame:
        """

        :param criteria: an optional parameter of additional criteria
        :return: a dataframe with books that satisfy the optional criteria
        """

        connection = DBConnector.create_connection()
        query = "SELECT * FROM book"
