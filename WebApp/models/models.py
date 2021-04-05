from flask_login import UserMixin
from Persistence.Dao.UserDao import UserDao
from Service.UserService import UserService
from WebApp import login_manager


class User(UserMixin):
    """
    A class representing user in the system. Inspired by:
    https://github.com/maxcountryman/flask-login/blob/main/test_login.py
    """

    def __init__(self, name: str, user_id: int, active: bool = True):
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


@login_manager.user_loader
def find_user(user_id: int) -> User:
    """
    Loads user with the given ID
    :param user_id: ID of the user that is to be found
    :return: user with information from DB
    """

    user_service = UserService(UserDao())
    user_tuple = user_service.get_user_by_id(user_id)
    return User(user_tuple["username"], user_tuple["id"])
