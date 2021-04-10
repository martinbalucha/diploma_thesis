import random
import numpy
import pandas
from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from persistence.dao.book_dao import BookDao
from service.i_preprocessor import IPreprocessor
from service.i_recommender_service import IRecommenderService


class ContentBasedRecommenderService(IRecommenderService):
    """
    A service class that performs content-based recommendations. Implements IRecommenderService
    """

    _preprocessor: IPreprocessor
    _tfidf_vectorizer: TfidfVectorizer
    _book_dao: BookDao

    def __init__(self, preprocessor: IPreprocessor, book_dao: BookDao, tfidf_vectorizer: TfidfVectorizer):
        """
        Ctor
        :param preprocessor: content pre-processor
        :param book_dao: data access object for books
        :param tfidf_vectorizer: TF-IDF vectorizer
        """

        self._preprocessor = preprocessor
        self._book_dao = book_dao
        self._tfidf_vectorizer = tfidf_vectorizer

    def recommend(self, user_id: int, count: int) -> DataFrame:
        best_rated_books = self._book_dao.get_best_rated_books(user_id)
        if len(best_rated_books.index) == 0:
            return best_rated_books

        selected_best_books, topics = self._select_best_rated_books(best_rated_books, 3)
        books = self._book_dao.find_candidate_books(user_id, topics)
        books = books.append(selected_best_books)
        best_rated_books_ids = best_rated_books.set_index("id").T.to_dict("list")

        books = self._preprocessor.preprocess(books)
        tfidf_matrix = self._tfidf_vectorizer.fit_transform(books["bagOfWords"])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        recommendations = {}
        selected_best_books_count = len(selected_best_books)
        similar_per_book = count // selected_best_books_count

        for i in range(selected_best_books_count):
            book = selected_best_books[i]
            if i == selected_best_books_count - 1:
                similar_per_book += count % selected_best_books_count
            index = self._get_index_from_id(books, book["id"])
            similarity_scores = list(enumerate(cosine_similarities[index]))
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            self._select_similar_books(similarity_scores, books, best_rated_books_ids, similar_per_book,
                                       recommendations)

        result_df = pandas.DataFrame.from_dict(recommendations, orient="index")
        return result_df

    def _select_similar_books(self, similarity_scores: list, books: DataFrame, best_rated_books: dict, count: int,
                              recommendations: dict) -> None:
        """
        Selects the most similar books to the one with the given ID and appends them
        to the result dataframe
        :param similarity_scores: a list of similarity scores books
        :param best_rated_books: a dictionary of books that were originally selected
        :param count: a number of similar books that are to be selected.
        :param recommendations: a dictionary with recommended books
        """

        books_selected = 0
        for book_index in similarity_scores:
            candidate_book = books.iloc[book_index[0]]
            candidate_book_id = candidate_book["id"]
            if candidate_book_id not in best_rated_books and candidate_book_id not in recommendations:
                recommendations[candidate_book_id] = candidate_book
                books_selected += 1
            if books_selected >= count:
                return

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
            topics_id = books["topic"].values.tolist()
            return selected_books, topics_id

        for i in range(count):
            book_index = random.randint(0, len(books.index) - 1)
            book = books.iloc[book_index]
            selected_books.append(book)
            topics_id.append(numpy.uint64(book["topic"]).item())
            books = books[books.id != book["id"]]
        return selected_books, topics_id

    def _get_index_from_id(self, data_frame: DataFrame, book_id: int) -> int:
        """
        Gets index of the book with the given id
        :param data_frame: dataframe with books
        :param book_id: id of the sought item
        :return: index of the book with given ID
        """

        return data_frame.index[data_frame["id"] == book_id].values[0]
