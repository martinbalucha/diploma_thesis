

def rated_books_query() -> str:
    """
    Creates the query for rated books
    :return: query for rated books
    """

    query = """SELECT b.*, r.rating, t.name as "topicName"
                FROM book b INNER JOIN rating r ON b.id = r."bookId"
                INNER JOIN topic t on b.topic = t.id
                WHERE r."userId" = %s ORDER BY r.rating, b.title LIMIT %s OFFSET %s"""

    return query


def rated_books_count_query() -> str:
    """
    Creates the query for count of rated books by the given user
    :return: query for count of rated books by the target user
    """

    query = """SELECT COUNT(*) AS count FROM book b INNER JOIN rating r ON b.id = r."bookId"
                INNER JOIN topic t on b.topic = t.id
                WHERE r."userId" = %s"""

    return query


def find_books_query() -> str:
    """
    Creates the query for finding book by title, author and topic
    :return: query for findings books by title, author and topic
    """

    query = """SELECT book.*, t.name as "topicName" FROM book INNER JOIN topic t on book.topic = t.id
                WHERE title ILIKE COALESCE(%s, title)
                AND author ILIKE COALESCE(%s, author)
                ORDER BY book.title, book.author LIMIT %s OFFSET %s"""

    return query


def find_books_count_query() -> str:
    """
    Creates the query for counting books satisfying given criteria
    :return: query for counting books satisfying given criteria
    """

    query = """SELECT COUNT(*) as count FROM book INNER JOIN topic t on book.topic = t.id
                WHERE title ILIKE COALESCE(%s, title)
                AND author ILIKE COALESCE(%s, author)"""

    return query


def find_user_by_id_query() -> str:
    """
    Creates the query for retrieving user by ID
    :return: query for retrieving user by ID
    """
    query = """SELECT id, username FROM registered_user WHERE id = %s"""
    return query


def find_user_by_login_query() -> str:
    """
    Creates the query for retrieving user by ID
    :return:
    """

    query = """SELECT id, username, "passwordHash" FROM registered_user WHERE username = %s"""
    return query


def insert_user_query() -> str:
    """
    Creates the query for user insert
    :return: query for user insert
    """

    query = """INSERT INTO registered_user (username, "passwordHash") VALUES (%s, %s)"""
    return query


def update_rating_query() -> str:
    """
    Creates the query for rating update
    :return: query for rating update
    """

    query = """UPDATE rating SET rating = %s WHERE "bookId" = %s AND "userId" = %s"""
    return query


def insert_rating_query() -> str:
    """
    Creates the query for rating insert
    :return: query for rating insert
    """

    query = """INSERT INTO rating ("bookId", "userId", rating) VALUES (%s, %s, %s)"""
    return query


def user_item_matrix_query() -> str:
    """
    Creates the query for user-item matrix
    :return: query for user-item matrix
    """

    query = """SELECT "userId", "bookId", rating FROM rating LEFT JOIN book ON book.id = rating."bookId" """
    return query


def find_candidate_books_query() -> str:
    """
    Creates the query for retrieving books that will be filtered by content
    :return: query for retrieving books that will be filtered by content
    """

    query = """SELECT DISTINCT b.*, t.name as "topicName" FROM book b
                INNER JOIN topic t ON t.id = b.topic
                WHERE b.id NOT IN (SELECT "bookId" FROM rating WHERE "userId" = %s)
                AND t.id IN %s"""

    return query


def find_book_by_id_query() -> str:
    """
    Creates the query for book retrieval by ID
    :return: query for book retrieval by ID
    """

    query = """SELECT b.id, b.author, b.title, b.year, b.pages, b."tableOfContents",
                      b.isbn, b.description, t.name AS "topicName", r.rating, stat.average, stat."ratingCount"
                FROM book b
                INNER JOIN topic t ON t.id = b.topic
                LEFT JOIN rating r ON r."bookId" = b.id AND r."userId" = %s
                LEFT JOIN (SELECT "bookId", COUNT(*) AS "ratingCount", ROUND(AVG(rating), 2) as average FROM rating 
                            GROUP BY "bookId") stat ON b.id = stat."bookId"
                WHERE b.id = %s"""

    return query


def get_best_rated_books_query() -> str:
    """
    Creates the query for retrieval of books rated by three or more stars by the target user
    :return: query for retrieval of books rated by three or more stars by the target user
    """

    query = """SELECT b.*, t.name as "topicName" FROM rating r
                INNER JOIN book b ON b.id = r."bookId"
                INNER JOIN topic t ON t.id = b.topic
                WHERE "userId" = %s AND rating >= 3 ORDER BY r.rating DESC"""

    return query


def get_candidate_books_collaborative() -> str:
    """
    Creates the query for retrieval of books that could be recommended by the collaborative filtering
    :return: query for retrieval of books that could be recommended by the collaborative filtering
    """

    query = """SELECT b.*, t.name as "topicName" FROM book b 
                INNER JOIN topic t on b.topic = t.id
                WHERE b.id IN (SELECT "bookId" FROM rating WHERE "userId" != %s
                                GROUP BY "bookId" HAVING COUNT(*) > 10)"""

    return query
