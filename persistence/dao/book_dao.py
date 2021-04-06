from dto.Filters.book_filter import BookFilter
from pandas import DataFrame
import pandas.io.sql as sqlio
from psycopg2.extras import DictCursor, RealDictCursor
from persistence import db_connector, query_storage


class BookDao:
    """
    Data access object for books
    """

    def find_book_by_id(self, book_filter: BookFilter) -> dict:
        """
        Finds the book with given ID
        :param book_filter: book filter
        :return: a dictionary with required book. None is does not exist
        """

        query = """SELECT b.id, b.author, b.title, b.year, b.pages, b."tableOfContents",
                          b.isbn, b.description, t.name AS "topicName", r.rating
                    FROM book b
                    INNER JOIN topic t ON t.id = b.topic
                    LEFT JOIN rating r ON r."bookId" = b.id AND r."userId" = %s
                    WHERE b.id = %s"""

        with db_connector.create_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (book_filter.user_id, book_filter.book_id,))
                return cursor.fetchone()

    def get_best_rated_books(self, user_id: int) -> DataFrame:
        """
        Gets IDs of best rated books by the user
        :param user_id: ID of user whose best rated books will be returned
        :return: a dataframe of best rated books
        """

        query = """SELECT b.*, t.name as "topicName" FROM rating r
                    INNER JOIN book b ON b.id = r."bookId"
                    INNER JOIN topic t ON t.id = b.topic
                    WHERE "userId" = %s AND rating >= 3 ORDER BY r.rating DESC"""

        with db_connector.create_connection() as connection:
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
        with db_connector.create_connection() as connection:
            return sqlio.read_sql(query, connection, params=(user_id,))

    def find_books(self, book_filter: BookFilter) -> tuple:
        """
        Finds books that fulfill broad criteria in the filter
        :param book_filter: book filter
        :return: a list of dictionaries containing information about found books
        """

        query = query_storage.find_books_query()
        book_count_query = query_storage.find_books_count_query()
        title_wildcard = self._add_wildcard_to_string(book_filter.title)
        author_wildcard = self._add_wildcard_to_string(book_filter.author, True)
        parameters = (title_wildcard, author_wildcard, book_filter.page_size,
                      (book_filter.page_number - 1) * book_filter.page_size )

        with db_connector.create_connection() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(book_count_query, (title_wildcard, author_wildcard))
                count = cursor.fetchone()["count"]
                cursor.execute(query, parameters)
                return cursor.fetchall(), count

    def _add_wildcard_to_string(self, string: str, with_prefix_wildcard: bool = False) -> str:
        """
        Appends wildcard symbol to the string used in filtering. If the 'with_prefix_wildcard' parameter is True,
        also adds wildcard in front of the string
        :param string: input string
        :param with_prefix_wildcard: optional parameter set to False. If true, method also puts wildcard in front
        of the string
        :return: string adjusted with wildcards. If the input string is None, no change is made and None is returned
        """

        if string is not None:
            string = string + "%"
            if with_prefix_wildcard:
                string = "%" + string
        return string

    def find_candidate_books(self, user_id: int, topics: list) -> DataFrame:
        """
        Finds all books that the user can understand and has not read them yet
        :param user_id: id of a user
        :param topics: a list of topic ids
        :return: a dataframe containing all books that the user could read next
        """

        query = query_storage.find_candidate_books_query()
        with db_connector.create_connection() as connection:
            return sqlio.read_sql(query, con=connection, params=(user_id, tuple(topics)))

    def find_rated_books(self, book_filter: BookFilter) -> tuple:
        """
        Finds all books rated by the user
        :param book_filter: book filter
        :return: a dataframe of all books rated by the given user
        """

        query = query_storage.rated_books_query()
        rated_book_count_query = query_storage.rated_books_count_query()
        parameters = (book_filter.user_id, book_filter.page_size, (book_filter.page_number - 1) * book_filter.page_size)
        with db_connector.create_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(rated_book_count_query, (book_filter.user_id,))
                count = cursor.fetchone()["count"]
                cursor.execute(query, parameters)
                return cursor.fetchall(), count
