from pandas import Series, DataFrame
from surprise import SVD, Reader, accuracy, Dataset
from Persistence.Dao import RatingDao, BookDao
from Service.IRecommenderService import IRecommenderService


class MatrixFactorizationService(IRecommenderService):
    """
    A matrix factorization service using singular value decomposition
    """

    svd: SVD
    rating_dao: RatingDao
    book_dao: BookDao

    def __init__(self, svd: SVD, rating_dao: RatingDao, book_dao: BookDao):
        """
        Ctor
        :param svd: a singular value decomposition
        :param rating_dao: a data access object for ratings
        :param book_dao: a data access object for books
        """

        self.svd = svd
        self.rating_dao = rating_dao
        self.book_dao = book_dao

    def recommend(self, user_id: int, count: int) -> DataFrame:
        reader = Reader(line_format="user item rating", rating_scale=(1, 5))
        ratings = self.rating_dao.get_user_item_matrix()
        rated_by_user = ratings.loc[ratings["userId"] == user_id, "bookId"]

        books = self.book_dao.get_candidate_books_collaborative(user_id)
        ratings_dataset = Dataset.load_from_df(ratings, reader)
        train_set = ratings_dataset.build_full_trainset()

        self.svd.fit(train_set)
        books["predictedRatings"] = books.apply(self._make_all_predictions, ratings=rated_by_user,
                                                user_id=user_id, axis=1)

        books = books.sort_values("predictedRatings", ascending=False)
        return books.head(count)

    def _make_all_predictions(self, book: Series, ratings: Series, user_id: int) -> float:
        """
        Extracts predicted rating for a book.
        :param book: series containing book ID
        :param user_id: ID of a user for whom the prediction will be made
        :return: float value representing predicted rating
        """

        return self.svd.predict(uid=user_id, iid=book["id"]).est

