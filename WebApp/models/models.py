from flask_login import UserMixin


class User(UserMixin):
    """
    A class representing user in the system. Inspired by:
    https://github.com/maxcountryman/flask-login/blob/main/test_login.py
    """

    def __init__(self, name: str, user_id: int, active: bool=True):
        """

        :param name: a name of the user
        :param user_id: an ID of the user
        :param active: a bool value indicating whether the user is active or not
        """

        self.id = user_id
        self.name = name
        self.active = active

    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return self.active


def map_tuple_to_user_object(user_tuple: tuple) -> User:
    """
    Maps tuple loaded from the DB to the User object
    :param user_tuple: a user tuple loaded from the DB
    :return: User object filled with information from the tuple
    """

    return User(user_tuple[1], user_tuple[0])
