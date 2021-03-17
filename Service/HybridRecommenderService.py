from Service import IDiversityService
from Service.IRecommenderService import IRecommenderService


class HybridRecommenderService(IRecommenderService):
    """
    A recommender service combining content-based filtering
    and collaborative filtering
    """

    content_based_service: IRecommenderService
    matrix_factorization_service: IRecommenderService
    diversity_service: IDiversityService

    def __init__(self, content_based_service: IRecommenderService, matrix_factorization_service: IRecommenderService,
                 diversity_service: IDiversityService):
        """
        Ctor
        :param content_based_service: Content-based recommendation service
        :param matrix_factorization_service: Matrix factorization service
        :param diversity_service: Diversity calculation service
        """

        self.content_based_service = content_based_service
        self.matrix_factorization_service = matrix_factorization_service
        self.diversity_service = diversity_service

    def recommend(self, size: int):
        """
        Performs recommendation algorithm
        :param size: the size of the result set
        :return: a set of recommended books of the required size
        """


        first_recommendation_set = self.content_based_service.recommend(15)
        second_recommendation_set = self.matrix_factorization_service(15)
        pass
