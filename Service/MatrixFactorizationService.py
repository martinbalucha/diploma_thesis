from surprise import SVD, Reader
from surprise import Dataset
from Persistence.Dao import RatingDao


class MatrixFactorizationService:
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

    def get_n_recommendations(self, count: int) -> list:
        """
        Finds the n predicted books that the target user will
        like the most
        :param count: the number of closest books that will be returned
        :return: a list of n books
        """

        recommended_books = self.recommend()


    def recommend(self) -> list:
        """
        Performs matrix factorization and returns recommended books
        :return:
        """

        user_item_matrix = self.rating_dao.get_user_item_matrix()
        ratings_dataset = Dataset.load_from_df(user_item_matrix, Reader())
        trainset = ratings_dataset.build_full_trainset()
        self.svd.fit(trainset)

        test_set = trainset.build_anti_testset()
        prediction_set = self.svd.test(test_set)
        return prediction_set
