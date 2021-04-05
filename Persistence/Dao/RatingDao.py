from pandas import DataFrame
import pandas.io.sql as sqlio
from Persistence import DBConnector, QueryStorage
from DTO import RatingDto


class RatingDao:
    """
    Data access object for book ratings
    """

    def get_user_item_matrix(self) -> DataFrame:
        """
        Returns user-item matrix in a dataframe
        :return: a dataframe of book ratings of each user
        """

        query = QueryStorage.user_item_matrix_query()
        with DBConnector.create_connection() as connection:
            return sqlio.read_sql(query, connection)

    def create(self, rating: RatingDto) -> None:
        """
        Creates book rating
        :param rating: a book rating
        """

        query = QueryStorage.insert_rating_query()
        with DBConnector.create_connection() as connection:
            with connection.cursor() as cursor:
                parameters = (rating.book_id, rating.user_id, rating.rating)
                cursor.execute(query, parameters)
                connection.commit()

    def update(self, rating: RatingDto) -> None:
        """
        Updates book rating
        :param rating: a book rating that is to be updated
        """

        query = QueryStorage.update_rating_query()
        with DBConnector.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (rating.rating, rating.book_id, rating.user_id))
                connection.commit()
