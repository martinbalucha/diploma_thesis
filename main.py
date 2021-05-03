#!/usr/bin/env python

from web_app import app

if __name__ == "__main__":
    # nltk.download("stopwords")
    # nltk.download("punkt")
    #evaluate()
    app.run(debug=True, port=8080)
