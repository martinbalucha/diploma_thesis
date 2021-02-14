from pandas import DataFrame
import pandas.io.sql as sqlio
import DBConnector


class BookDao:
    """
    Data access objects for books
    """

    def get_books(self) -> DataFrame:
        """
        Gets the set of all books in the table
        :return: a dataframe containing all stored books
        """

        connection = DBConnector.create_connection()
        query = "SELECT * FROM books"
        books = sqlio.read_sql(query, connection)
        connection.close()
        return books
