import ray
import nltk
from googletrans import Translator
from nltk import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from surprise import SVD
from Persistence.Dao.BookDao import BookDao
from Persistence.Dao.RatingDao import RatingDao
from Service.DiversityService import DiversityService
from Service.ContentBasedRecommenderService import ContentBasedRecommenderService
from Service.HybridRecommenderService import HybridRecommenderService
from Service.MatrixFactorizationService import MatrixFactorizationService
from Service.Preprocessor import Preprocessor


def main():
    """
    Launches the application
    """

    preprocessor = Preprocessor(PorterStemmer(), Translator())
    vectorizer = TfidfVectorizer()
    content_based = ContentBasedRecommenderService(preprocessor, BookDao(), vectorizer)
    matrix_factorization = MatrixFactorizationService(SVD(), RatingDao())
    diversity_service = DiversityService()
    recommender_service = HybridRecommenderService(content_based, matrix_factorization, diversity_service)
    kek = content_based.recommend(320562, 10)

if __name__ == "__main__":
    nltk.download("stopwords")
    nltk.download("punkt")
    ray.init()
    main()
