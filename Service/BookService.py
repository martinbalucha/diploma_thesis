from pandas import DataFrame
from DTO.Filters.BookFilter import BookFilter
from Persistence.Dao import BookDao


class BookService:
    """
    Service class for operation on books
    """

    _book_dao: BookDao

    def __init__(self, book_dao: BookDao):
        """
        Ctor
        :param book_dao: DAO for books
        """

        self._book_dao = book_dao

    def find_rated_books(self, book_filter: BookFilter) -> DataFrame:
        """
        Finds all books rated by the user with given ID
        :param book_filter: a book filter
        :return: a dataframe containing all books rated by the user and their ratings
        """

        return self._book_dao.find_rated_books(book_filter)

    def find_book(self, book_filter: BookFilter) -> dict:
        """
        Finds the book with the given ID
        :param book_filter: book filter
        :return: a dictionary with book information. None, if does not exist
        """

        return self._book_dao.find_book_by_id(book_filter)

    def find_book_by_title(self, book_filter: BookFilter) -> tuple:
        """
        Finds books which have title starting with the given parameter
        :param book_filter: book filter
        :return: a dataframe containing books withe the given title
        """

        return self._book_dao.find_books(book_filter)
