import Preprocessor
from pandas import DataFrame
from Persistence.Dao import BookDao
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class ContentBasedRecommenderService:
    """
    A service class that performs content-based recommendations
    """

    preprocessor: Preprocessor
    tfidf_vectorizer: TfidfVectorizer
    book_dao: BookDao

    def __init__(self, preprocessor: Preprocessor, book_dao: BookDao, tfidf_vectorizer: TfidfVectorizer):
        """
        Ctor
        :param preprocessor: content pre-processor
        :param book_dao: data access object for books
        :param tfidf_vectorizer: TF-IDF vectorizer
        """

        self.preprocessor = preprocessor
        self.book_dao = book_dao
        self.tfidf_vectorizer = tfidf_vectorizer

    def recommend(self, count: int) -> List[int]:
        """
        Performs content-based filtering
        :param count: the number of closest books that will be returned
        :return: 
        """

        features = ["title", "tableOfContents", "description", "author"]
        books = self.book_dao.get_books()
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(books["tableOfContents"])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    def _build_features(self, books: DataFrame) -> None:
        """
        Adjusts loaded dataframe
        :param books: a dataframe with books
        :return:
        """
        pass


