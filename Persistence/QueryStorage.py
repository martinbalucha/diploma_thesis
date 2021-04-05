

def rated_books_query() -> str:
    """
    Creates query for rated books
    :return: query for rated books
    """

    query = """SELECT b.*, r.rating, t.name as "topicName"
                FROM book b INNER JOIN rating r ON b.id = r."bookId"
                INNER JOIN topic t on b.topic = t.id
                WHERE r."userId" = %s ORDER BY r.rating, b.title LIMIT %s OFFSET %s"""

    return query


def rated_books_count_query() -> str:
    """
    Creates query for count of rated books by the given user
    :return: query for count of rated books by the target user
    """

    query = """SELECT COUNT(*) AS count FROM book b INNER JOIN rating r ON b.id = r."bookId"
                INNER JOIN topic t on b.topic = t.id
                WHERE r."userId" = %s"""

    return query


def find_books_query() -> str:
    """
    Creates query for finding book by title, author and topic
    :return: query for findings books by title, author and topic
    """

    query = """SELECT book.*, t.name as "topicName" FROM book INNER JOIN topic t on book.topic = t.id
                WHERE title ILIKE COALESCE(%s, title)
                AND author ILIKE COALESCE(%s, author)
                ORDER BY book.title, book.author LIMIT %s OFFSET %s"""

    return query


def find_books_count_query() -> str:
    """
    Creates query for counting books satisfying given criteria
    :return: query for counting books satisfying given criteria
    """

    query = """SELECT COUNT(*) as count FROM book INNER JOIN topic t on book.topic = t.id
                WHERE title ILIKE COALESCE(%s, title)
                AND author ILIKE COALESCE(%s, author)"""

    return query


def find_user_by_id_query() -> str:
    """
    Creates query for retrieving user by ID
    :return: query for retrieving user by ID
    """
    query = """SELECT id, username FROM registered_user WHERE id = %s"""
    return query


def find_user_by_login_query() -> str:
    """
    Creates query for retrieving user by ID
    :return:
    """

    query = """SELECT id, username, "passwordHash" FROM registered_user WHERE username = %s"""
    return query


def insert_user_query() -> str:
    """
    Creates query for user insert
    :return: query for user insert
    """

    query = """INSERT INTO registered_user (username, "passwordHash") VALUES (%s, %s)"""
    return query


def update_rating_query() -> str:
    """
    Creates query for rating update
    :return: query for rating update
    """

    query = """UPDATE rating SET rating = %s WHERE "bookId" = %s AND "userId" = %s"""
    return query


def insert_rating_query() -> str:
    """
    Creates query for rating insert
    :return: query for rating insert
    """

    query = """INSERT INTO rating ("bookId", "userId", rating) VALUES (%s, %s, %s)"""
    return query


def user_item_matrix_query() -> str:
    """
    Creates query for user-item matrix
    :return: query for user-item matrix
    """

    query = """SELECT "userId", "bookId", rating FROM rating LEFT JOIN book ON book.id = rating."bookId"
                WHERE book.language = 1"""

    return query
