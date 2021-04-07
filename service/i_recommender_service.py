from pandas import DataFrame


class IRecommenderService:
    """
    Interface for recommender service
    """

    def recommend(self, user_id: int, count: int) -> DataFrame:
        """
        Provides book recommendation of a given size
        :param user_id: ID of a user for whom the recommendation will be made
        :param count: a number of books to be recommended
        :return: a dataframe of suggested books. If no books were recommended, an empty
        dataframe is returned
        """

        raise NotImplementedError
