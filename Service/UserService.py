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

    def authenticate(self, username: str, password: str) -> tuple:
        """
        Performs authentication
        :param username: login given by the user
        :param password: password given by the user
        :return: Tuple (True, user) if the authentication was successful,
        otherwise (False, None)
        """

        user = self._user_dao.get_user_by_login(username)
        is_password_correct = False
        if user is not None:
            user_password = user[2]
            is_password_correct = bcrypt.check_password_hash(password=password, pw_hash=user_password)
        return is_password_correct, user

    def register(self, username: str, password: str) -> None:
        """
        Registers a new user into the system
        :param username: a name of the new user
        :param password: a new password given by the user
        """

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        self._user_dao.create(username, password_hash)

    def get_user_by_id(self, user_id: int) -> tuple:
        """
        Gets user with the given ID
        :param user_id: ID of the wanted user
        :return: a user with a given ID. Null if no such user exists
        """

        return self._user_dao.get_user(user_id)