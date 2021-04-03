from pandas import DataFrame
import pandas.io.sql as sqlio
from Persistence import DBConnector
from Service.DTO import RatingDto


class RatingDao:
    """
    Data access object for book ratings
    """

    def get_user_item_matrix(self) -> DataFrame:
        """
        Returns user-item matrix in a dataframe
        :return: a dataframe of book ratings of each user
        """
        query = """SELECT "userId", "bookId", rating FROM rating
                    LEFT JOIN book ON book.id = rating."bookId"
                    WHERE book.language = 1"""

        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, connection)

    def create(self, rating: RatingDto) -> None:
        """
        Creates book rating
        :param rating: a book rating
        """

        command = """INSERT INTO rating ("bookId", "userId", rating) VALUES (%s, %s, %s)"""
        with DBConnector.create_connection() as connection:
            with connection.cursor() as cursor:
                parameters = (rating.book_id, rating.user_id, rating.rating)
                cursor.execute(command, parameters)
                connection.commit()

    def update(self, rating: RatingDto) -> None:
        """
        Updates book rating
        :param rating: a book rating that is to be updated
        """

        command = """UPDATE rating SET rating = %s WHERE "bookId" = %s AND "userId" = %s"""
        with DBConnector.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(command, (rating.rating, rating.book_id, rating.user_id))
                connection.commit()
