import random
from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from service.i_diverse_selection_service import IDiverseSelectionService


class DiverseSelectionService(IDiverseSelectionService):
    """
    Implements IDiversityService interface
    """

    _tfidf_vectorizer: TfidfVectorizer

    def __init__(self, tfidf_vectorizer: TfidfVectorizer):
        """
        Ctor
        :param tfidf_vectorizer: TF-IDF vectorizer
        """

        self._tfidf_vectorizer = tfidf_vectorizer

    def diversify(self, recommended_books: DataFrame, final_set_size: int) -> DataFrame:
        result = DataFrame(columns=recommended_books.columns[:-2])
        if len(recommended_books.index) == 0:
            return result

        tfidf_matrix = self._tfidf_vectorizer.fit_transform(recommended_books["topicName"])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        selected_book_index = random.randint(0, len(recommended_books.index) - 1)
        first_item = recommended_books.iloc[selected_book_index]
        result = result.append(first_item)
        book_ids = recommended_books["id"]

        for i in range(final_set_size - 1):
            already_picked_books = result["id"].tolist()
            least_similar_index = self._pick_least_similar(selected_book_index, cosine_similarities,
                                                           already_picked_books, book_ids)

            least_similar_book = recommended_books.iloc[least_similar_index]
            result = result.append(least_similar_book)

        return result

    def _pick_least_similar(self, book_index: int, cosine_similarities: list, selected_books: list,
                            recommended_books: DataFrame) -> int:
        """
        Picks the least similar item from the list that has not yet been selected.
        :param book_index: Index of a book for which the least similar counterpart will be found
        :param cosine_similarities: a matrix of similarity scores for each book
        :param selected_books: a list of already selected books' ids
        :param recommended_books: a dataframe of books recommended by the filtering algorithms
        :return: the least similar book that has not yet been selected. If all books have been selected,
        -1 will be returned - this scenario should not occur, though
        """

        similarity_scores = list(enumerate(cosine_similarities[book_index]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1])
        for similar_book in similarity_scores:
            index = similar_book[0]
            book_id = recommended_books.iloc[index]
            if book_id not in selected_books:
                return similar_book[0]

        return -1
