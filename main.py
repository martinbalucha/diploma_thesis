#!/usr/bin/env python

from web_app import app
from evaluate.accuracy_metric import evaluate, grid_search, grid_search_epochs

if __name__ == "__main__":
    # nltk.download("stopwords")
    # nltk.download("punkt")
    #evaluate()
    app.run(debug=True, port=8080)
