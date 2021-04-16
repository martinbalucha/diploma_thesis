from math import floor
from multiprocessing import Pool
from pandas import DataFrame
from service.i_diverse_selection_service import IDiverseSelectionService
from service.i_recommender_service import IRecommenderService


class HybridRecommenderService(IRecommenderService):
    """
    A recommender service combining content-based filtering and collaborative filtering
    """

    _content_based_service: IRecommenderService
    _matrix_factorization_service: IRecommenderService
    _diversity_service: IDiverseSelectionService

    def __init__(self, content_based_service: IRecommenderService, collaborative_filtering_service: IRecommenderService,
                 diversity_service: IDiverseSelectionService):
        """
        Ctor
        :param content_based_service: Content-based recommendation service
        :param collaborative_filtering_service: Matrix factorization service
        :param diversity_service: Diversity calculation service
        """

        self._content_based_service = content_based_service
        self._matrix_factorization_service = collaborative_filtering_service
        self._diversity_service = diversity_service

    def recommend(self, user_id: int, count: int) -> DataFrame:
        books_per_algo = floor((count // 2) * 1.5)

        with Pool(processes=2) as pool:
            cb_tmp = pool.apply_async(self._content_based_service.recommend, args=(user_id, books_per_algo))
            cf_tmp = pool.apply_async(self._matrix_factorization_service.recommend, args=(user_id, books_per_algo))

            content_based_recommendations = cb_tmp.get()
            collaborative_recommendations = cf_tmp.get()

            recommendations = content_based_recommendations.append(collaborative_recommendations)
            diverse_recommendations = self._diversity_service.diversify(recommendations, count)
            return diverse_recommendations
