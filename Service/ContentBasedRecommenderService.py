import random
import numpy
from modin.pandas import Series
from pandas import DataFrame
from Persistence.Dao import BookDao
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from Service import IPreprocessor
from Service.IRecommenderService import IRecommenderService


class ContentBasedRecommenderService(IRecommenderService):
    """
    A service class that performs content-based recommendations
    """

    preprocessor: IPreprocessor
    tfidf_vectorizer: TfidfVectorizer
    book_dao: BookDao

    def __init__(self, preprocessor: IPreprocessor, book_dao: BookDao, tfidf_vectorizer: TfidfVectorizer):
        """
        Ctor
        :param preprocessor: content pre-processor
        :param book_dao: data access object for books
        :param tfidf_vectorizer: TF-IDF vectorizer
        """

        self.preprocessor = preprocessor
        self.book_dao = book_dao
        self.tfidf_vectorizer = tfidf_vectorizer

    def recommend(self, user_id: int, count: int) -> list:
        best_rated_books = self.book_dao.get_best_rated_books(user_id)
        selected_best_books, topics = self._select_best_rated_books(best_rated_books, 5)
        books = self.book_dao.find_candidate_books(user_id, topics)
        books = books.append(selected_best_books)

        books = self.preprocessor.preprocess(books)
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(books["bagOfWords"])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        recommendations = []
        selected_best_books_count = len(selected_best_books)
        similar_per_book = count // selected_best_books_count

        for i in range(selected_best_books_count):
            book = selected_best_books[i]

            if i == selected_best_books_count - 1:
                similar_per_book += count % selected_best_books_count

            most_similar_books = self._select_similar_books(cosine_similarities, books, book["id"], similar_per_book)
            recommendations.extend(most_similar_books)

        return recommendations

    def _select_similar_books(self, similarities: numpy.ndarray, books: DataFrame, book_id: int, count: int) -> list:
        """
        Selects the most similar books to the one with the given ID.
        :param similarities: a matrix of cosine similarities
        :param book_id: an ID of a book for which similar ones will be found
        :param count: a number of similar books that are to be selected.
        :return: A list of similar books
        """

        recommendations = []
        index = self._get_index_from_id(books, book_id)
        similarity_scores = list(enumerate(similarities[index]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        most_similar_books = similarity_scores[1:count + 1]

        for similar_book in most_similar_books:
            recommended = self._get_book_by_index(books, similar_book[0])
            recommendations.append(recommended)

        return recommendations

    def _adjust_recommendations_per_book(self, selected_book_count: int, required_count: int) -> int:
        """
        Adjusts the number of selected similar books per one read book. This is needed if the target
        user has read fewer books than it was passed to method _select_best_rated_books in the parameter
        count.
        :param selected_book_count: a number of selected books rated by the user
        :param required_count: a number of books that should be recommended
        :return:
        """

        books_per_one = required_count // selected_book_count
        return books_per_one

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
