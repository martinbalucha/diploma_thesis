from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from googletrans import Translator
from typing import List


class Preprocessor:
    """
    A preprocessor for the content-based recommender service
    """

    stemmer: PorterStemmer
    translator: Translator

    def __init__(self, stemmer: PorterStemmer, translator: Translator):
        """
        Ctor
        :param stemmer: the word stemmer
        :param translator: the tool used for translation from other
        languages to English
        """

        self.stemmer = stemmer
        self.translator = translator

    def preprocess_string(self, input_string: str, input_language: str = "english") -> List[str]:
        """
        Performs stop-word removal, translation and stemming on the input string
        :param input_string: Input string that is to be pre-processed
        :param input_language: An optional parameter of the input language.
        The default value is set to 'english'
        :return: A list of stemmed words that are not stop-words
        """

        processed_words = []
        input_words = word_tokenize(input_string, input_language)
        stop_words = stopwords.words(input_language)

        for word in input_words:
            if word not in stop_words:
                stemmed_word = self.stemmer.stem(word)
                processed_words.append(stemmed_word)

        return processed_words

    def _add_toc_specific_stop_words(self, stop_words: dict) -> None:
        """
        Adds additional stop-words to the dictionary. These stop-words
        are specific for the tables of contents. Examples of such words are
        'page', 'bibliography' and 'index'
        :param stop_words:
        """

        pass
