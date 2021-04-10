import numpy as np
import psycopg2
from psycopg2 import extras
from psycopg2.extensions import register_adapter, AsIs

from persistence import db_connector
from web_app import app
import pandas as pd

def insert_ratings():
    register_adapter(np.int64, psycopg2. _psycopg.AsIs)
    chunkReader = pd.read_csv("D:/Skola/Diplomka/Book reviews/large_goodreads_dataset/goodreads_interactions.csv",
                              sep=",", chunksize=500000)
    query = "INSERT INTO ratings_tmp (%s) VALUES %%s" % """ "userId", "bookId", rating"""
    with db_connector.create_connection() as connection:
        with connection.cursor() as cursor:
            for chunk in chunkReader:
                picked = chunk[chunk["rating"] != 0]
                tmp = picked[["user_id", "book_id", "rating"]]
                tuples = [tuple(x) for x in tmp.to_numpy()]
                extras.execute_values(cursor, query, tuples)
        connection.commit()

if __name__ == "__main__":
    #nltk.download("stopwords")
    #nltk.download("punkt")
    #app.run(debug=True, port=8080)
    insert_ratings()
