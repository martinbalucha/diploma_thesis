from typing import List


class User:
    """
    A class representing registered user
    in the book recommender system
    """

    id: int
    login: str
    password_hash: str
    languages_spoken: List
