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

    def get_best_rated_books(self, user_id: int) -> DataFrame:
        """
        Gets IDs of best rated books by the user
        :param user_id: ID of user whose best rated books will be returned
        :return: a dataframe of best rated books
        """

        query = """SELECT b.*, t.name as "topicName", t."metaTopic" FROM rating r
                    INNER JOIN book b ON b.id = r."bookId" INNER JOIN topic t ON t.id = b.topic
                    WHERE "userId" = %s AND rating > 3
                    ORDER BY r.rating DESC"""

        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, connection, params=[user_id])

    def find_books_by_title(self, title: str) -> DataFrame:
        """

        :param title: a title of the book
        :return: a dataframe with books that satisfy the optional criteria
        """

        query = "SELECT * FROM book WHERE title = %s"
        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, params=title, con=connection)

    def find_candidate_books(self, user_id: int, topics: list) -> DataFrame:
        """
        Finds all books that the user can understand and has not read them yet
        :param user_id: id of a user
        :param topics: a list of topic ids
        :return: a dataframe containing all books that the user could read next
        """

        query = """SELECT DISTINCT b.*, t.name as "topicName" FROM book b LEFT JOIN rating r ON b.id = r."bookId"
                    INNER JOIN topic t ON t.id = b.topic
                    WHERE (r."userId" IS DISTINCT FROM %s) AND b.language = 1
                    AND t.id IN %s"""

        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, con=connection, params=(user_id, tuple(topics)))

    def find_read_books(self, user_id: int) -> DataFrame:
        """
        Finds all books read by the user
        :param user_id: an id of the user whose read books will be returned
        :return: a dataframe of all books read by the given user
        """

        query = """SELECT b.* FROM book b LEFT JOIN rating r ON b.id = r."bookId"
                    WHERE r."userId" = %d"""

        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, params=user_id, con=connection)
