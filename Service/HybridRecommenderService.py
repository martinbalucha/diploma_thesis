from Service import ContentBasedRecommenderService, MatrixFactorizationService


class HybridRecommenderService:
    """
    A recommender service combining content-based filtering
    and collaborative filtering
    """

    content_based_service: ContentBasedRecommenderService
    matrix_factorization_service: MatrixFactorizationService

    def __init__(self, content_based_service: ContentBasedRecommenderService,
                 matrix_factorization_service: MatrixFactorizationService):
        """
        Ctor
        :param content_based_service: Content-based recommendation service
        :param matrix_factorization_service: Matrix factorization service
        """

        self.content_based_service = content_based_service
        self.matrix_factorization_service = matrix_factorization_service

    def recommend(self, size: int):
        """
        Performs recommendation algorithm
        :param size: the size of the result set
        :return: a set of recommended books of the required size
        """

        pass
