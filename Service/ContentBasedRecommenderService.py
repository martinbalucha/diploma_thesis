import random
import numpy
from pandas import DataFrame
from Persistence.Dao import BookDao
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from Service import IPreprocessor
from Service.IRecommenderService import IRecommenderService
from Service.Utils.DataframeUtils import get_index_from_id


class ContentBasedRecommenderService(IRecommenderService):
    """
    A service class that performs content-based recommendations. Implements IRecommenderService
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

    def recommend(self, user_id: int, count: int) -> DataFrame:
        best_rated_books = self.book_dao.get_best_rated_books(user_id)
        selected_best_books, topics = self._select_best_rated_books(best_rated_books, 5)
        books = self.book_dao.find_candidate_books(user_id, topics)
        books = books.append(selected_best_books)

        books = self.preprocessor.preprocess(books)
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(books["bagOfWords"])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        recommendations = DataFrame(columns=books.columns)
        selected_best_books_count = len(selected_best_books)
        similar_per_book = count // selected_best_books_count

        for i in range(selected_best_books_count):
            book = selected_best_books[i]

            if i == selected_best_books_count - 1:
                similar_per_book += count % selected_best_books_count

            recommendations = self._select_similar_books(cosine_similarities, books, book["id"],
                                                         similar_per_book, recommendations)

        return recommendations

    def _select_similar_books(self, similarities: numpy.ndarray, books: DataFrame, book_id: int, count: int,
                              recommendations: DataFrame) -> DataFrame:
        """
        Selects the most similar books to the one with the given ID and appends them
        to the result dataframe
        :param similarities: a matrix of cosine similarities
        :param book_id: an ID of a book for which similar ones will be found
        :param count: a number of similar books that are to be selected.
        :param recommendations: a dataframe with recommended books
        :return: dataframe filled with recommended books
        """

        index = get_index_from_id(books, book_id)
        similarity_scores = list(enumerate(similarities[index]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        most_similar_books = similarity_scores[1:count + 1]

        for similar_book in most_similar_books:
            recommended = books.iloc[similar_book[0]]
            recommendations = recommendations.append(recommended)

        return recommendations

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
