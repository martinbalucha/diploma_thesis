import Preprocessor
from Persistence.Entities import BookDao
from typing import List
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommenderService:
    """
    A service class that performs content-based recommendations
    """

    preprocessor: Preprocessor
    count_vectorizer: CountVectorizer
    book_dao: BookDao

    def __init__(self, preprocessor: Preprocessor, book_dao: BookDao, count_vectorizer: CountVectorizer):
        """
        Ctor
        :param preprocessor: content pre-processor
        :param book_dao: data access object for books
        :param count_vectorizer: count vectorizer
        """

        self.preprocessor = preprocessor
        self.book_dao = book_dao
        self.count_vectorizer = count_vectorizer

    def recommend(self, count: int) -> List[int]:
        """
        Performs content-based filtering
        :param count: the number of closest books that will be returned
        :return: 
        """

        features = ["title", "table_of_contents", "description", "author"]
        books = self.book_dao.get_books()
