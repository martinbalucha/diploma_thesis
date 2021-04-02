from pandas import DataFrame
import pandas.io.sql as sqlio
from psycopg2.extras import DictCursor
from Persistence import DBConnector


class BookDao:
    """
    Data access object for books
    """

    def find_book_by_id(self, book_id: int, user_id: int) -> dict:
        """
        Finds the book with given ID
        :param book_id: ID of the wanted book
        :param user_id: ID of the target user
        :return: a dictionary with required book. None is does not exist
        """

        query = """SELECT b.id, b.author, b.title, b.year, b.pages, b."tableOfContents",
                          b.isbn, b.description, t.name AS "topicName"
                    FROM book b
                    INNER JOIN topic t ON t.id = b.topic
                    LEFT JOIN rating r ON r."bookId" = b.id AND r."userId" = %s
                    WHERE b.id = %s"""

        with DBConnector.create_connection() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id, book_id,))
                return cursor.fetchone()

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

    def get_candidate_books_collaborative(self, user_id: int) -> DataFrame:
        """
        Returns all rated books by other users
        :param user_id: ID of the target user.
        :return: a dataframe of all rated books by other users
        """

        query = """SELECT b.*, t.name as "topicName" FROM book b 
                    INNER JOIN topic t on b.topic = t.id
                    WHERE b.id IN (SELECT "bookId" FROM rating WHERE "userId" != %s)"""
        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, connection, params=(user_id,))

    def find_books_by_title(self, title: str) -> list:
        """
        Finds books that have
        :param title: a title of the book
        :return: a list of dictionaries containing information about found books
        """

        query = """SELECT book.*, t.name as "topicName" FROM book 
                    INNER JOIN topic t on book.topic = t.id
                    WHERE lower(title) LIKE %s"""
        title_wildcard = title + "%"
        with DBConnector.create_connection() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (title_wildcard,))
                return cursor.fetchall()

    def find_candidate_books(self, user_id: int, topics: list) -> DataFrame:
        """
        Finds all books that the user can understand and has not read them yet
        :param user_id: id of a user
        :param topics: a list of topic ids
        :return: a dataframe containing all books that the user could read next
        """

        query = """SELECT DISTINCT b.*, t.name as "topicName" FROM book b
                    LEFT JOIN rating r ON b.id = r."bookId"
                    INNER JOIN topic t ON t.id = b.topic
                    WHERE (r."userId" IS DISTINCT FROM %s) AND b.language = 1
                    AND t.id IN %s"""

        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, con=connection, params=(user_id, tuple(topics)))

    def find_rated_books(self, user_id: int) -> DataFrame:
        """
        Finds all books rated by the user
        :param user_id: an id of the user whose rated books will be returned
        :return: a dataframe of all books rated by the given user
        """

        query = """SELECT b.*, r.rating, t.name as "topicName"
                    FROM book b
                    INNER JOIN rating r ON b.id = r."bookId"
                    INNER JOIN topic t on b.topic = t.id
                    WHERE r."userId" = %s"""

        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, params=(user_id,), con=connection)
