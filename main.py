from web_app import app
from evaluate.accuracy_metric import evaluate, grid_search

if __name__ == "__main__":
    # nltk.download("stopwords")
    # nltk.download("punkt")
    # grid_search()
    app.run(debug=True, port=8080)
