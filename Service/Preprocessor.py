from nltk.stem import PorterStemmer
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

    def preprocess_string(self, word: str, input_language: str = "english") -> List[str]:
        """
        Performs translation and stemming on the input string
        :param word: Input string that is to be pre-processed
        :param input_language: An optional parameter of the input language.
        The default value is set to 'english'
        :return: Stem of the translated input word
        """

        lower_word = word.lower()
        if input_language != "english":
            lower_word = self.translator.translate(lower_word, src=input_language)
        return self.stemmer.stem(lower_word)

    def _add_toc_specific_stop_words(self, stop_words: dict) -> None:
        """
        Adds additional stop-words to the dictionary. These stop-words
        are specific for the tables of contents. Examples of such words are
        'page', 'bibliography' and 'index'
        :param stop_words:
        """

        pass
