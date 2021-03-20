import random

from sklearn.feature_extraction.text import TfidfVectorizer

from Service.IDiversityService import IDiversityService


class DiversityService(IDiversityService):
    """
    Implements IDiversityService interface
    """

    tfidf_vectorizer: TfidfVectorizer

    def __init__(self, tfidf_vectorizer: TfidfVectorizer):
        """
        Ctor
        :param tfidf_vectorizer: TF-IDF vectorizer
        """

        self.tfidf_vectorizer = tfidf_vectorizer

    def diversify(self, recommendation_set: list, final_set_size: int):
        result_set = []
        first_pick_index = random.randint(0, len(recommendation_set) - 1)
        first_item = recommendation_set[first_pick_index]
        result_set.append(first_item)

        for i in range(final_set_size - 1):
            pass
