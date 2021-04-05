from pandas import DataFrame


class IDiversityService:
    """
    An interface for a class that ensures diversity of the recommendation set
    """

    def diversify(self, recommended_books: DataFrame, final_set_size: int) -> DataFrame:
        """
        Calculates pair-wise diversity of the recommendation
        set and filters
        :param recommended_books: a dataframe of items recommended by the hybrid recommender system
        :param final_set_size: a desired size of the diverse recommendation set
        :return: a filtered recommendation set that contains the most diverse items
        """

        raise NotImplementedError
