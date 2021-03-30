from pandas import DataFrame
from Persistence.Dao import BookDao


class BookService:
    """
    Service class for operation on books
    """

    book_dao: BookDao

    def __init__(self, book_dao: BookDao):
        """
        Ctor
        :param book_dao: DAO for books
        """
        self.book_dao = book_dao

    def rated_books(self, user_id: int) -> DataFrame:
        """
        Finds all books rated by the user with given ID
        :param user_id: ID of the user whose rated books will be found
        :return: a dataframe containing all books rated by the user and their ratings
        """

        rated_books = self.book_dao.find_rated_books(user_id)
        rated_books = rated_books[["title", "author", "year", "pages", "rating", "topicName"]]
        rated_books.rename(columns={"topicName": "Topic"})
        return rated_books
