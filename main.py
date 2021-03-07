from io import StringIO
import pandas
from psycopg2 import extras

from Persistence import DBConnector


def main():
    pass

def adjustRating(row):
    rating = row["Book-Rating"]
    return int(round(rating / 2))

def create_adjusted_file():
    ratings = pandas.read_csv("d:/Skola/Diplomka/Book reviews/BX-Book-Ratings.csv", delimiter=";")
    ratings['rating'] = ratings.swifter.apply(adjustRating, axis=1)
    ratings.pop('Book-Rating')

    tuples = [tuple(x) for x in ratings.to_numpy()]
    query = "INSERT INTO %s (%s) VALUES %%s" % ("ratings_tmp", "user_id, ISBN, rating")
    connection = DBConnector.create_connection()
    cursor = connection.cursor()
    extras.execute_values(cursor, query, tuples)
    connection.commit()

    cursor.close()
    connection.close()

def create_final_ratings_csv():
    query = """SELECT b.id, r.user_id, r.rating
                FROM ratings_tmp r
                INNER JOIN (SELECT title, id, isbn FROM book WHERE isbn != '' AND isbn != ',') b
                ON b.isbn LIKE '%' || r.isbn || '%'"""

    ratings = pandas.read_sql(query, con=DBConnector.create_connection())
    ratings.to_csv("ratings_final_zero.csv")

def remove_duplicate(row):
    pass

def insert_ratings():
    ratings = pandas.read_csv("ratings_final.csv", delimiter=",", index_col=0)
    duplicateRowsDF = ratings[ratings.duplicated(['id', 'user_id'])]
    indices = duplicateRowsDF.index.values.tolist()
    ratings = ratings.drop(indices)
    ratings.rename(columns={"id": '"bookId"', "user_id": '"userId"'}, inplace=True)

    # Initialize a string buffer
    sio = StringIO()
    sio.write(ratings.to_csv(index=None, header=None))  # Write the Pandas DataFrame as a csv to the buffer
    sio.seek(0)  # Be sure to reset the position to the start of the stream

    connection = DBConnector.create_connection()
    cursor = connection.cursor()
    cursor.copy_from(sio, "rating", columns=ratings.columns, sep=',')
    connection.commit()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_final_ratings_csv()
