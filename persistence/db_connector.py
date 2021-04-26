import psycopg2
from configparser import ConfigParser


config = ConfigParser()
config.read("config.ini")


def create_connection():
    """
    Creates connection to the database. The connection must
    be closed after it is no longer used!
    :return: a connection to the database.
    """

    host = config["postgresDb"]["host"]
    database = config["postgresDb"]["database"]
    user = config["postgresDb"]["user"]
    password = config["postgresDb"]["password"]

    connection = psycopg2.connect(host=host, database=database, user=user, password=password)
    return connection
