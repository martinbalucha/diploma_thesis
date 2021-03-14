import random

import numpy
import swifter
from modin.pandas import Series
from pandas import DataFrame
from Persistence.Dao import BookDao
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from Service import Preprocessor


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

    def recommend(self, user_id: int, count: int,) -> List[int]:
        """
        Performs content-based filtering
        :param user_id: ID of the target user
        :param count: the number of closest books that will be returned
        :return: 
        """

        best_rated_books = self.book_dao.get_best_rated_books(user_id)
        tmp = self._select_best_rated_books(best_rated_books, 10)
        selected_best_books = tmp[0]
        topics = tmp[1]

        books = self.book_dao.find_candidate_books(user_id, topics)
        books = books.append(selected_best_books)

        books = self.preprocessor.preprocess(books)

        tfidf_matrix = self.tfidf_vectorizer.fit_transform(books["bagOfWords"])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        recommendations = []
        for book in selected_best_books:
            index = self._get_index_from_id(books, book["id"])
            similarity_scores = list(enumerate(cosine_similarities[index]))
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            most_similar_books = similarity_scores[1:3]
            recommended = self._get_book_by_index(books, most_similar_books[0][0])
            recommendations.append(recommended)

        return recommendations

    def _get_recommendations(self, cosine_similarities, count: int):
        """

        :param cosine_similarities:
        :param count:
        :return:
        """

        pass

    def _select_best_rated_books(self, books: DataFrame, count: int) -> tuple:
        """
        Randomly selects n books
        :param books: a dataframe with books
        :param count: a number of books that are to be selected
        :return: a tuple of  of randomly selected books' ids and their topics
        """

        selected_books = []
        topics_id = []
        if len(books.index) < count:
            selected_books = books["bookId"].values.tolist()
            topics_id = books["metaTopic"].values.tolist()
            return selected_books, topics_id

        for i in range(count):
            book_index = random.randint(0, len(books.index) - 1)
            book = books.iloc[book_index, :-1]
            selected_books.append(book)
            meta_topic_id = books.iloc[book_index, -1]
            topics_id.append(numpy.uint64(meta_topic_id).item())
            books = books[books.id != book["id"]]
        return selected_books, topics_id

    def _get_book_by_index(self, data_frame: DataFrame, index: int) -> Series:
        """
        Gets book by the given index
        :param data_frame: dataframe with books
        :param index: an index of the wanted book
        :return: data row with book information
        """

        return data_frame.iloc[index]

    def _get_index_from_id(self, data_frame: DataFrame, book_id: int) -> int:
        """
        Gets index of the book with the given id
        :param data_frame: dataframe with books
        :param book_id: id of the sought book
        :return: index of the book with given ID
        """

        return data_frame.index[data_frame["id"] == book_id].values[0]
