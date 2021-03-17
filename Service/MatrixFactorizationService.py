from surprise import SVD, Reader
from surprise import Dataset
from Persistence.Dao import RatingDao
from Service.IRecommenderService import IRecommenderService


class MatrixFactorizationService(IRecommenderService):
    """
    A matrix factorization service using singular value decomposition
    """

    svd: SVD
    rating_dao: RatingDao

    def __init__(self, svd: SVD, rating_dao: RatingDao):
        """
        Ctor
        :param svd: a singular value decomposition
        :param rating_dao: a data access object for ratings
        """

        self.svd = svd
        self.rating_dao = rating_dao

    def recommend(self, user_id: int, count: int) -> list:
        reader = Reader(rating_scale=(1, 5))
        user_item_matrix = self.rating_dao.get_user_item_matrix()
        ratings_dataset = Dataset.load_from_df(user_item_matrix, reader)
        train_set = ratings_dataset.build_full_trainset()
        self.svd.fit(train_set)

        test_set = train_set.build_anti_testset()
        prediction_set = self.svd.test(test_set)
        return prediction_set
