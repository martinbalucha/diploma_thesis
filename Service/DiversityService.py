import random
from Service.IDiversityService import IDiversityService


class DiversityService(IDiversityService):
    """
    Implements IDiversityService interface
    """

    def diversify(self, recommendation_set: list, final_set_size: int):
        result_set = []
        first_pick_index = random.randint(0, len(recommendation_set) - 1)
        first_item = recommendation_set[first_pick_index]
        result_set.append(first_item)

        for i in range(final_set_size - 1):
            pass
