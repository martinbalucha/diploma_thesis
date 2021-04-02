from pandas import DataFrame
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

    def rated_books(self, user_id: int) -> DataFrame:
        """
        Finds all books rated by the user with given ID
        :param user_id: ID of the user whose rated books will be found
        :return: a dataframe containing all books rated by the user and their ratings
        """

        return self._book_dao.find_rated_books(user_id)

    def find_book(self, book_id: int, user_id: int) -> dict:
        """
        Finds the book with the given ID
        :param book_id: ID of the book
        :param user_id: ID of the target user
        :return: a dictionary with book information. None, if does not exist
        """

        return self._book_dao.find_book_by_id(book_id, user_id)

    def find_book_by_title(self, book_title: str) -> DataFrame:
        """
        Finds books which have title starting with the given parameter
        :param book_title: a title of the wanted book
        :return: a dataframe containing books withe the given title
        """

        return self._book_dao.find_books_by_title(book_title.lower())
