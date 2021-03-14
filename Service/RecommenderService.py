

class RecommenderService:
    """
    Interface for recommender service
    """

    def recommend(self, count: int) -> list:
        """
        Provides book recommendation of a given size
        :param count: a number of books to be recommended
        :return: a list of suggested books
        """

        raise NotImplementedError
