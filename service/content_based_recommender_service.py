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

        pick_per_one_rated = 2
        rated_books_to_pick = count // pick_per_one_rated
        selected_best_books, topics = self._select_best_rated_books(best_rated_books, rated_books_to_pick)
        books = self._book_dao.find_candidate_books(user_id, topics)
        books = books.append(selected_best_books)
        best_rated_books_ids = best_rated_books.set_index("id").T.to_dict("list")

        books = self._preprocessor.preprocess(books)
        cosine_similarities = self._calculate_similarities(books, books.tail(rated_books_to_pick))

        recommendations = {}
        selected_best_books_count = len(selected_best_books)
        similar_per_book = pick_per_one_rated

        for i in range(rated_books_to_pick):
            # book = selected_best_books[i]
            if i == selected_best_books_count - 1:
                similar_per_book += count % selected_best_books_count
            similarity_scores = list(enumerate(cosine_similarities[i]))
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            self._select_similar_books(similarity_scores, books, best_rated_books_ids, similar_per_book,
                                       recommendations)

        result_df = pandas.DataFrame.from_dict(recommendations, orient="index")
        return result_df

    def _calculate_similarities(self, candidate_books: DataFrame, rated_books: DataFrame):
        """
        Calculates tf-idf for books and calculates cosine similarity between selected rated books.
        Rated books have to be first fit into the vector space of all words and then
        :param candidate_books:
        :param rated_books:
        :return:
        """

        tfidf_matrix_candidate = self._tfidf_vectorizer.fit_transform(candidate_books["bagOfWords"])
        tfidf_matrix_rated = self._tfidf_vectorizer.fit(candidate_books["bagOfWords"])
        tfidf_matrix_rated = tfidf_matrix_rated.transform(rated_books["bagOfWords"])
        return linear_kernel(tfidf_matrix_rated, tfidf_matrix_candidate)

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
            count = len(books.index)

        for i in range(count):
            book_index = random.randint(0, len(books.index) - 1)
            book = books.iloc[book_index]
            selected_books.append(book)
            topics_id.append(numpy.uint64(book["topic"]).item())
            books = books[books.id != book["id"]]
        return selected_books, topics_id
