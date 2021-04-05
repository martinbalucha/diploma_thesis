

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
