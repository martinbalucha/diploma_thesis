import swifter
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from pandas import Series, DataFrame
from service.i_preprocessor import IPreprocessor


class Preprocessor(IPreprocessor):
    """
    A preprocessor for the content-based recommender service
    """

    _stemmer: PorterStemmer
    _stop_words: set

    def __init__(self, stemmer: PorterStemmer, stop_words: set):
        """
        Ctor
        :param stemmer: the word stemmer
        :param stop_words: a set of English stop-words
        languages to English
        """

        self._stemmer = stemmer
        self._stop_words = stop_words
        self._build_stop_word_dict()

    def _preprocess(self, book: Series) -> str:
        """
        Pre-processes the bag of words
        :param book: a row with book information
        :return: pre-processed book's bag of words
        """

        lowercase_string = str(book["bagOfWords"]).lower()
        words = word_tokenize(lowercase_string)
        preprocessed_words = self._stem_and_remove_stop_words(words)
        separator = " "
        return separator.join(preprocessed_words)

    def preprocess(self, data_frame: DataFrame) -> DataFrame:
        data_frame.reset_index(drop=True, inplace=True)
        data_frame["authorName"] = data_frame.swifter.apply(self._adjust_author_name, axis=1)
        data_frame["bagOfWords"] = data_frame.swifter.apply(self._build_features, axis=1)
        data_frame["bagOfWords"] = data_frame.swifter.apply(self._preprocess, axis=1)
        return data_frame

    def _adjust_author_name(self, book: Series) -> str:
        """
        Removes spaces from author name. The idea is match prevent false similarities
        between books whose authors have the same first name, e.g. James Burnham and James Baldwin.
        By removing spaces, first name and surname are joined and treated as one words.
        :param book: a row containing information about the book
        :return: joined first name and surname of the author
        """

        author = str(book["author"])
        return author.replace(" ", "")

    def _stem_and_remove_stop_words(self, words: list) -> list:
        """
        Removes stop-words from bag of words
        :param words: a list of words that are to be cleared
        :return: a bag of words cleared of any stop-words
        """

        filtered_words = []
        for word in words:
            if word not in self._stop_words:
                stemmed_word = self._stemmer.stem(word)
                if len(stemmed_word) > 2:
                    filtered_words.append(stemmed_word)
        return filtered_words

    def _build_stop_word_dict(self) -> None:
        """
        Adds additional stop-words to the standard dictionary. These stop-words
        are specific for the tables of contents. Examples of such words are
        'page', 'bibliography' and 'index' but also HTML elements like <br>
        """

        additional_words = ["page", "index", "bibliography", "br", "/br", "copyright", "\'s", "...", "\\\\", "......",
                            "preface", "postscript", "endnotes", "credits", "front cover", "epigraph",
                            "edition", "appendix"]

        for stop_word in additional_words:
            self._stop_words.add(stop_word)

    def _build_features(self, book: Series) -> str:
        """
        Combines all features used in content-based filtering
        :return: combined feature of the book
        """

        return (book["title"] + " " + book["authorName"] + " " + book["description"] + " "
                + book["tableOfContents"] + " " + book["topicName"])