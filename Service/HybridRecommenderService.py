import multiprocessing
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

    def __init__(self, content_based_service: IRecommenderService, collaborative_filtering_service: IRecommenderService,
                 diversity_service: IDiversityService):
        """
        Ctor
        :param content_based_service: Content-based recommendation service
        :param collaborative_filtering_service: Matrix factorization service
        :param diversity_service: Diversity calculation service
        """

        self.content_based_service = content_based_service
        self.matrix_factorization_service = collaborative_filtering_service
        self.diversity_service = diversity_service

    def recommend(self, user_id: int, count: int):
        content_based_recommendations = self.content_based_service.recommend(user_id, 15)
        collaborative_recommendations = self.matrix_factorization_service.recommend(user_id, 15)
        recommendations = content_based_recommendations.append(collaborative_recommendations)
        diverse_recommendations = self.diversity_service.diversify(recommendations, count // 2)
