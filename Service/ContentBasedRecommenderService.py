import Preprocessor
from typing import List
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommenderService:
    """
    A service class that performs content-based recommendations
    """

    preprocessor: Preprocessor

    def __init__(self, preprocessor: Preprocessor):
        """
        Ctor
        :param preprocessor: content pre-processor
        """

        self.preprocessor = preprocessor

    def recommend(self, count: int) -> List[int]:
        """
        Performs content-based filtering
        :param count: the number of closest books that will be returned
        :return: 
        """


        count_vectorizer = CountVectorizer()




