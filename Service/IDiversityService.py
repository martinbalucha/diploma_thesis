

class IDiversityService:
    """
    Ensures diversity of the recommendation set
    """

    def diversify(self, recommendation_set: list, final_set_size: int):
        """
        Calculates pair-wise diversity of the recommendation
        set and filters
        :param recommendation_set: a set of items recommended by the hybrid recommender system
        :param final_set_size: a desired size of the diverse recommendation set
        :return: a filtered recommendation set that contains the most diverse items
        """

        raise NotImplementedError
