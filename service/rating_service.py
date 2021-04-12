from persistence.dao.rating_dao import RatingDao
from dto.rating_dto import RatingDto


class RatingService:
    """
    A service for ratings
    """

    _rating_dao: RatingDao

    def __init__(self, rating_dao: RatingDao):
        """
        Ctor
        :param rating_dao: DAO for ratings
        """

        self._rating_dao = rating_dao

    def create(self, rating: RatingDto):
        """
        Creates a new rating
        :param rating: dto for rating
        """

        self._rating_dao.create(rating)

    def update(self, rating: RatingDto):
        """
        Updates existing rating
        :param rating: updated rating of the book
        """

        self._rating_dao.update(rating)
