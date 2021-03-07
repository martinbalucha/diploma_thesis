import bcrypt
from Persistence.Dao import UserDao


class UserService:
    """
    A service class for business logic operations with
    users
    """

    def __init__(self, user_dao: UserDao):
        """
        Ctor
        :param user_dao: data access object for users
        """

        self.user_dao = user_dao

    def authenticate(self, login: str, password: str) -> bool:
        """
        Performs authentication
        :param login: login given by the user
        :param password: password given by the user
        :return: True, if the login and password were correct,
        otherwise false
        """

        user = self.user_dao.get_user(login)
        if user is not None:
            return bcrypt.checkpw(password, user)
        return False

    def register(self, user):
        pass
