import swifter
from math import floor
from multiprocessing import Queue
from pandas import DataFrame
from service.i_diversity_service import IDiversityService
from service.i_recommender_service import IRecommenderService


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

    def recommend(self, user_id: int, count: int) -> DataFrame:
        books_per_algo = floor((count // 2) * 1.5)
        queue = Queue()
        processes = []
        outputs = []

        """
        process1 = Process(target=self._recommend_wrapper, args=(self.content_based_service, user_id, books_per_algo,
                                                                 queue))

        process2 = Process(target=self._recommend_wrapper, args=(self.matrix_factorization_service, user_id,
                                                                 books_per_algo, queue))

        process1.start()
        processes.append(process1)
        process2.start()
        processes.append(process2)

        for process in processes:
            rets = queue.get()
            outputs.append(rets)

        for p in processes:
            p.join()

        """
        content_based_recommendations = self.content_based_service.recommend(user_id, books_per_algo)
        collaborative_recommendations = self.matrix_factorization_service.recommend(user_id, books_per_algo)

        recommendations = content_based_recommendations.append(collaborative_recommendations)
        recommendations.reset_index(drop=True, inplace=True)
        diverse_recommendations = self.diversity_service.diversify(recommendations, count)

        """"
        content_based_recommendations = outputs[0]
        collaborative_recommendations = outputs[1]
        recommendations = content_based_recommendations.append(collaborative_recommendations)
        diverse_recommendations = self.diversity_service.diversify(recommendations, 20)
        """
        return diverse_recommendations

    def _recommend_wrapper(self, recommender: IRecommenderService, user_id: int, count: int,
                           queue: Queue) -> None:
        """
        Wrapper method for receiving recommendations so they can run in parallel and store results into the queue
        :param recommender: recommending service
        :param user_id: ID of the target user
        :param count: number of books to recommend
        :param queue: a thread-safe queue for storing recommended books
        """

        queue.put(recommender.recommend(user_id, count))
