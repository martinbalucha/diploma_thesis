

class IRecommenderService:
    """
    Interface for recommender service
    """

    def recommend(self, user_id: int, count: int) -> list:
        """
        Provides book recommendation of a given size
        :param user_id: ID of a user for whom the recommendation will be made
        :param count: a number of books to be recommended
        :return: a list of suggested books
        """

        raise NotImplementedError
