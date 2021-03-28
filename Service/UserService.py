from WebApp import bcrypt
from Persistence.Dao import UserDao


class UserService:
    """
    A service class for business logic operations with
    users
    """

    _user_dao: UserDao

    def __init__(self, user_dao: UserDao):
        """
        Ctor
        :param user_dao: data access object for users
        """

        self._user_dao = user_dao

    def authenticate(self, username: str, password: str) -> bool:
        """
        Performs authentication
        :param username: login given by the user
        :param password: password given by the user
        :return: True, if the login and password were correct,
        otherwise false
        """

        user = self._user_dao.get_user(username)
        if user is not None:
            user_password = user[2]
            return bcrypt.check_password_hash(password=password, pw_hash=user_password)
        return False

    def register(self, username: str, password: str) -> None:
        """
        Registers a new user into the system
        :param username: a name of the new user
        :param password: a new password given by the user
        """

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        self._user_dao.create(username, password_hash)
