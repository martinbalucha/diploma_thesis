from pandas import DataFrame
import pandas.io.sql as sqlio
from persistence import db_connector, query_storage
from dto import rating_dto


class RatingDao:
    """
    Data access object for book ratings
    """

    def get_user_item_matrix(self) -> DataFrame:
        """
        Returns user-item matrix in a dataframe
        :return: a dataframe of book ratings of each user
        """

        query = query_storage.user_item_matrix_query()
        with db_connector.create_connection() as connection:
            return sqlio.read_sql(query, connection)

    def create(self, rating: rating_dto) -> None:
        """
        Creates book rating
        :param rating: a book rating
        """

        query = query_storage.insert_rating_query()
        with db_connector.create_connection() as connection:
            with connection.cursor() as cursor:
                parameters = (rating.book_id, rating.user_id, rating.rating)
                cursor.execute(query, parameters)
                connection.commit()

    def update(self, rating: rating_dto) -> None:
        """
        Updates book rating
        :param rating: a book rating that is to be updated
        """

        query = query_storage.update_rating_query()
        with db_connector.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (rating.rating, rating.book_id, rating.user_id))
                connection.commit()
