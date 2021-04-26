from pandas import Series, DataFrame
from surprise import SVD, Reader, Dataset
from persistence.dao.book_dao import BookDao
from persistence.dao.rating_dao import RatingDao
from service.i_recommender_service import IRecommenderService


class MatrixFactorizationService(IRecommenderService):
    """
    A matrix factorization service using singular value decomposition
    """

    _svd: SVD
    _rating_dao: RatingDao
    _book_dao: BookDao

    def __init__(self, svd: SVD, rating_dao: RatingDao, book_dao: BookDao):
        """
        Ctor
        :param svd: a singular value decomposition
        :param rating_dao: a data access object for ratings
        :param book_dao: a data access object for books
        """

        self._svd = svd
        self._rating_dao = rating_dao
        self._book_dao = book_dao

    def recommend(self, user_id: int, count: int) -> DataFrame:
        lower_rating_bound = 3.8
        reader = Reader(line_format="user item rating", rating_scale=(1, 5))
        ratings = self._rating_dao.get_user_item_matrix()
        rated_by_user = ratings.loc[ratings["userId"] == user_id, ["bookId", "rating"]]
        if len(rated_by_user.index) == 0:
            return rated_by_user

        books = self._book_dao.get_candidate_books_collaborative(user_id)
        ratings_dataset = Dataset.load_from_df(ratings, reader)
        train_set = ratings_dataset.build_full_trainset()

        self._svd.fit(train_set)
        books["predictedRating"] = books.swifter.apply(self._extract_prediction, user_id=user_id, axis=1)
        books = books[books["predictedRating"] >= lower_rating_bound]
        return books.sample(frac=1).head(count)

    def _extract_prediction(self, book: Series, user_id: int) -> float:
        """
        Extracts predicted rating for a book.
        :param book: series containing book ID
        :param user_id: ID of a user for whom the prediction will be made
        :return: float value representing predicted rating
        """

        return self._svd.predict(uid=user_id, iid=book["id"]).est
