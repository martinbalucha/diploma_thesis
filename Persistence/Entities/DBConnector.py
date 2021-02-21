import psycopg2


def create_connection():
    """
    Creates connection to the database. The connection must
    be closed after it is no longer used!
    :return: a connection to the database.
    """

    connection = psycopg2.connect()
    return connection
