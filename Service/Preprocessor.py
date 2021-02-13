from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from typing import List


class Preprocessor:
    """
    A preprocessor for the content-based recommender service
    """

    def preprocess_string(self, input_string: str, input_language: str) -> List[str]:
        """
        Performs stop-word removal and stemming on the input string
        :param input_string: Input string that is to be pre-processed
        :param input_language: A language of the input
        :return: A list of stemmed words that are not stop-words
        """

        processed_words = []
        stemmer = PorterStemmer()
        input_words = word_tokenize(input_string, input_language)
        stop_words = stopwords.words(input_language)

        for word in input_words:
            if word not in stop_words:
                stemmed_word = stemmer.stem(word)
                processed_words.append(stemmed_word)

        return processed_words
