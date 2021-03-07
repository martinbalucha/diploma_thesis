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

    def get_best_rated_books(self, user_id: int):
        """

        :param user_id:
        :return:
        """

        pass