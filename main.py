#!/usr/bin/env python

from web_app import app
from evaluate.accuracy_metric import evaluate, grid_search

__author__ = "Martin Balucha"
__copyright__ = "Copyright (c) 2021, Martin Balucha"
__credits__ = ["Martin Balucha"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Rob Knight"
__email__ = "rob@spot.colorado.edu"
__status__ = "Production"

if __name__ == "__main__":
    # nltk.download("stopwords")
    # nltk.download("punkt")
    # grid_search()
    app.run(debug=True, port=8080)
