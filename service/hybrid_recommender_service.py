import multiprocessing
from pandas import DataFrame
from service import i_diversity_service
from service.i_recommender_service import IRecommenderService


class HybridRecommenderService(IRecommenderService):
    """
    A recommender service combining content-based filtering
    and collaborative filtering
    """

    content_based_service: IRecommenderService
    matrix_factorization_service: IRecommenderService
    diversity_service: i_diversity_service

    def __init__(self, content_based_service: IRecommenderService, collaborative_filtering_service: IRecommenderService,
                 diversity_service: i_diversity_service):
        """
        Ctor
        :param content_based_service: Content-based recommendation service
        :param collaborative_filtering_service: Matrix factorization service
        :param diversity_service: Diversity calculation service
        """

        self.content_based_service = content_based_service
        self.matrix_factorization_service = collaborative_filtering_service
        self.diversity_service = diversity_service

    def recommend(self, user_id: int, count: int) -> DataFrame:
        books_per_algorithm = count // 2
        content_based_recommendations = self.content_based_service.recommend(user_id, books_per_algorithm)
        collaborative_recommendations = self.matrix_factorization_service.recommend(user_id, books_per_algorithm)

        recommendations = content_based_recommendations.append(collaborative_recommendations)
        recommendations.reset_index(drop=True, inplace=True)
        diverse_recommendations = self.diversity_service.diversify(recommendations, 20)
        return diverse_recommendations
