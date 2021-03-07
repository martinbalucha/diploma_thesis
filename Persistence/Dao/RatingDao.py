from pandas import DataFrame
import pandas.io.sql as sqlio
from Persistence import DBConnector
from Persistence.Entities import Rating


class RatingDao:
    """
    Data access object for book ratings
    """

    def get_user_item_matrix(self) -> DataFrame:
        """
        Returns user-item matrix in a dataframe
        :return: a dataframe of book ratings of each user
        """
        query = "SELECT * FROM rating"
        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, connection)

    def create(self, rating: Rating) -> None:
        """
        Creates book rating
        :param rating: a book rating
        """

        command = """INSERT INTO rating ("bookId", "userId", rating) VALUES(%d, %d, %d)"""
        with DBConnector.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(command, (rating.book_id, rating.user_id, rating.rating))
                connection.commit()

    def update(self, rating: Rating) -> None:
        """
        Updates book rating
        :param rating: a book rating that is to be updated
        """

        command = """UPDATE rating SET rating = %d WHERE "bookId" = %d AND "userId" = %d"""
        with DBConnector.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(command, (rating.rating, rating.book_id, rating.user_id))
                connection.commit()